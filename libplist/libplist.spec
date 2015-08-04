%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:          libplist
Version:       1.12
Release:       5
Summary:       Library for manipulating Apple Binary and XML Property Lists

Group:         System Environment/Libraries
License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
BuildRequires: libxml2-devel
BuildRequires: python-devel
BuildRequires: swig
BuildRequires: cmake

%description
libplist is a library for manipulating Apple Binary and XML Property Lists

%package devel
Summary: Development package for libplist
Group: Development/Libraries
Requires: libplist = %{version}-%{release}
Requires: pkgconfig

%description devel
%{name}, development headers and libraries.

#%package python
#Summary: Python package for libplist
#Group: Development/Libraries
#Requires: libplist = %{version}-%{release}
#Requires: python
#
#%description python
#%{name}, python libraries and support

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LESSER README
%{_bindir}/plistutil
%{_libdir}/libplist.so.*
%{_libdir}/libplist++.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libplist.pc
%{_libdir}/pkgconfig/libplist++.pc
%{_libdir}/libplist.so
%{_libdir}/libplist++.so
%{_includedir}/plist

#%files python
#%defattr(-,root,root,-)
#%{python_sitearch}/plist*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

