Name: LibRaw 
Version: 0.17.0
Release: 2
Summary: Raw image decoder

License: GPL
URL: http://www.libraw.org/
Source0: http://www.libraw.org/data/%{name}-%{version}.tar.gz
BuildRequires: lcms2-devel, libjpeg-turbo-devel, jasper-devel
BuildRequires: libgomp, libstdc++-devel

%description
LibRaw is a library for reading RAW files obtained from digital photo cameras
include (CRW/CR2, NEF, RAF, DNG, and others). 

LibRaw is based on the source codes of the dcraw utility.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -rf $RPM_BUILD_ROOT/%{_docdir}/libraw

%files
%{_bindir}/*
%{_libdir}/libraw.so.*
%{_libdir}/libraw_r.so.*

%files devel
%{_includedir}/libraw
%{_libdir}/libraw.a
%{_libdir}/libraw_r.a
%{_libdir}/libraw.so
%{_libdir}/libraw_r.so
%{_libdir}/pkgconfig/libraw.pc
%{_libdir}/pkgconfig/libraw_r.pc

%changelog
* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com> - 0.17.0-2
- update.
