#we only need major.minor in the SONAME in the stable (even numbered) series
#this should be changed to %%{version} in unstable (odd numbered) releases
%global sover 0.10

Name: libuv
Epoch:   1
Version: 1.4.0
Release: 2%{?dist}
Summary: Platform layer for node.js
# the licensing breakdown is described in detail in the LICENSE file
License: MIT and BSD and ISC
URL: http://libuv.org/
Source0: http://libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
Source2: libuv.pc.in

BuildRequires: autoconf automake libtool
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
libuv is a new platform layer for Node. Its purpose is to abstract IOCP on
Windows and libev on Unix systems. We intend to eventually contain all platform
differences in this library.

%package devel
Summary: Development libraries for libuv
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: pkgconfig
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description devel
Development libraries for libuv

%package static
Summary: Platform layer for node.js - static library
Requires:   %{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static library (.a) version of libuv.

%prep
%setup -q -n %{name}-v%{version}

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/libuv.la

%check
# Tests are currently disabled because some require network access
# Working with upstream to split these out
#./run-tests
#./run-benchmarks

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md AUTHORS LICENSE
%{_libdir}/libuv.so.*

%files devel
%doc README.md AUTHORS LICENSE
%{_libdir}/libuv.so
%{_libdir}/pkgconfig/libuv.pc
%{_includedir}/uv*.h

%files static
%{_libdir}/libuv.a

%changelog
