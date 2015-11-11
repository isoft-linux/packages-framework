Name:           accountsservice
Version:        0.6.40
Release:        5
Summary:        D-Bus interfaces for querying and manipulating user account information

License:        GPLv3+
URL:            http://www.freedesktop.org/wiki/Software/AccountsService/
#VCS: git:git://git.freedesktop.org/accountsservice
Source0:        http://www.freedesktop.org/software/accountsservice/accountsservice-%{version}.tar.xz

# Autologin for sddm 
Patch0: 0001-sddm-autologin.patch
# Administrator group set as firstboot
Patch1: 0002-admin-group.patch

BuildRequires:  glib2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  polkit-devel
BuildRequires:  intltool
BuildRequires:  systemd-units
BuildRequires:  systemd-devel
BuildRequires:  gobject-introspection-devel

Requires:       polkit
Requires:       shadow-utils

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%package libs
Summary: Client-side library to talk to accountsservice
Requires: %{name} = %{version}-%{release}

%description libs
The accountsservice-libs package contains a library that can
be used by applications that want to interact with the accountsservice
daemon.


%package devel
Summary: Development files for accountsservice-libs
Requires: %{name}-libs = %{version}-%{release}

%description devel
The accountsservice-devel package contains headers and other
files needed to build applications that use accountsservice-libs.


%description
The accountsservice project provides a set of D-Bus interfaces for
querying and manipulating user account information and an implementation
of these interfaces, based on the useradd, usermod and userdel commands.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a

%find_lang accounts-service


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post
%systemd_post accounts-daemon.service

%preun
%systemd_preun accounts-daemon.service

%postun
%systemd_postun accounts-daemon.service

%files -f accounts-service.lang
%defattr(-,root,root,-)
%doc COPYING README AUTHORS
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Accounts.conf
%{_libexecdir}/accounts-daemon
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.User.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Accounts.service
%{_datadir}/polkit-1/actions/org.freedesktop.accounts.policy
%dir %{_localstatedir}/lib/AccountsService/
%dir %{_localstatedir}/lib/AccountsService/users
%dir %{_localstatedir}/lib/AccountsService/icons
%{_unitdir}/accounts-daemon.service

%files libs
%{_libdir}/libaccountsservice.so.*
%{_libdir}/girepository-1.0/AccountsService-1.0.typelib

%files devel
%{_includedir}/accountsservice-1.0
%{_libdir}/libaccountsservice.so
%{_libdir}/pkgconfig/accountsservice.pc
%{_datadir}/gir-1.0/AccountsService-1.0.gir
%dir %{_datadir}/gtk-doc/html/libaccountsservice
%{_datadir}/gtk-doc/html/libaccountsservice/*

%changelog
* Wed Nov 11 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Administrator group set as firstboot.

* Mon Nov 09 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Add autologin for sddm. 

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.6.40-3
- Rebuild for new 4.0 release.

