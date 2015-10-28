# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Enable hardened build, as the udev part runs with privilege.
%define _hardened_build 1

Summary: A printer administration tool
Name: system-config-printer
Version: 1.5.7
Release: 7%{?dist}
License: GPLv2+
URL: http://cyberelk.net/tim/software/system-config-printer/
Source0: http://cyberelk.net/tim/data/system-config-printer/1.5/%{name}-%{version}.tar.xz
Patch1: system-config-printer-shbang.patch
Patch2: system-config-printer-device-sorting.patch

BuildRequires: cups-devel >= 1.2
BuildRequires: desktop-file-utils >= 0.2.92
BuildRequires: gettext-devel
BuildRequires: intltool
BuildRequires: libusb1-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: xmlto
BuildRequires: systemd-units, systemd-devel
BuildRequires: python3-devel

Requires: python3-gobject%{?_isa}
Requires: gtk3%{?_isa}
Requires: desktop-file-utils >= 0.2.92
Requires: dbus-x11
Requires: python3-dbus%{?_isa}
Requires: system-config-printer-libs = %{version}-%{release}
#Requires: desktop-notification-daemon
Requires: libnotify%{?_isa}
#Requires: libgnome-keyring%{?_isa}
Requires: python3-cairo%{?_isa}
#Requires: python3-firewall
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
system-config-printer is a graphical user interface that allows
the user to configure a CUPS print server.

%package libs
Summary: Libraries and shared code for printer administration tool
Requires: python3-cups >= 1.9.60
Requires: python3-pycurl
Requires: gobject-introspection
Requires: python3-gobject
Requires: gtk3
Requires: python3-dbus
Requires: python3-requests
Suggests: python-smbc
BuildArch: noarch
Obsoletes: %{name}-libs < 1.3.12-10

%description libs
The common code used by both the graphical and non-graphical parts of
the configuration tool.

%package applet
Summary: Print job notification applet
Requires: %{name}-libs

%description applet
Print job notification applet.

%package udev
Summary: Rules for udev for automatic configuration of USB printers
Requires: system-config-printer-libs = %{version}-%{release}
Obsoletes: hal-cups-utils < 0.6.20
Provides: hal-cups-utils = 0.6.20

%description udev
The udev rules and helper programs for automatically configuring USB
printers.

%prep
%setup -q

# Fixed shbang line in udev-add-printer (trac #244).
%patch1 -p1 -b .shbang

# Fixed device sorting (bug #1210733).
%patch2 -p1 -b .device-sorting

%build
%configure --with-udev-rules
make %{?_smp_mflags}

%install
make DESTDIR=%buildroot install

%{__mkdir_p} %buildroot%{_localstatedir}/run/udev-configure-printer
touch %buildroot%{_localstatedir}/run/udev-configure-printer/usb-uris

# Manually invoke the python byte compile macro for each path that
# needs byte compilation
%py_byte_compile %{__python3} %{buildroot}%{python3_sitelib}/cupshelpers
%py_byte_compile %{__python3} %{buildroot}%{datadir}/system-config-printer

#hide desktop item.
echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/system-config-printer.desktop

%find_lang system-config-printer

%files libs -f system-config-printer.lang
%doc COPYING
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.redhat.NewPrinterNotification.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.redhat.PrinterDriversInstaller.conf
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/services/*.service
%{_bindir}/scp-dbus-service
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/asyncconn.py*
%{_datadir}/%{name}/asyncipp.py*
%{_datadir}/%{name}/asyncpk1.py*
%{_datadir}/%{name}/authconn.py*
%{_datadir}/%{name}/config.py*
%{_datadir}/%{name}/cupspk.py*
%{_datadir}/%{name}/debug.py*
%{_datadir}/%{name}/dnssdresolve.py*
%{_datadir}/%{name}/errordialogs.py*
%{_datadir}/%{name}/firewallsettings.py*
%{_datadir}/%{name}/gtkinklevel.py*
%{_datadir}/%{name}/gui.py*
%{_datadir}/%{name}/installpackage.py*
%{_datadir}/%{name}/jobviewer.py*
%{_datadir}/%{name}/killtimer.py*
%{_datadir}/%{name}/monitor.py*
%{_datadir}/%{name}/newprinter.py*
%{_datadir}/%{name}/options.py*
%{_datadir}/%{name}/optionwidgets.py*
%{_datadir}/%{name}/OpenPrintingRequest.py*
%{_datadir}/%{name}/PhysicalDevice.py*
%{_datadir}/%{name}/ppdcache.py*
%{_datadir}/%{name}/ppdippstr.py*
%{_datadir}/%{name}/ppdsloader.py*
%{_datadir}/%{name}/printerproperties.py*
%{_datadir}/%{name}/probe_printer.py*
%{_datadir}/%{name}/pysmb.py*
%{_datadir}/%{name}/scp-dbus-service.py*
%{_datadir}/%{name}/smburi.py*
%{_datadir}/%{name}/statereason.py*
%{_datadir}/%{name}/timedops.py*
%dir %{_sysconfdir}/cupshelpers
%config(noreplace) %{_sysconfdir}/cupshelpers/preferreddrivers.xml
%{python3_sitelib}/cupshelpers
%{python3_sitelib}/*.egg-info

%files applet
%{_bindir}/%{name}-applet
%{_datadir}/%{name}/applet.py*
%{_sysconfdir}/xdg/autostart/print-applet.desktop
%{_mandir}/man1/%{name}-applet.1*

%files udev
%{_prefix}/lib/udev/rules.d/*.rules
%{_prefix}/lib/udev/udev-*-printer
%ghost %dir %{_localstatedir}/run/udev-configure-printer
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %attr(0644,root,root) %{_localstatedir}/run/udev-configure-printer/usb-uris
%{_unitdir}/configure-printer@.service

%files
%doc ChangeLog README
%{_bindir}/%{name}
%{_bindir}/install-printerdriver
%{_datadir}/%{name}/check-device-ids.py*
%{_datadir}/%{name}/HIG.py*
%{_datadir}/%{name}/SearchCriterion.py*
%{_datadir}/%{name}/serversettings.py*
%{_datadir}/%{name}/system-config-printer.py*
%{_datadir}/%{name}/ToolbarSearchEntry.py*
%{_datadir}/%{name}/userdefault.py*
%{_datadir}/%{name}/troubleshoot
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/install-printerdriver.py*
%dir %{_datadir}/%{name}/xml
%{_datadir}/%{name}/xml/*.rng
%{_datadir}/%{name}/xml/validate.py*
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/ui/*.ui
%{_datadir}/applications/system-config-printer.desktop
%{_datadir}/appdata/*.appdata.xml
%{_mandir}/man1/%{name}.1*

%post
/bin/rm -f /var/cache/foomatic/foomatic.pickle
exit 0

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.5.7-7
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- tune desktop file.

