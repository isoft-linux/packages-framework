Summary: A library for interfacing IEEE 1284-compatible devices
Name: libieee1284
Version: 0.2.11
Release: 15
License: GPLv2+
Group: System Environment/Libraries
URL: http://cyberelk.net/tim/libieee1284/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch1: libieee1284-strict-aliasing.patch
Patch2: libieee1284-aarch64.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: xmlto, python-devel

%description
The libieee1284 library is for communicating with parallel port devices.

%package devel
Summary: Files for developing applications that use libieee1284
Requires: %{name} = %{version}-%{release}
Group: Development/Libraries

%description devel
The header files, static library, libtool library and man pages for
developing applications that use libieee1284.

%package python
Summary: Python extension module for libieee1284
Requires: %{name} = %{version}-%{release}
Group: System Environment/Libraries

%description python
Python extension module for libieee1284.  To use libieee1284 with Python,
use 'import ieee1284'.

%prep
%setup -q
# Fixed strict aliasing warnings (bug #605170).
%patch1 -p1 -b .strict-aliasing

# Add support for building on aarch64 (bug #925774).
%patch2 -p1 -b .aarch64

%build
touch doc/interface.xml
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install
rm -f %{buildroot}%{_libdir}/python*/*/*a
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README COPYING TODO AUTHORS NEWS
%{_libdir}/*.so.*
%{_bindir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/ieee1284.h
%{_libdir}/*.so
%{_mandir}/*/*

%files python
%defattr(-,root,root)
%{_libdir}/python*/*/*.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

