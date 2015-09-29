Name:           libxspf
Version:        1.2.0
Release:        9%{?dist}
Summary:        XSPF playlist library

License:        BSD and LGPL
URL:            http://www.xiph.org/oggz/
Source0:        http://downloads.xiph.org/releases/libxspf/%{name}-%{version}.tar.bz2
Patch0:	libxspf-missing-header.patch

BuildRequires:  doxygen
BuildRequires:  docbook-utils
BuildRequires:  uriparser-devel
BuildRequires: cpptest-devel

%description
libxspf is a C++ library that can help your application
to read and write XSPF playlist files (both Version 0 and 1).

%package devel
Summary:	Files needed for development using libxspf 
Requires:       libxspf = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains the header files and documentation needed for
development using libxspf.

%package doc
Summary:        Documentation for libxspf
Requires:	libxspf = %{version}-%{release}

%description doc
This package contains HTML documentation needed for development using
libxspf.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%configure --disable-static
make %{?_smp_mflags}



%install
rm -rf $RPM_BUILD_ROOT
%makeinstall INSTALL="%{__install} -p"
pushd doc
./configure
make
popd

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

                                                                                
%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/lib*.so.*
%{_bindir}/xspf*

%files devel
%defattr(-,root,root)
%{_includedir}/xspf
%{_libdir}/libxspf.so
%{_libdir}/pkgconfig/xspf.pc

%files doc
%defattr(-,root,root)
%doc doc/html


%changelog
