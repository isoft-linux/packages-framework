%define rcver %{nil}
%define snapshot %{nil}

Summary: WPA/WPA2/IEEE 802.1X Supplicant
Name: wpa_supplicant
Epoch: 1
Version: 2.5
Release: 5.git
License: BSD
Group:  Framework/Runtime/Utility
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
Group: Applications/System

%description gui
Graphical User Interface for wpa_supplicant written using QT

%endif

%package -n libeap
Summary: EAP peer library
Group: System Environment/Libraries

%description -n libeap
This package contains the runtime EAP peer library. Don't use this
unless you know what you're doing.

%package -n libeap-devel
Summary: Header files for EAP peer library
Group: Development/Libraries
Requires: libeap = %{epoch}:%{version}-%{release}

%description -n libeap-devel
This package contains header files for using the EAP peer library.
Don't use this unless you know what you're doing.

%prep
%setup -q -n hostap
%patch0 -p1 -b .assoc-timeout
%patch1 -p1 -b .flush-debug-output
%patch2 -p1 -b .dbus-service-file

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
* Wed Aug 05 2015 Cjacker <cjacker@foxmail.com>
- update to ab653ed
