%define rcver %{nil}
%define snapshot %{nil}

Summary: WPA/WPA2/IEEE 802.1X Supplicant
Name: wpa_supplicant
Epoch: 1
Version: 2.5
Release: 9.git
License: BSD
Source0: hostap.tar.gz
#Source0: http://w1.fi/releases/%{name}-%{version}%{rcver}%{snapshot}.tar.gz
Source1: build-config
Source2: %{name}.conf
Source3: %{name}.service
Source4: %{name}.sysconfig

%define build_gui 0


# distro specific customization and not suitable for upstream,
# works around busted drivers
Patch0: wpa_supplicant-assoc-timeout.patch
# ensures that debug output gets flushed immediately to help diagnose driver
# bugs, not suitable for upstream
Patch1: wpa_supplicant-flush-debug-output.patch
# disto specific customization for log paths, not suitable for upstream
Patch2: wpa_supplicant-dbus-service-file-args.patch
# quiet an annoying and frequent syslog message
Patch3: wpa_supplicant-quiet-scan-results-message.patch
# distro specific customization for Qt4 build tools, not suitable for upstream
Patch6: wpa_supplicant-gui-qt4.patch
# Less aggressive roaming; signal strength is wildly variable
# dcbw states (2015-04):
# "upstream doesn't like that patch so it's been discussed and I think rejected"
Patch8: rh837402-less-aggressive-roaming.patch
# Fix a security issue - rh #rh1241907
# http://w1.fi/security/2015-5/0001-NFC-Fix-payload-length-validation-in-NDEF-record-par.patch
Patch11: rh1241907-NFC-Fix-payload-length-validation-in-NDEF-record-par.patch
# Don't override D-Bus policy for other daemons
# http://lists.infradead.org/pipermail/hostap/2015-October/034036.html
Patch12: 0001-wpa_supplicant-don-t-do-deny-send_interface-.-in-dbu.patch


URL: http://w1.fi/wpa_supplicant/

%if %{build_gui}
BuildRequires: qt-devel >= 4.0
%endif
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: dbus-devel
BuildRequires: libnl3-devel
BuildRequires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
wpa_supplicant is a WPA Supplicant for Linux, BSD and Windows with support
for WPA and WPA2 (IEEE 802.11i / RSN). Supplicant is the IEEE 802.1X/WPA
component that is used in the client stations. It implements key negotiation
with a WPA Authenticator and it controls the roaming and IEEE 802.11
authentication/association of the wlan driver.

%if %{build_gui}

%package gui
Summary: Graphical User Interface for %{name}

%description gui
Graphical User Interface for wpa_supplicant written using QT

%endif

%package -n libeap
Summary: EAP peer library

%description -n libeap
This package contains the runtime EAP peer library. Don't use this
unless you know what you're doing.

%package -n libeap-devel
Summary: Header files for EAP peer library
Requires: libeap = %{epoch}:%{version}-%{release}

%description -n libeap-devel
This package contains header files for using the EAP peer library.
Don't use this unless you know what you're doing.

%prep
%setup -q -n hostap
%patch0 -p1 -b .assoc-timeout
%patch1 -p1 -b .flush-debug-output
%patch2 -p1 -b .dbus-service-file
#%patch3 -p1 -b .quiet-scan-results-msg
#%patch6 -p1 -b .qt4
%patch8 -p1 -b .rh837402-less-aggressive-roaming
%patch12 -p1 -b .dbus-policy

%build
pushd wpa_supplicant
  cp %{SOURCE1} .config
  CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
  CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
  LDFLAGS="${LDFLAGS:-%optflags}" ; export LDFLAGS ;
  # yes, BINDIR=_sbindir
  BINDIR="%{_sbindir}" ; export BINDIR ;
  LIBDIR="%{_libdir}" ; export LIBDIR ;
  make %{_smp_mflags}
%if %{build_gui}
  QTDIR=%{_libdir}/qt4 make wpa_gui-qt4 %{_smp_mflags}
%endif
popd

%install
# init scripts
install -D -m 0644 %{SOURCE3} %{buildroot}/%{_unitdir}/%{name}.service
install -D -m 0644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
# config
install -D -m 0600 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf

# binary
install -d %{buildroot}/%{_sbindir}
install -m 0755 %{name}/wpa_passphrase %{buildroot}/%{_sbindir}
install -m 0755 %{name}/wpa_cli %{buildroot}/%{_sbindir}
install -m 0755 %{name}/wpa_supplicant %{buildroot}/%{_sbindir}
install -D -m 0644 %{name}/dbus/dbus-wpa_supplicant.conf %{buildroot}/%{_sysconfdir}/dbus-1/system.d/wpa_supplicant.conf
install -D -m 0644 %{name}/dbus/fi.w1.wpa_supplicant1.service %{buildroot}/%{_datadir}/dbus-1/system-services/fi.w1.wpa_supplicant1.service
install -D -m 0644 %{name}/dbus/fi.epitest.hostap.WPASupplicant.service %{buildroot}/%{_datadir}/dbus-1/system-services/fi.epitest.hostap.WPASupplicant.service

%if %{build_gui}
# gui
install -d %{buildroot}/%{_bindir}
install -m 0755 %{name}/wpa_gui-qt4/wpa_gui %{buildroot}/%{_bindir}
%endif

# man pages
#git codes, not pre-generated man pages.
#install -d %{buildroot}%{_mandir}/man{5,8}
#install -m 0644 %{name}/doc/docbook/*.8 %{buildroot}%{_mandir}/man8
#install -m 0644 %{name}/doc/docbook/*.5 %{buildroot}%{_mandir}/man5

# some cleanup in docs and examples
rm -f  %{name}/doc/.cvsignore
rm -rf %{name}/doc/docbook
chmod -R 0644 %{name}/examples/*.py

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable wpa_supplicant.service > /dev/null 2>&1 || :
    /bin/systemctl stop wpa_supplicant.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart wpa_supplicant.service >/dev/null 2>&1 || :
fi



%files
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_sysconfdir}/dbus-1/system.d/%{name}.conf
%{_datadir}/dbus-1/system-services/fi.epitest.hostap.WPASupplicant.service
%{_datadir}/dbus-1/system-services/fi.w1.wpa_supplicant1.service
%{_sbindir}/wpa_passphrase
%{_sbindir}/wpa_supplicant
%{_sbindir}/wpa_cli
%dir %{_sysconfdir}/%{name}
#%{_mandir}/man8/*
#%{_mandir}/man5/*

%if %{build_gui}
%files gui
%{_bindir}/wpa_gui
%endif

%changelog
* Sun Nov 15 2015 Cjacker <cjacker@foxmail.com> - 1:2.5-9.git
- Update to latest git

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 1:2.5-8.git
- Update to git f10ff62

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:2.5-7.git
- Rebuild for new 4.0 release.

* Wed Aug 05 2015 Cjacker <cjacker@foxmail.com>
- update to ab653ed
