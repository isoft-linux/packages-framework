%global apiver 1.6
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           atkmm
Version:        2.22.7
Release:        1 
Summary:        C++ interface for the ATK library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/atkmm/%{release_version}/atkmm-%{version}.tar.xz

BuildRequires:  atk-devel
BuildRequires:  glibmm-devel

# atkmm was split out into a separate package in gtkmm 2.21.1
Conflicts:      gtkmm < 2.21.1

%description
atkmm provides a C++ interface for the ATK library. Highlights
include typesafe callbacks, widgets extensible via inheritance and a
comprehensive set of widget classes that can be freely combined to
quickly create complex user interfaces.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Conflicts:      gtkmm-devel < 2.21.1

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Developer's documentation for the atkmm library
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       glibmm-doc

%description    doc
This package contains developer's documentation for the atkmm
library. Atkmm is the C++ API for the ATK accessibility toolkit library.

The documentation can be viewed either through the devhelp
documentation browser or through a web browser.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rpmclean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/atkmm-%{apiver}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/atkmm-%{apiver}/

%files doc
%doc %{_docdir}/atkmm-%{apiver}/
%doc %{_datadir}/devhelp/


%changelog
