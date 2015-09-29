%define nm_version        0.9.9.95

%define realversion 1.0.2

Summary:   NetworkManager VPN plug-in for openswan and libreswan
Name:      NetworkManager-openswan
Version:   %{realversion}
Release:   2%{?dist}
License:   GPLv2+
Group:     System Environment/Base
URL:       https://download.gnome.org/sources/NetworkManager-openswan/1.0/
Source0:   https://download.gnome.org/sources/NetworkManager-openswan/1.0/%{name}-%{realversion}.tar.xz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: libnl3-devel
BuildRequires: NetworkManager-devel       >= 1:%{nm_version}
BuildRequires: NetworkManager-glib-devel  >= 1:%{nm_version}
BuildRequires: libnm-gtk-devel >= %{nm_version}
BuildRequires: libsecret-devel
BuildRequires: intltool gettext

Requires: NetworkManager   >= 1:%{nm_version}
Requires: gnome-keyring
Requires: gtk3
Requires: dbus
Requires: libreswan
Requires: shared-mime-info

%global _privatelibs libnm-openswan-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating the openswan/libreswan VPN software
with NetworkManager and the GNOME desktop

%package -n NetworkManager-openswan-gnome
Summary: NetworkManager VPN plugin for openswan/libreswan - GNOME files
Group:   System Environment/Base

Requires: NetworkManager-openswan = %{version}-%{release}
Requires: network-manager-applet 

%description -n NetworkManager-openswan-gnome
This package contains software for integrating VPN capabilities with
the openswan/libreswan server with NetworkManager (GNOME files).

%prep
%setup -q  -n NetworkManager-openswan-%{realversion}

%build
%configure --disable-static --enable-more-warnings=yes
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a
ln -sf %{_libexecdir}/nm-openswan-service-helper  %{buildroot}%{_libexecdir}/nm-libreswan-service-helper

%find_lang %{name}

%post
update-desktop-database &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root,-)
%doc AUTHORS ChangeLog COPYING
#%{_libdir}/NetworkManager/lib*.so*
%{_libexecdir}/nm-openswan-auth-dialog
%{_sysconfdir}/dbus-1/system.d/nm-openswan-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-openswan-service.name
%{_libexecdir}/nm-openswan-service
%{_libexecdir}/nm-openswan-service-helper
%{_libexecdir}/nm-libreswan-service-helper
%{_datadir}/applications/nm-openswan-auth-dialog.desktop

%files -n NetworkManager-openswan-gnome
%doc AUTHORS ChangeLog COPYING
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/openswan
%{_datadir}/gnome-vpn-properties/openswan/nm-openswan-dialog.ui


%changelog
