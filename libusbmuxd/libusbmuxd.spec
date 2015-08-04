Name:          libusbmuxd
Version:       1.0.10
Release:       5
Summary:       A client library to multiplex connections from and to iOS devices

Group:         System Environment/Libraries
License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
BuildRequires: libxml2-devel
BuildRequires: python-devel
BuildRequires: swig
BuildRequires: cmake

%description
A client library to multiplex connections from and to iOS devices by connecting to a socket provided by a usbmuxd daemon.

%package devel
Summary: Development package for %{name} 
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
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

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/iproxy
%{_libdir}/libusbmuxd.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libusbmuxd.pc
%{_libdir}/libusbmuxd.so
%{_includedir}/*.h

#%files python
#%defattr(-,root,root,-)
#%{python_sitearch}/plist*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.
