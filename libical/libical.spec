Summary:	Reference implementation of the iCalendar data type and serialization format
Name:		libical
Version:    2.0.0
Release:	1
License:	LGPLv2 or MPLv1.1
URL:		http://freeassociation.sourceforge.net/
Source:		http://downloads.sourceforge.net/freeassociation/%{name}-%{version}.tar.gz
Requires:	tzdata
BuildRequires:	bison, byacc, flex, cmake
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Reference implementation of the iCalendar data type and serialization format
used in dozens of calendaring and scheduling products.

%package devel
Summary:	Development files for libical
Requires:	%{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The libical-devel package contains libraries and header files for developing 
applications that use libical.

%prep
%setup -q

%build
mkdir %{_target} && cd %{_target}
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make %{?_smp_mflags}
cd -

%install
rm -rf $RPM_BUILD_ROOT
cd %{_target}
%{make_install}
cd -

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/%{name}.so.*
%{_libdir}/libicalss.so.*
%{_libdir}/libicalvcal.so.*
%{_libdir}/libical_cxx.so.*
%{_libdir}/libicalss_cxx.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/UsingLibical.txt
%{_libdir}/%{name}.so
%{_libdir}/libicalss.so
%{_libdir}/libicalvcal.so
%{_libdir}/libical.a
%{_libdir}/libical_cxx.a
%{_libdir}/libical_cxx.so
%{_libdir}/libicalss.a
%{_libdir}/libicalss_cxx.a
%{_libdir}/libicalss_cxx.so
%{_libdir}/libicalvcal.a
%{_libdir}/pkgconfig/libical.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/cmake/LibIcal/*.cmake

%changelog
* Tue Jan 17 2017 sulit - 2.0.0-1
- upgrade libical to 2.0.0

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0-5
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

