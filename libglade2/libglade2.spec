%define debug_package %{nil}
%define libxml2_version 2.4.12-0.7
%define gtk2_version 2.3.2
%define pango_version 1.3.2

Summary: The libglade library for loading user interfaces.
Name: libglade2
Version: 2.6.4
Release: 4 
License: LGPL
Source: libglade-%{version}.tar.bz2
Patch:  libglade-2.6.2-set-prop-for-tool-item.patch	
URL: http://www.gnome.org
Requires: libxml2 >= %{libxml2_version}
BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: fontconfig
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: libtool

# http://bugzilla.gnome.org/show_bug.cgi?id=121025

%description
Libglade is a small library that allows a program to load its user
interface from am XML description at runtime. Libglade uses the XML
file format used by the GLADE user interface builder GLADE, so
libglade acts as an alternative to GLADE's code generation
approach. Libglade also provides a simple interface for connecting
handlers to the various signals in the interface (on platforms where
the gmodule library works correctly, it is possible to connect all the
handlers with a single function call). Once the interface has been
instantiated, libglade gives no overhead, so other than the short
initial interface loading time, there is no performance tradeoff.

%package devel
Summary: The files needed for libglade application development.
Requires: %name = %{version}
Requires: libxml2-devel >= %{libxml2_version}
Requires: gtk2-devel >= %{gtk2_version}
Conflicts: libglade < 0.17

%description devel
The libglade-devel package contains the libraries and include files
that you can use to develop libglade applications.

%prep
%setup -q -n libglade-%{version}
%patch -p1

%build
%configure --disable-gtk-doc
make %{?_smp_mflags}

%install

rm -rf $RPM_BUILD_ROOT
%makeinstall

rm $RPM_BUILD_ROOT%{_libdir}/*.la
%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING
%{_libdir}/lib*.so.*
%{_datadir}/xml

%files devel
%defattr(-, root, root)
%doc test-libglade.c
%{_bindir}/*
%{_libdir}/lib*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gtk-doc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.6.4-4
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

