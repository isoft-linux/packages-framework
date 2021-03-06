%define dbus_version            0.90
%define dbus_glib_version       0.70
%define glib2_version           2.26.0

Summary: Desktop notification library
Name: libnotify
Version: 0.7.6
Release: 7 
URL: http://www.gnome.org
Source0: http://ftp.gnome.org/pub/GNOME/sources/libnotify/0.7/%{name}-%{version}.tar.xz
Patch0: libnotify-disable-test-depend-on-gtk3.patch
License: LGPLv2+
BuildRequires: libtool
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gdk-pixbuf2-devel
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: gobject-introspection-devel
Requires: glib2 >= %{glib2_version}

%description
libnotify is a library for sending desktop notifications to a notification
daemon, as defined in the freedesktop.org Desktop Notifications spec. These
notifications can be used to inform the user about an event or display some
form of information without getting in the user's way.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel >= %{glib2_version}
Requires:       dbus-devel >= %{dbus_version}
Requires:       dbus-glib-devel >= %{dbus_glib_version}
Requires:       pkgconfig

%description devel
This package contains libraries and header files needed for
development of programs using %{name}.

%prep
%setup -q
%patch0 -p1

%build
autoreconf -ivf
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING NEWS AUTHORS

%{_bindir}/notify-send
%{_libdir}/libnotify.so.*
%{_libdir}/girepository-1.0/Notify-0.7.typelib

%files devel
%dir %{_includedir}/libnotify
%{_includedir}/libnotify/*
%{_libdir}/libnotify.so
%{_libdir}/pkgconfig/libnotify.pc
%dir %{_datadir}/gtk-doc/html/libnotify
%{_datadir}/gtk-doc/html/libnotify/*
%{_datadir}/gir-1.0/Notify-0.7.gir

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.7.6-7
- Rebuild for new 4.0 release.

