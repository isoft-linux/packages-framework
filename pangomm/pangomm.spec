%define apiver 1.4
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           pangomm
Version:        2.38.1
Release:        2 
Summary:        C++ interface for Pango

License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/pangomm/%{release_version}/%{name}-%{version}.tar.xz

BuildRequires:  glibmm-devel >= 2.14.1
BuildRequires:  cairomm-devel >= 1.2.2
BuildRequires:  pango-devel >= 1.23.0
BuildRequires:  doxygen


%description
pangomm provides a C++ interface to the Pango library. Highlights
include typesafe callbacks, widgets extensible via inheritance and a
comprehensive set of widget classes that can be freely combined to
quickly create complex user interfaces.


%package devel
Summary:        Headers for developing programs that will use %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the libraries and header files needed for
developing pangomm applications.


%package          doc
Summary:          Developer's documentation for the pangomm library
BuildArch:        noarch
Requires:         %{name} = %{version}-%{release}
Requires:         libsigc++-doc
Requires:         glibmm-doc

%description      doc
This package contains developer's documentation for the pangomm
library. Pangomm is the C++ API for the Pango font layout library.

The documentation can be viewed either through the devhelp
documentation browser or through a web browser.

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/*.so.*


%files devel
%{_includedir}/pangomm-%{apiver}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/pangomm-%{apiver}

%files doc
%doc %{_docdir}/pangomm-%{apiver}/
%{_datadir}/devhelp/

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.38.1-2
- Rebuild for new 4.0 release.

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

