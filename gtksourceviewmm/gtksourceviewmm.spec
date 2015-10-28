%define apiver 3.0
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           gtksourceviewmm 
Version:        3.12.0
Release:        2 
Summary:        C++ interface for GtkSourceView 

License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gtksourceviewmm/%{release_version}/%{name}-%{version}.tar.xz

BuildRequires:  glibmm-devel >= 2.14.1
BuildRequires:  cairomm-devel >= 1.2.2
BuildRequires:  pango-devel >= 1.23.0
BuildRequires:  gtkmm-devel >= 3.2.0
BuildRequires:  doxygen


%description
gtksourceviewmm provides a C++ interface to the GtkSourceView library.


%package devel
Summary:        Headers for developing programs that will use %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       gtkmm-devel >= 3.2.0

%description devel
This package contains the libraries and header files needed for
developing %{name} applications.


%package          doc
Summary:          Developer's documentation for the %{name} library
BuildArch:        noarch
Requires:         %{name} = %{version}-%{release}
Requires:         libsigc++-doc
Requires:         glibmm-doc
Requires:         gtkmm-doc

%description      doc
This package contains developer's documentation for the %{name} library.

%prep
%setup -q


%build
export CC=cc
export CXX=c++
export CXXFLAGS="-std=c++11"

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
%{_includedir}/gtksourceviewmm-%{apiver}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/gtksourceviewmm-%{apiver}

%files doc
%doc %{_docdir}/gtksourceviewmm-%{apiver}/
%{_datadir}/devhelp/

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.12.0-2
- Rebuild for new 4.0 release.

