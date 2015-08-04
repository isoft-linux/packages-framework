Name:          libideviceactivation 
Version:       1.0.0
Release:       5
Summary:       A library to manage the activation process of Apple iOS devices.

Group:         System Environment/Libraries
License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
BuildRequires: libxml2-devel
BuildRequires: python-devel
BuildRequires: libplist-devel, libimobiledevice-devel
%description
A library to manage the activation process of Apple iOS devices.

%package devel
Summary: Development package for %{name} 
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
%{name}, development headers and libraries.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a
rpmclean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/ideviceactivation
%{_libdir}/libideviceactivation.so.*
%{_mandir}/man1/ideviceactivation.1.gz


%files devel
%defattr(-,root,root,-)
%{_libdir}/libideviceactivation.so
%{_libdir}/pkgconfig/libideviceactivation-1.0.pc
%{_includedir}/libideviceactivation.h

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

