%define libxml2_version 2.4.12
%define orbit2_version 2.8.0    
%define glib2_version 2.2.0

Summary: A process-transparent configuration system
Name: GConf2
Version: 3.2.6 
Release: 1 
License: LGPL
Group: System Environment/Base
URL: http://www.gnome.org
Source: ftp://ftp.gnome.org/pub/GNOME/unstable/sources/GConf/GConf-%{version}.tar.xz
Patch0: 01_xml-gettext-domain.patch  
Patch1: gconf-reload.patch

BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk-doc >= 0.9
BuildRequires: pkgconfig >= 0.14
BuildRequires: gettext

%description
GConf is a process-transparent configuration database API used to 
store user preferences. It has pluggable backends and features to 
support workgroup administration.

%package devel
Summary: Headers and libraries for GConf development
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: libxml2-devel >= %{libxml2_version}
Requires: glib2-devel >= %{glib2_version}


%description devel
GConf development package. Contains files needed for doing
development using GConf.

%prep
%setup -q -n GConf-%{version}
%patch0 -p1
%patch1 -p1

%build
%configure \
    --disable-static \
    --enable-defaults-service \
    --disable-orbit \
    --without-openldap
make %{?_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang GConf2

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f GConf2.lang
%defattr(-, root, root)
%dir %{_sysconfdir}/gconf/2
%dir %{_sysconfdir}/gconf/gconf.xml.defaults
%dir %{_sysconfdir}/gconf/gconf.xml.mandatory
%config(noreplace) %{_sysconfdir}/gconf/2/path

%{_bindir}/*
%{_libdir}/libgconf-2.so.*

%{_datadir}/polkit-1/actions/org.gnome.gconf.defaults.policy
%{_libexecdir}/*
%dir %{_datadir}/sgml/gconf
%{_datadir}/sgml/gconf/gconf-1.0.dtd

%dir %{_libdir}/GConf
%dir %{_libdir}/GConf/2
%{_libdir}/GConf/2/*.so

%{_sysconfdir}/dbus-1/system.d/org.gnome.GConf.Defaults.conf
%{_datadir}/dbus-1/services/org.gnome.GConf.service
%{_datadir}/dbus-1/system-services/org.gnome.GConf.Defaults.service

%{_sysconfdir}/xdg/autostart/gsettings-data-convert.desktop
%{_libdir}/gio/modules/libgsettingsgconfbackend.so

%{_libdir}/girepository-?.?/*.typelib

%{_mandir}/man1/*


%files devel
%defattr(-, root, root)
%{_includedir}/gconf
%{_libdir}/libgconf-2.so
%{_libdir}/pkgconfig/gconf-2.0.pc
%{_datadir}/gir-?.?/*.gir
%{_datadir}/aclocal/gconf-2.m4
%{_datadir}/gtk-doc/html/gconf

%changelog
