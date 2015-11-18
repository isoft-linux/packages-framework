%global snapshot %{nil}

Summary:   NetworkManager VPN plugin for vpnc
Name:      NetworkManager-vpnc
Epoch:     1
Version:   1.0.2
Release:   4%{snapshot}%{?dist}
License:   GPLv2+
URL:       http://www.gnome.org/projects/NetworkManager/
Source0:   https://download.gnome.org/sources/NetworkManager-vpnc/1.0/%{name}-%{version}%{snapshot}.tar.xz

BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel >= 1:0.9.9.0
BuildRequires: intltool gettext
BuildRequires: libnm-gtk-devel >= 0.9.9.0
BuildRequires: libsecret-devel

Requires: gtk3
Requires: dbus
Requires: NetworkManager >= 1:0.9.9.0
Requires: vpnc
Requires: shared-mime-info
Requires: gnome-keyring
Obsoletes: NetworkManager-vpnc < 1:0.9.8.2-2

%global _privatelibs libnm-vpnc-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the vpnc server with NetworkManager.

%package -n NetworkManager-vpnc-gnome
Summary: NetworkManager VPN plugin for vpnc - GNOME files

Requires: NetworkManager-vpnc = %{epoch}:%{version}-%{release}
Requires: network-manager-applet 
Obsoletes: NetworkManager-vpnc < 1:0.9.8.2-2

%description -n NetworkManager-vpnc-gnome
This package contains software for integrating VPN capabilities with
the vpnc server with NetworkManager (GNOME files).

%prep
%setup -q -n %{name}-%{version}


%build
export CFLAGS="$RPM_OPT_FLAGS -Wno-error=deprecated-declarations"
%configure --enable-more-warnings=yes --with-gtkver=3 --with-tests=yes
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a

%find_lang %{name}


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang

%doc AUTHORS ChangeLog
%{_libexecdir}/nm-vpnc-auth-dialog
%{_sysconfdir}/dbus-1/system.d/nm-vpnc-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-vpnc-service.name
%{_libexecdir}/nm-vpnc-service
%{_libexecdir}/nm-vpnc-service-vpnc-helper
%{_datadir}/applications/nm-vpnc-auth-dialog.desktop
%{_datadir}/icons/hicolor/48x48/apps/gnome-mime-application-x-cisco-vpn-settings.png

%files -n NetworkManager-vpnc-gnome
%doc AUTHORS ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/vpnc
%{_datadir}/gnome-vpn-properties/vpnc/nm-vpnc-dialog.ui

%changelog
* Wed Nov 18 2015 Cjacker <cjacker@foxmail.com> - 1:1.0.2-4
- Rebuild

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:1.0.2-3
- Rebuild for new 4.0 release.

