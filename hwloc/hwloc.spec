Name:		hwloc
Version:	1.11.0
Release:	2
Summary:	Portable Hardware Locality

License:    BSD	
URL:		http://www.open-mpi.org/projects/hwloc/
Source0:	%{name}-%{version}.tar.bz2

%description
The Portable Hardware Locality (hwloc) software package provides a portable abstraction (across OS, versions, architectures, ...) of the hierarchical topology of modern architectures, including NUMA memory nodes, sockets, shared caches, cores and simultaneous multithreading. It also gathers various system attributes such as cache and memory information as well as the locality of I/O devices such as network interfaces, InfiniBand HCAs or GPUs. It primarily aims at helping applications with gathering information about modern computing hardware so as to exploit it accordingly and efficiently.


%package -n libhwloc-devel
Summary:        Development files for %{name}
Requires:       libhwloc = %{version}-%{release}

%description -n libhwloc-devel
This package contains the header files, static libraries and development
documentation for %{name}.

%package -n libhwloc
Summary:        libraries  for %{name}.

%description -n libhwloc
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%post -n libhwloc -p /sbin/ldconfig

%postun -n libhwloc -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_datadir}/hwloc/
%exclude %{_datadir}/doc/hwloc/

%files -n libhwloc
%defattr(-,root,root,-)
%{_libdir}/libhwloc.so.*

%files -n libhwloc-devel
%defattr(-,root,root,-)
%{_mandir}/man3/HWLOC_*.3*
%{_mandir}/man3/hwloc_*.3*
%{_mandir}/man3/hwlocality_*.3*
%{_includedir}/hwloc/
%{_includedir}/hwloc.h
%{_libdir}/libhwloc.so
%{_libdir}/pkgconfig/hwloc.pc



%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.11.0-2
- Rebuild for new 4.0 release.


