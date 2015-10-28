Name:                   libconfig
Summary:                C/C++ configuration file library
Version:                1.5
Release:                3%{?dist}
License:                LGPLv2+
Source0:                http://www.hyperrealm.com/libconfig/libconfig-%{version}.tar.gz
URL:                    http://www.hyperrealm.com/libconfig/
BuildRequires:		bison, flex

%description
Libconfig is a simple library for manipulating structured configuration
files. This file format is more compact and more readable than XML. And
unlike XML, it is type-aware, so it is not necessary to do string parsing
in application code.

%package devel
Summary:                Development files for libconfig
Requires:               %{name} = %{version}-%{release}
Requires:               pkgconfig

%description devel
Development libraries and headers for developing software against
libconfig.

%prep
%setup -q
iconv -f iso-8859-1 -t utf-8 -o AUTHORS{.utf8,}
mv AUTHORS{.utf8,}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_infodir}

%check
./tests/libconfig_tests

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libconfig*.so.*

%files devel
%{_includedir}/libconfig*
%{_libdir}/libconfig*.so
%{_libdir}/pkgconfig/libconfig*.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.5-3
- Rebuild for new 4.0 release.

