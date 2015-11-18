%global ppp_version %(rpm -q ppp --queryformat '%{VERSION}')

Summary:   NetworkManager VPN plugin for PPTP
Name:      NetworkManager-pptp
Epoch:     2
Version:   1.0.2
Release:   3%{?dist}
License:   GPLv2+
URL:       http://www.gnome.org/projects/NetworkManager/
Source0:   https://download.gnome.org/sources/NetworkManager-pptp/1.0/%{name}-%{version}.tar.xz

BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: glib2-devel
BuildRequires: ppp-devel
BuildRequires: libtool intltool gettext
BuildRequires: libsecret-devel
BuildRequires: libnm-gtk-devel >= 0.9

Requires: dbus
Requires: NetworkManager >= 1.0.2 
Requires: pptp
Requires: ppp

%global _privatelibs libnm-pptp-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the PPTP server with NetworkManager.


%package -n NetworkManager-pptp-gnome
Summary: NetworkManager VPN plugin for PPTP - GNOME files

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
* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 2:1.0.2-3
- Rebuild

* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 2:1.0.2-2
- Downgrade to 1.0.2 official release, increase the Epoch

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:1.1.0-3.20150428git695d4f2
- Rebuild for new 4.0 release.

