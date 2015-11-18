%define nm_version          1:0.9.9.95
%define dbus_version        1.1
%define gtk3_version        3.4.0
%define openconnect_version 7.00

Summary:   NetworkManager VPN plugin for openconnect
Name:      NetworkManager-openconnect
Version:   1.0.2
Release:   5
License:   GPLv2+, LGPLv2.1
URL:       http://www.gnome.org/projects/NetworkManager/
Source:    https://download.gnome.org/sources/NetworkManager-openconnect/1.0/%{name}-%{version}.tar.xz

BuildRequires: gtk3-devel             >= %{gtk3_version}
BuildRequires: dbus-devel             >= %{dbus_version}
BuildRequires: dbus-glib-devel        >= 0.100
BuildRequires: NetworkManager-devel   >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: libsecret-devel
BuildRequires: intltool gettext
BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(openconnect) >= %{openconnect_version}

Requires: NetworkManager   >= %{nm_version}
Requires: openconnect      >= %{openconnect_version}

Requires(pre): %{_sbindir}/useradd
Requires(pre): %{_sbindir}/groupadd

%description
This package contains software for integrating the openconnect VPN software
with NetworkManager and the GNOME desktop

%package -n NetworkManager-openconnect-gnome
Summary: NetworkManager VPN plugin for OpenConnect - GNOME files

Requires: NetworkManager-openconnect = %{version}-%{release}
Requires: network-manager-applet

%description -n NetworkManager-openconnect-gnome
This package contains software for integrating VPN capabilities with openconnect
with NetworkManager (GNOME files).


%prep
%setup -q

%build
autoreconf -ivf
%configure \
    --enable-more-warnings=yes
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a

%find_lang %{name}

%pre
%{_sbindir}/groupadd -r nm-openconnect &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d / -M \
                     -c 'NetworkManager user for OpenConnect' \
                     -g nm-openconnect nm-openconnect &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING
%{_sysconfdir}/dbus-1/system.d/nm-openconnect-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-openconnect-service.name
%{_libexecdir}/nm-openconnect-service
%{_libexecdir}/nm-openconnect-service-openconnect-helper
%{_libexecdir}/nm-openconnect-auth-dialog

%files -n NetworkManager-openconnect-gnome
%doc COPYING AUTHORS ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/openconnect
%{_datadir}/gnome-vpn-properties/openconnect/nm-openconnect-dialog.ui

%changelog
* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 1.0.2-5
- Rebuild

* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 1.0.2-4
- Rebuild, sep gnome pkg

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.2-3
- Rebuild for new 4.0 release.

