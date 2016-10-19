Summary: Soup, an HTTP library implementation
Name: libsoup
Version: 2.56.0
Release: 2
License: LGPL
Source0: ftp://ftp.gnome.org/pub/gnome/sources/libsoup/2.2/%{name}-%{version}.tar.xz
URL:  ftp://ftp.gnome.org/pub/gnome/sources/libsoup/

Patch0:  nocheck-digest-for-guest.patch
Patch1:  emit-signal-with-auth.patch

Requires: glib2 >= 2.0, libxml2, gnutls
Requires: glib-networking
BuildRequires: pkgconfig, gnutls-devel
BuildRequires: glib2-devel
BuildRequires: glib-networking
BuildRequires: intltool
BuildRequires: krb5-devel >= 1.11
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: vala-tools
BuildRequires: vala-devel
%description
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

%package devel
Summary: Header files for the Soup library
Requires: %{name} = %{version}
Requires: glib2-devel, libxml2-devel

%description devel
Libsoup is an HTTP library implementation in C. This package allows
you to develop applications that use the libsoup library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --disable-gtk-doc
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
%doc README COPYING NEWS AUTHORS
%{_libdir}/lib*.so.*
%{_libdir}/girepository-?.?/*.typelib

%files devel
%defattr(-, root, root)
%{_includedir}/%{name}-2.4
%{_includedir}/%{name}-gnome-2.4
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Soup*2.4.gir
%{_datadir}/gtk-doc/html/%{name}-2.4
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libsoup-2.4.deps
%{_datadir}/vala/vapi/libsoup-2.4.vapi

%changelog
* Wed Oct 19 2016 x <ming.wang@i-soft.com.cn> - 2.56.0-1
- Update to 2.56.0, release number 1. 
- Patch0: No check digest for guest.
- Patch1: Emit signal with auth information when got headers.

* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 2.52.2-2
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.52.1-3
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 2.52.1

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

