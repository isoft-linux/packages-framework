%global gitrev 99edb54e18f4971f50a359803633f44fdeb08428
%{!?ruby_vendorarch: %global ruby_vendorarch %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"] ')}
%filter_provides_in %{perl_vendorarch}/.*\.so$
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{ruby_vendorarch}/.*\.so$
%filter_setup

Name:		libsolv
Version:	0.6.10
Release:	3
License:	BSD
Url:		https://github.com/openSUSE/libsolv
Source:		https://github.com/openSUSE/libsolv/archive/%{gitrev}.tar.gz
Patch0:		libsolv-rubyinclude.patch
Patch1:		libsolv-ruby22-rbconfig.patch
Group:		Development/Libraries
Summary:	Package dependency solver
BuildRequires:	cmake libdb-devel expat-devel librpm-devel zlib-devel
BuildRequires:	swig perl perl-devel ruby ruby-devel python-devel
BuildRequires:  xz-devel
%description
A free package dependency solver using a satisfiability algorithm. The
library is based on two major, but independent, blocks:

- Using a dictionary approach to store and retrieve package
  and dependency information.

- Using satisfiability, a well known and researched topic, for
  resolving package dependencies.

%package devel
Summary:	A new approach to package dependency solving
Group:		Development/Libraries
Requires:	libsolv-tools%{?_isa} = %{version}-%{release}
Requires:	libsolv%{?_isa} = %{version}-%{release}
Requires:	librpm-devel%{?_isa}
Requires:	cmake

%description devel
Development files for libsolv,

%package tools
Summary:	A new approach to package dependency solving
Group:		Development/Libraries
Requires:	gzip bzip2 coreutils
Requires:	libsolv%{?_isa} = %{version}-%{release}

%description tools
Package dependency solver tools.

%package demo
Summary:	Applications demoing the libsolv library
Group:		Development/Libraries
Requires:	curl gnupg2

%description demo
Applications demoing the libsolv library.

%package -n ruby-solv
Summary:	Ruby bindings for the libsolv library
Group:		Development/Languages

%description -n ruby-solv
Ruby bindings for sat solver.

%package -n python-solv
Summary:	Python bindings for the libsolv library
Group:		Development/Languages
Requires:	python

%description -n python-solv
Python bindings for sat solver.

%package -n perl-solv
Summary:	Perl bindings for the libsolv library
Group:		Development/Languages
Requires:	perl

%description -n perl-solv
Perl bindings for sat solver.

%prep
%setup -q -n libsolv-%{gitrev}
%patch0 -p1 -b .rubyinclude
%patch1 -p1 -b .ruby-rbconfig

%check
make ARGS="-V" test

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DENABLE_PERL=1 \
       -DENABLE_PYTHON=1 \
       -DPYTHON_EXECUTABLE=python3 \
       -DENABLE_RUBY=1 \
       -DUSE_VENDORDIRS=1 \
       -DFEDORA=1 \
       -DENABLE_DEBIAN=1 \
       -DENABLE_ARCHREPO=1 \
       -DENABLE_LZMA_COMPRESSION=1 \
       -DMULTI_SEMANTICS=1

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT/usr/bin/testsolv

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE* README BUGS
/usr/lib64/libsolv.so.*
/usr/lib64/libsolvext.so.*

%files tools
%_bindir/archpkgs2solv
%_bindir/archrepo2solv
%_bindir/deb2solv
%_bindir/deltainfoxml2solv
%_bindir/dumpsolv
%_bindir/installcheck
%_bindir/mergesolv
%_bindir/repo2solv.sh
%_bindir/repomdxml2solv
%_bindir/rpmdb2solv
%_bindir/rpmmd2solv
%_bindir/rpms2solv
%_bindir/updateinfoxml2solv

%files devel
%doc examples/solv.c
/usr/lib64/libsolv.so
/usr/lib64/libsolvext.so
%_includedir/solv
%_datadir/cmake/Modules/FindLibSolv.cmake
%{_mandir}/man?/*

%files demo
%_bindir/solv

%files -n perl-solv
%doc examples/p5solv
%{perl_vendorarch}/*

%files -n ruby-solv
%doc examples/rbsolv
%{ruby_vendorarch}/*

%files -n python-solv
%doc examples/pysolv
/usr/lib/python3.4/site-packages/*

%changelog
