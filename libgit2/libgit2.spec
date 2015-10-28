Name: libgit2
Version: 0.23.2
Release: 5
Summary: A C implementation of the Git core methods as a library

License: GPLv2 with exceptions
URL: http://libgit2.github.com/
Source0: %{name}-%{version}.tar.gz

BuildRequires: cmake >= 2.6
BuildRequires: libssh2-devel
BuildRequires: openssl-devel
BuildRequires: python
BuildRequires: zlib-devel

Provides: bundled(libxdiff)

%description
libgit2 is a portable, pure C implementation of the Git core methods 
provided as a re-entrant linkable library with a solid API, allowing
you to write native speed custom Git applications in any language
with bindings.


%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

# Fix pkgconfig generation
sed -i 's|@CMAKE_INSTALL_PREFIX@/||' libgit2.pc.in

# Don't test network
sed -i 's/ionline/xonline/' CMakeLists.txt

%build
%cmake -DTHREADSAFE:BOOL=1 .
make %{_smp_mflags}

%check
make test

%install
make install DESTDIR=%{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc README.md COPYING AUTHORS
%{_libdir}/libgit2.so.*


%files devel
%doc docs examples
%{_libdir}/libgit2.so
%{_libdir}/pkgconfig/libgit2.pc
%{_includedir}/git2*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.23.2-5
- Rebuild for new 4.0 release.

* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- update to 0.23.2
