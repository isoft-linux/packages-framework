Name: libndp
Version: 1.5
Release: 3
Summary: Library for Neighbor Discovery Protocol
License: LGPLv2+
URL: http://www.libndp.org/
Source: http://www.libndp.org/files/libndp-%{version}.tar.gz

Patch1: libndp-remove-utils.patch

%description
This package contains a library which provides a wrapper
for IPv6 Neighbor Discovery Protocol.  It also provides a tool
named ndptool for sending and receiving NDP messages.

%package devel
Summary: Libraries and header files for libndp development
Requires: libndp = %{version}-%{release}

%description devel
The libndp-devel package contains the header files and libraries
necessary for developing programs using libndp.

%prep
%setup -q
%patch1 -p1

%build
autoreconf -ivf
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/*so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.5-3
- Rebuild for new 4.0 release.

