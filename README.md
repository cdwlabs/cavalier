# Cavalier
As physical hardware ages we end up reliant on firmware that is difficult to connect to. In particular older servers often have web interfaces that require Flash and Java be detected in the browser to both login to them and then launch a KVM session.

For whatever reason you may find yourself working on such old hardware and might struggle to install the magic combination of browser, flash and Java at the correct versions in the correct places on the right operating system. Cavalier removes this obstacle by logging in via the API and downloading the JNLP file that Java Web Start can use to start the KVM session.

# Short Demonstration Video
![](cavalier-demo-2021.gif)

# Getting Started
We use GitHub Actions and PyInstaller to build single file executables. These are unsigned so you may need to disable certain security checks to launch them. The files are available on the [releases](https://github.com/cdwlabs/cavalier/releases) page.

You will need a Java implementation that supports launching JNLP files. In Linux the IcedTea project is able to do this.

## IcedTea on Ubuntu 20.04
    apt install icedtea-netx

## IcedTea on Fedora, CentOS 7, and CentOS 8
    dnf install icedtea-web

# Running From The Repository
If you'd like to run it directly from the repos that is possible. It's not currently posted to PyPI.

    python -m pip install git+https://github.com/cdwlabs/cavalier.git