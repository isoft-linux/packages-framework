Summary: NetworkManager VPN plugin for iodine
Name: NetworkManager-iodine
Version: 0.0.5 
Release: 3%{?dist}
License: GPLv2+
URL: https://honk.sigxcpu.org/piki/projects/network-manager-iodine
Source0: http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.0/%{name}-%{version}.tar.xz

BuildRequires: gtk3-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: glib2-devel
BuildRequires: libtool intltool gettext
BuildRequires: libnm-gtk-devel >= 0.9.9.0
BuildRequires: libsecret-devel
Requires: shared-mime-info
Requires: iodine-client
Requires: dbus
Requires: NetworkManager

%global _privatelibs libnm-iodine-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the iodine server and NetworkManager.

%package -n NetworkManager-iodine-gnome
Summary: NetworkManager VPN plugin for iodine - GNOME files
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: network-manager-applet 

%description -n NetworkManager-iodine-gnome
This package contains software for integrating VPN capabilities with
the iodine server and NetworkManager (GNOME files).

%prep
%setup -q

%build
%configure --disable-static --enable-more-warnings=yes
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" install

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la

%find_lang %{name}

%files -f %{name}.lang
%{_sysconfdir}/dbus-1/system.d/nm-iodine-service.conf
%{_libexecdir}/nm-iodine-service
%{_libexecdir}/nm-iodine-auth-dialog
%doc AUTHORS NEWS
%license COPYING

%files -n NetworkManager-iodine-gnome
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/iodine
%{_datadir}/gnome-vpn-properties/iodine/nm-iodine-dialog.ui
%{_sysconfdir}/NetworkManager/VPN/nm-iodine-service.name

%changelog
* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 0.0.5-3
- Rebuild

* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 0.0.5-2
- Initial build

