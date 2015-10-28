Name: libguess
Version: 1.2
Release: 3%{?dist}

Summary: High-speed character set detection library
License: BSD
URL: http://rabbit.dereferenced.org/~nenolod/distfiles/
Source0: http://rabbit.dereferenced.org/~nenolod/distfiles/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig

%description
libguess employs discrete-finite automata to deduce the character set of
the input buffer. The advantage of this is that all character sets can be
checked in parallel, and quickly. Right now, libguess passes a byte to
each DFA on the same pass, meaning that the winning character set can be
deduced as efficiently as possible.

libguess is fully reentrant, using only local stack memory for DFA
operations.


%package devel
Summary: Files needed for developing with %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the files that are needed when building
software that uses %{name}.


%prep
%setup -q

sed -i '\,^.SILENT:,d' buildsys.mk.in


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"


%check
cd src/tests/testbench
LD_LIBRARY_PATH=${RPM_BUILD_ROOT}%{_libdir} make


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING README
%{_libdir}/%{name}.so.1
%{_libdir}/%{name}.so.1.*

%files devel
%{_libdir}/%{name}.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.2-3
- Rebuild for new 4.0 release.

