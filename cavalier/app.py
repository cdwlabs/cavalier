from tkinter import Button, Entry, Frame, Label, StringVar, Tk

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import xml.etree.ElementTree as ET
from subprocess import Popen

from socket import AF_INET, AF_INET6, gaierror, getaddrinfo, inet_ntop, inet_pton, IPPROTO_TCP
from urllib.parse import urlencode

class Cavalier(Frame):
    def __init__(self, parent, *args, **kwargs):
        # Setup App Internals
        self.sessions = []
        # Setup GUI
        super().__init__(parent)
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.winfo_toplevel().title("Cavalier")
        self.create_widgets()


    def create_widgets(self):
        self.status = StringVar()
        self.status.set("Fill in the details and click the button!")
        self.lstatus = Label(self, textvariable = self.status, fg = "black")
        self.lstatus.grid(row = 0, columnspan = 2)
        self.lcimc = Label(self, text = "IP/Hostname")
        self.lcimc.grid(row = 1, column = 0)
        self.cimc = Entry(self)
        self.cimc.grid(row = 1, column = 1)
        self.lusername = Label(self, text = "Username")
        self.lusername.grid(row = 2, column = 0)
        self.username = Entry(self)
        self.username.grid(row = 2, column = 1)
        self.lpassword = Label(self, text = "Password")
        self.lpassword.grid(row = 3, column = 0)
        self.password = Entry(self)
        self.password.grid(row = 3, column = 1)
        self.launch = Button(self)
        self.launch["text"] = "Launch the Remote KVM Java Applet"
        self.launch["command"] = self.kvm
        self.launch.grid(row = 4, columnspan = 2)


    def kvm(self):
        # build the base uri for the api calls
        self.status.set("Building the API URI")
        self.lstatus.config(fg = "dark green")
        root.update_idletasks()
        cimc = self.cimc.get()
        base = "https://{}".format(cimc)
        # check for an ipv6 literal and ensure it gets wrapped in brackets
        try:
            cimc = inet_ntop(inet_pton(AF_INET6, cimc))
            base = "https://[{}]".format(cimc)
        except:
            pass
        api = "{}/nuova".format(base)
        headers = { "Content-Type": "application/x-www-form-urlencoded" }

        aaaLogin = ET.Element("aaaLogin")
        aaaLogin.set("inName", self.username.get())
        aaaLogin.set("inPassword", self.password.get())
        print(ET.tostring(aaaLogin, encoding = "unicode", method = "xml"))
        res = requests.post(api, headers = headers, data = ET.tostring(aaaLogin, encoding = "unicode", method = "xml"), verify = False)
        if res.status_code == 200:
            self.status.set("Extracting the cookie!")
            root.update_idletasks()
            cookie = ET.fromstring(res.text).attrib["outCookie"]

            self.status.set("Setting up scheduled token refreshing!")
            self.master.update_idletasks()
            timing = round(int(ET.fromstring(res.text).attrib["outRefreshPeriod"]) * 0.90) * 1000
            self.sessions.append({
                "cookie": cookie,
                "cur_sman_id": self.master.after(timing, self.sman, timing, api, cookie, headers, self.username.get(), self.password.get())
                })
            
            self.status.set("Obtaining compute authorization tokens!")
            root.update_idletasks()
            aaaGetComputeAuthTokens = ET.Element("aaaGetComputeAuthTokens")
            aaaGetComputeAuthTokens.set("cookie", cookie)
            print(ET.tostring(aaaGetComputeAuthTokens, encoding = "unicode", method = "xml"))
            res = requests.post(api, headers = headers, data = ET.tostring(aaaGetComputeAuthTokens, encoding = "unicode", method = "xml"), verify = False)
            self.status.set("Building URL for Java Web Start to launch the KVM App!")
            root.update_idletasks()
            kvm = "{}/kvm.jnlp?{}".format(base, urlencode({
                "cimcAddr": cimc,
                "tkn1": ET.fromstring(res.text).attrib["outTokens"].split(",")[0],
                "tkn2": ET.fromstring(res.text).attrib["outTokens"].split(",")[1]
                }))
            print(kvm)
            
            self.status.set("Launching the app via Java Web Start!")
            root.update_idletasks()
            viewer = Popen(["javaws", kvm])
            self.master.after_idle(self.pman, api, cimc, cookie, headers, viewer)


    def find(self, lst, key, val):
        for idx, dic in enumerate(lst):
            if dic[key] == val:
                return idx 
        return ValueError


    def pman(self, api, cimc, cookie, headers, viewer):
        if viewer.poll() == None:
            self.master.after_idle(self.pman, api, cimc, cookie, headers, viewer)
        else:
            try:
                self.master.after_cancel(
                    self.sessions[self.find(self.sessions, "cookie", cookie)]["cur_sman_id"])
            except ValueError:
                print("Failed to find the session in the session manager database. It might not be cancelled.")
            aaaLogout = ET.Element("aaaLogout")
            aaaLogout.set("cookie", cookie)
            aaaLogout.set("inCookie", cookie)
            print(ET.tostring(aaaLogout, encoding = "unicode", method = "xml"))
            res = requests.post(api, headers = headers, data = ET.tostring(aaaLogout, encoding = "unicode", method = "xml"), verify = False)


    def sman(self, timing, api, cookie, headers, username, password):
        aaaRefresh = ET.Element("aaaRefresh")
        aaaRefresh.set("cookie", cookie)
        aaaRefresh.set("inCookie", cookie)
        aaaRefresh.set("inName", username)
        aaaRefresh.set("inPassword", password)
        print(ET.tostring(aaaRefresh, encoding = "unicode", method = "xml"))
        res = requests.post(api, headers = headers, data = ET.tostring(aaaRefresh, encoding = "unicode", method = "xml"), verify = False)
        if res.status_code == 200:
            try:
                self.sessions[self.find(self.sessions, "cookie", cookie)]["cur_sman_id"] = \
                    self.master.after(timing, self.sman, timing, api, cookie, headers, username, password)
            except ValueError:
                print("sman entry not found, likely failed to schedule session renewal!")


def main():
#if __name__ == "__main__":
    #import pdb; pdb.set_trace()
    root = Tk()
    root.title("Cavalier")
    cavalier = Cavalier(root)
    cavalier.mainloop()
