%global snapshot .20150428git695d4f2
%global ppp_version %(rpm -q ppp --queryformat '%{VERSION}')

Summary:   NetworkManager VPN plugin for PPTP
Name:      NetworkManager-pptp
Epoch:     1
Version:   1.1.0
Release:   2%{snapshot}%{?dist}
License:   GPLv2+
URL:       http://www.gnome.org/projects/NetworkManager/
Group:     System Environment/Base
Source0:   https://download.gnome.org/sources/NetworkManager-pptp/1.0/%{name}-%{version}%{snapshot}.tar.bz2

BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: glib2-devel
BuildRequires: ppp-devel
BuildRequires: libtool intltool gettext
BuildRequires: libsecret-devel
BuildRequires: libnm-gtk-devel

Requires: gtk3
Requires: dbus
Requires: NetworkManager
Requires: pptp
Requires: ppp
Requires: shared-mime-info
Requires: gnome-keyring
Requires: libnm-gtk
Obsoletes: NetworkManager-pptp < 1:0.9.8.2-3

%global _privatelibs libnm-pptp-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the PPTP server with NetworkManager.

%package -n NetworkManager-pptp-gnome
Summary: NetworkManager VPN plugin for PPTP - GNOME files
Group:   System Environment/Base

Requires: NetworkManager-pptp = %{epoch}:%{version}-%{release}
Requires: network-manager-applet
Obsoletes: NetworkManager-pptp < 1:0.9.8.2-3

%description -n NetworkManager-pptp-gnome
This package contains software for integrating VPN capabilities with
the PPTP server with NetworkManager (GNOME files).

%prep
%setup -q -n %{name}-%{version}

%build
if [ ! -f configure ]; then
  ./autogen.sh
fi
%configure \
	--disable-static \
	--enable-more-warnings=yes \
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version}
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a
rm -f %{buildroot}%{_libdir}/pppd/%{ppp_version}/*.la

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS README ChangeLog
%{_sysconfdir}/dbus-1/system.d/nm-pptp-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-pptp-service.name
%{_libexecdir}/nm-pptp-service
%{_libexecdir}/nm-pptp-auth-dialog
%{_libdir}/pppd/%{ppp_version}/nm-pptp-pppd-plugin.so

%files -n NetworkManager-pptp-gnome
%doc COPYING AUTHORS README ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/pptp
%{_datadir}/gnome-vpn-properties/pptp/nm-pptp-dialog.ui

%changelog
