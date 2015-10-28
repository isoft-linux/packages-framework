# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           libsigc++
Version:        2.6.1
Release:        2 
Summary:        Typesafe signal framework for C++

License:        LGPLv2+
URL:            http://libsigc.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{release_version}/libsigc++-%{version}.tar.xz

BuildRequires:  m4

%description
This library implements a full callback system for use in widget libraries,
abstract interfaces, and general programming. Originally part of the Gtk--
widget set, libsigc++ is now a separate library to provide for more general
use. It is the most complete library of its kind with the ability to connect
an abstract callback to a class method, function, or function object. It
contains adaptor classes for connection of dissimilar callbacks and has an
ease of use unmatched by other C++ callback libraries.

Package GTK-- (gtkmm), which is a C++ binding to the GTK+ library,
starting with version 1.1.2, uses libsigc++.


%package devel
Summary:        Development tools for the typesafe signal framework for C++
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains the static libraries and header files
needed for development with %{name}.


%package        doc
Summary:        Documentation for %{name}, includes full API docs
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains the full API documentation for %{name}.


%prep
%setup -q -n libsigc++-%{version}


%build
%configure %{!?_with_static: --disable-static}
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README NEWS ChangeLog
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/sigc++-2.0/
%{_libdir}/pkgconfig/*.pc
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so

%files doc
%doc %{_datadir}/doc/libsigc++-2.0/
# according guidelines, we can co-own this, since devhelp is not required
# for accessing documentation
%doc %{_datadir}/devhelp/


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.6.1-2
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 2.6.1

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

