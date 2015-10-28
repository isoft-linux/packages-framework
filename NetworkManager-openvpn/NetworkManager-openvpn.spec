#global commit %{nil}
#global snapshot %{nil}%{commit}

Summary:   NetworkManager VPN plugin for OpenVPN
Name:      NetworkManager-openvpn
Epoch:     1
Version:   1.0.2
Release:   4%{?snapshot}%{?dist}
License:   GPLv2+
URL:       http://www.gnome.org/projects/NetworkManager/
# git clone git://git.gnome.org/network-manager-openvpn
# cd network-manager-openvpn
# ./autogen.sh
# make dist
# mv NetworkManager-openvpn-0.9.9.0.tar.bz2 NetworkManager-openvpn-0.9.9.0-5afb8eb.tar.bz2
Source0:   http://ftp.gnome.org/pub/GNOME/sources/%{name}/1.0/%{name}-%{version}%{?commit:-%{commit}}.tar.xz

Patch0:    0001-reneg-sec.patch

BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: glib2-devel
BuildRequires: libtool intltool gettext
BuildRequires: libnm-gtk-devel >= 0.9.9.0
BuildRequires: libsecret-devel

Requires: gtk3
Requires: dbus
Requires: NetworkManager
Requires: openvpn
Requires: shared-mime-info
Obsoletes: NetworkManager-openvpn < 1:0.9.8.2-3

%global _privatelibs libnm-openvpn-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the OpenVPN server with NetworkManager.

%package -n NetworkManager-openvpn-gnome
Summary: NetworkManager VPN plugin for OpenVPN - GNOME files

Requires: NetworkManager-openvpn = %{epoch}:%{version}-%{release}
Requires: network-manager-applet
Obsoletes: NetworkManager-openvpn < 1:0.9.8.2-3

%description -n NetworkManager-openvpn-gnome
This package contains software for integrating VPN capabilities with
the OpenVPN server with NetworkManager (GNOME files).

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .0001-reneg-sec.orig

%build
if [ ! -f configure ]; then
  ./autogen.sh
fi
%configure \
        --disable-static \
        --disable-dependency-tracking \
        --enable-more-warnings=yes \
        --with-gnome
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS README ChangeLog
%{_sysconfdir}/dbus-1/system.d/nm-openvpn-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-openvpn-service.name
%{_libexecdir}/nm-openvpn-service
%{_libexecdir}/nm-openvpn-auth-dialog
%{_libexecdir}/nm-openvpn-service-openvpn-helper

%files -n NetworkManager-openvpn-gnome
%doc COPYING AUTHORS README ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/openvpn
%{_datadir}/gnome-vpn-properties/openvpn/nm-openvpn-dialog.ui

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:1.0.2-4
- Rebuild for new 4.0 release.

