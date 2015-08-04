Summary: Interfaces for accessibility support.
Name: atk
Version: 2.16.0
Release: 1
License: LGPL
Group: System Environment/Libraries
Source: atk-%{version}.tar.xz
URL: http://developer.gnome.org/projects/gap/
BuildPreReq: glib2-devel
BuildRequires:gobject-introspection-devel
%description
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits. By
supporting the ATK interfaces, an application or toolkit can be used
with tools such as screen readers, magnifiers, and alternative input
devices.

%package devel
Summary: System for layout and rendering of internationalized text.
Group: Development/Libraries
Requires: atk = %{version}
Requires: glib2-devel

%description devel
The atk-devel package includes the static libraries, header files, and
developer docs for the atk package.

Install atk-devel if you want to develop programs which will use ATK.

%prep
%setup -q

%build
%configure --disable-gtk-doc
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall


rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-, root, root)
%{_libdir}/libatk*.so.*
%{_datadir}/locale
%{_libdir}/girepository-?.?/*.typelib

%files devel
%defattr(-, root, root)
%{_libdir}/libatk*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/
%{_datadir}/gir-?.?/*.gir

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

