%global ppp_version %(rpm -q ppp --queryformat '%{VERSION}')

Summary:   NetworkManager VPN plugin for l2tp
Name:      NetworkManager-l2tp
Version:   0.9.8.7
Release:   7%{?dist}
# The most of code uses GPLv2+ license.
# Only vpn-password-dialog has LGPLv2+.
License:   GPLv2+ and LGPLv2+
URL:       https://launchpad.net/~seriy-pr/+archive/network-manager-l2tp
Source:    https://github.com/seriyps/NetworkManager-l2tp/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: libtool automake autoconf
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: intltool gettext
BuildRequires: ppp-devel

Requires: network-manager-applet
Requires: dbus
Requires: NetworkManager
Requires: ppp = %{ppp_version}
Requires: shared-mime-info
Requires: pptp
Requires: gnome-keyring
Requires: xl2tpd
Requires: openswan

%filter_provides_in %{_libdir}/pppd/%{ppp_version}/nm-l2tp-pppd-plugin.so
%filter_provides_in %{_libdir}/NetworkManager/lib*.so

%description
This package contains software for integrating L2TP VPN support with
the NetworkManager and the GNOME desktop.

%prep
%setup -q

%build
./autogen.sh
%configure \
    --disable-static \
    --enable-more-warnings=yes \
    --with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version}

make %{?_smp_mflags}

%install

make install DESTDIR=%{buildroot} INSTALL="/usr/bin/install -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a

rm -f %{buildroot}%{_libdir}/pppd/%{ppp_version}/nm-l2tp-pppd-plugin.la
rm -f %{buildroot}%{_libdir}/pppd/%{ppp_version}/nm-l2tp-pppd-plugin.a

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/nm-l2tp-service.conf
# Content must not be changed
%config %{_sysconfdir}/NetworkManager/VPN/nm-l2tp-service.name
%{_libdir}/NetworkManager/lib*.so
%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.so
%{_libexecdir}/nm-l2tp-auth-dialog
%{_libexecdir}/nm-l2tp-service
%{_datadir}/gnome-vpn-properties/l2tp

%changelog
* Wed Nov 18 2015 Cjacker <cjacker@foxmail.com> - 0.9.8.7-7
- Rebuild

* Wed Nov 18 2015 Cjacker <cjacker@foxmail.com> - 0.9.8.7-6
- Rebuild

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.9.8.7-5
- Rebuild for new 4.0 release.

