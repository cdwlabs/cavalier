![Run Test Suite](https://github.com/cdwlabs/cavalier/workflows/Run%20Test%20Suite/badge.svg)
![Build Binaries](https://github.com/cdwlabs/cavalier/workflows/Build%20Binaries/badge.svg)
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/cdwlabs/cavalier)

# Cavalier

As physical hardware ages we end up reliant on firmware that is difficult to connect to. In particular older servers often have web interfaces that require Flash and Java be detected in the browser to both login to them and then launch a KVM session.

For whatever reason you may find yourself working on such old hardware and might struggle to install the magic combination of browser, flash and Java at the correct versions in the correct places on the right operating system. Cavalier removes this obstacle by logging in via the API and downloading the JNLP file that Java Web Start can use to start the KVM session.

## Short Demonstration Video

![](cavalier-demo-2021.gif)

## Getting Started

We use GitHub Actions and PyInstaller to build single file executables. These are unsigned so you may need to disable certain security checks to launch them. The files are available on the [releases](https://github.com/cdwlabs/cavalier/releases) page.

You will need a Java implementation that supports Java Web Start (JWS). The Oracle JDK removed it starting in version 11. Projects like IcedTea and OpenWebStart are open source replacements. This app was tested with IcedTea on Linux.

### Remarks on Java Web Start

A complication to the problem that Cavalier helps solve is the usage of Java Web Start by the CIMC. Java Web Start was removed in Java SE 11. Because this application actually launches the Java runtime installed on the system it also requires a functional implementation of Java Web Start to be installed in some cases.

### Java Web Start via IcedTea on Ubuntu 20.04

    apt install icedtea-netx

### Java Web Start via IcedTea on Fedora, CentOS 7, and CentOS 8

> Yum is used intentionally here for compatibility across all of these platforms.

    yum install icedtea-web

### Java Web Start via OpenWebStart on Mac OS X 

Brew is used here as an example. It can also be installed directly: [OpenWebStart Installation Instructions](https://openwebstart.com/docs/OWSGuide.html#_interactive_installation)

    brew install --cask openwebstart

### Java Web Start via OpenWebStart on Windows

It can be installed directly when following the instructions found here: [OpenWebStart Installation Instructions](https://openwebstart.com/docs/OWSGuide.html#_interactive_installation)

# Running From The Repository

If you'd like to run it directly from the repos that is possible. It's not currently posted to PyPI. This will install all of the necessary Python dependencies. The `--editable` flag can be used for local development.

    python -m pip install git+https://github.com/cdwlabs/cavalier.git
