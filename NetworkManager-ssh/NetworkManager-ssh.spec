%global commit 60f03fefe3fdce4cef9cf35eec9e6ca1bc61af41
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global checkout 20150713git%{shortcommit}

Summary: NetworkManager VPN plugin for SSH
Name: NetworkManager-ssh
Version: 0.9.4
Release: 0.3.%{checkout}%{?dist}
License: GPLv2+
URL: https://github.com/danfruehauf/NetworkManager-ssh
Source0: https://github.com/danfruehauf/NetworkManager-ssh/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires: autoconf
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: glib2-devel
BuildRequires: libtool intltool gettext
BuildRequires: libnm-gtk-devel >= 0.9.10
BuildRequires: libsecret-devel
BuildRequires: libtool intltool gettext
Requires: gtk3
Requires: dbus
Requires: NetworkManager
Requires: openssh-clients
Requires: shared-mime-info
Requires: sshpass

%global _privatelibs libnm-ssh-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the OpenSSH server with NetworkManager.

%package -n NetworkManager-ssh-gnome
Summary: NetworkManager VPN plugin for SSH - GNOME files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: network-manager-applet

%description -n NetworkManager-ssh-gnome
This package contains software for integrating VPN capabilities with
the OpenSSH server with NetworkManager (GNOME files).

%prep
%setup -q -n %{name}-%{commit}

%build
if [ ! -f configure ]; then
  autoreconf -fvi
fi
CFLAGS="$RPM_OPT_FLAGS -Wno-deprecated-declarations" \
	%configure --disable-static --disable-dependency-tracking --enable-more-warnings=yes --with-gtkver=3
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" install

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS README ChangeLog
%{_sysconfdir}/dbus-1/system.d/nm-ssh-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-ssh-service.name
%{_libexecdir}/nm-ssh-service
%{_libexecdir}/nm-ssh-auth-dialog

%files -n NetworkManager-ssh-gnome
%doc COPYING AUTHORS README ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/ssh
%{_datadir}/gnome-vpn-properties/ssh/nm-ssh-dialog.ui

%changelog
* Wed Nov 18 2015 Cjacker <cjacker@foxmail.com> - 0.9.4-0.3.20150713git60f03fe
- Rebuild

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.9.4-0.2.20150713git60f03fe
- Rebuild for new 4.0 release.

