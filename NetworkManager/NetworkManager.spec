%define build_nmtui 1

%define with_systemd 1 

%define dbus_version 1.1
%define dbus_glib_version 0.86-4

%define glib2_version	2.24.0
%define wireless_tools_version 1:28-0pre9
%define ppp_version 2.4.6

%define systemd_dir /usr/lib/systemd/system/

Name: NetworkManager
Summary: Network connection manager and user applications
Epoch: 1
Version: 1.0.2 
Release: 4 
Group: System Environment/Base
License: GPLv2+
URL: http://www.gnome.org/projects/NetworkManager/

Source: %{name}-%{version}.tar.xz
Source2: NetworkManager.conf
Source3: NetworkManager.init
Patch0: explain-dns1-dns2.patch
Patch1: NetworkManager-fix-polkit-icon-missing.patch

Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: glib2 >= %{glib2_version}
Requires: iproute
Requires: dhcpcd
Requires: wpa_supplicant >= 1:0.7.3-1
Requires: libnl3
Requires: %{name}-glib = %{epoch}:%{version}-%{release}
Requires: ppp >= %{ppp_version}
Requires: udev
#Requires: mobile-broadband-provider-info >= 0.20090602
#Requires: ModemManager >= 0.4
Obsoletes: dhcdbd

Conflicts: NetworkManager-vpnc < 1:0.7.0.99-1
Conflicts: NetworkManager-openvpn < 1:0.7.0.99-1
Conflicts: NetworkManager-pptp < 1:0.7.0.99-1
Conflicts: NetworkManager-openconnect < 0:0.7.0.99-1

BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: wireless-tools-devel >= %{wireless_tools_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildRequires: wpa_supplicant
BuildRequires: libnl3-devel
BuildRequires: perl(XML::Parser)
BuildRequires: automake autoconf intltool libtool
BuildRequires: ppp >= %{ppp_version}
BuildRequires: ppp-devel >= %{ppp_version}
BuildRequires: nss-devel >= 3.11.7
BuildRequires: libudev-devel
BuildRequires: libuuid-devel
BuildRequires: libndp-devel
BuildRequires: libgudev-devel >= 143
BuildRequires: ModemManager-devel
BuildRequires: dhcpcd
BuildRequires: libsoup-devel
%if %{with_systemd}
BuildRequires: systemd >= 200-3 systemd-devel
%endif

%if %{build_nmtui}
BuildRequires: newt >= 0.52.15
%endif

%description
NetworkManager is a system network service that manages your network devices
and connections, attempting to keep active network connectivity when available.
It manages ethernet, WiFi, mobile broadband (WWAN), and PPPoE devices, and
provides VPN integration with a variety of different VPN services.


%package devel
Summary: Libraries and headers for adding NetworkManager support to applications
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: dbus-devel >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: pkgconfig

%description devel
This package contains various headers accessing some NetworkManager functionality
from applications.

%package glib
Summary: Libraries for adding NetworkManager support to applications that use glib.
Group: Development/Libraries
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}

%description glib
This package contains the libraries that make it easier to use some NetworkManager
functionality from applications that use glib.


%package glib-devel
Summary: Header files for adding NetworkManager support to applications that use glib.
Group: Development/Libraries
Requires: %{name}-devel = %{epoch}:%{version}-%{release}
Requires: %{name}-glib = %{epoch}:%{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig
Requires: dbus-glib-devel >= %{dbus_glib_version}

%description glib-devel
This package contains the header and pkg-config files for development applications using
NetworkManager functionality from applications that use glib.


%package tui 
Summary: Newt based console ui for Networkmanager 
Group:   System Environment/Base 

%description tui
Newt based console ui for Networkmanager

%prep
%setup -q -n NetworkManager-%{version}
%patch1 -p1

%build
%configure \
	--disable-static \
	--enable-ifcfg-rh \
	--with-dhclient=no \
	--with-dhcpcd=/usr/sbin/dhcpcd \
	--with-crypto=nss \
	--enable-more-warnings=yes \
	--enable-wimax=no \
    	--with-system-ca-path=/etc/pki/tls/cert.pem \
	--with-tests=no \
    	--disable-gtk-doc \
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version} \
	--with-dist-version=%{version}-%{release} \
    	--enable-introspection \
    	--with-modem-manager-1 \
    	--enable-bluez5-dun \
    	--without-iptables \
    	--enable-vala=no  \
    	--enable-concheck=yes \
    %if %{build_nmtui}
    	--with-nmtui=yes \
    %endif
    %if %{with_systemd}
    	--with-session-tracking=systemd \
    	--with-suspend-resume=systemd \
    %else
    	--with-session-tracking=none 
    %endif


make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT

# install NM
make install DESTDIR=$RPM_BUILD_ROOT DATADIRNAME=share

%{__cp} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/

# create a VPN directory
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/VPN

# create a keyfile plugin system settings directory
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/system-connections

%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

%{__mkdir_p} $RPM_BUILD_ROOT%{_localstatedir}/lib/NetworkManager

%find_lang %{name}

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/pppd/%{ppp_version}/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/NetworkManager/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/gnome-bluetooth/plugins/*.la


%if %{with_systemd}
mkdir -p $RPM_BUILD_ROOT%{systemd_dir}/network-online.target.wants
#ln -s ../NetworkManager-wait-online.service $RPM_BUILD_ROOT%{systemd_dir}/network-online.target.wants
%else
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 0755 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/NetworkManager
%endif


rpmclean
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
%systemd_post NetworkManager.service NetworkManager-wait-online.service NetworkManager-dispatcher.service
/bin/systemctl enable NetworkManager ||:
%preun
if [ $1 -eq 0 ]; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable NetworkManager.service >/dev/null 2>&1 || :

    # Don't kill networking entirely just on package remove
    #/bin/systemctl stop NetworkManager.service >/dev/null 2>&1 || :
fi
%systemd_preun NetworkManager-wait-online.service

%postun
%systemd_postun

%post	glib -p /sbin/ldconfig
%postun	glib -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING NEWS AUTHORS README CONTRIBUTING TODO
%{_sysconfdir}/dbus-1/system.d/*
%{_sbindir}/%{name}
%{_bindir}/nmcli
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/dispatcher.d
%dir %{_sysconfdir}/%{name}/VPN
%config(noreplace) %{_sysconfdir}/%{name}/NetworkManager.conf
#%{_bindir}/nm-tool
%{_bindir}/nm-online
%{_libexecdir}/nm-dhcp-helper
%{_libexecdir}/nm-dispatcher
%{_libexecdir}/nm-avahi-autoipd.action
%{_libexecdir}/nm-iface-helper
%dir %{_libdir}/NetworkManager
%{_libdir}/NetworkManager/*.so*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*


%{_libdir}/girepository-1.0/NM-1.0.typelib
%{_libdir}/libnm.so.*


%dir %{_localstatedir}/run/NetworkManager
%dir %{_localstatedir}/lib/NetworkManager
%dir %{_sysconfdir}/NetworkManager/system-connections
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_libdir}/pppd/%{ppp_version}/nm-pppd-plugin.so
%{_datadir}/polkit-1/actions/*.policy
/lib/udev/rules.d/*.rules
%{_datadir}/bash-completion/completions/nmcli

%if %{with_systemd}
# systemd stuff
%{_datadir}/dbus-1/system-services/org.freedesktop.NetworkManager.service
%{systemd_dir}/NetworkManager.service
%{systemd_dir}/NetworkManager-wait-online.service
%{systemd_dir}/network-online.target.wants/NetworkManager-wait-online.service
%{systemd_dir}/NetworkManager-dispatcher.service
%else
%{_sysconfdir}/rc.d/init.d/NetworkManager
%endif
%{_libdir}/girepository-?.?/NetworkManager-1.0.typelib

%files devel
%defattr(-,root,root,0755)
%doc ChangeLog docs/api/html/*
%{_libdir}/libnm.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/%{name}.h
%{_includedir}/%{name}/NetworkManagerVPN.h
%{_includedir}/%{name}/nm-version.h
%dir %{_includedir}/libnm
%{_includedir}/libnm/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/libnm.pc
%{_datadir}/gtk-doc/html/NetworkManager
%{_datadir}/gtk-doc/html/libnm
%{_datadir}/gir-?.?/NetworkManager-1.0.gir
%{_datadir}/gir-?.?/NM-1.0.gir

%files glib
%defattr(-,root,root,0755)
%{_libdir}/libnm-glib.so.*
%{_libdir}/libnm-glib-vpn.so.*
%{_libdir}/libnm-util.so.*
%{_libdir}/girepository-?.?/NMClient-1.0.typelib



%files glib-devel
%defattr(-,root,root,0755)
%dir %{_includedir}/libnm-glib
%{_includedir}/libnm-glib/*.h
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/libnm-glib.pc
%{_libdir}/pkgconfig/libnm-glib-vpn.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-glib.so
%{_libdir}/libnm-glib-vpn.so
%{_libdir}/libnm-util.so
%{_datadir}/gtk-doc/html/libnm-glib
%{_datadir}/gtk-doc/html/libnm-util
%{_datadir}/gir-?.?/NMClient-1.0.gir

%if %{build_nmtui}
%files tui
%defattr(-,root,root,0755)
%{_bindir}/nmtui
%{_bindir}/nmtui-connect
%{_bindir}/nmtui-edit
%{_bindir}/nmtui-hostname
%endif

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

