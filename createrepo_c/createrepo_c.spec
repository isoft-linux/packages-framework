%global gitrev a3aaa03
# gitrev is output of: git rev-parse --short HEAD

%define bash_completion %{_datadir}/bash-completion/completions/*

Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        0.9.0
Release:        5
License:        GPLv2
# Use the following commands to generate the tarball:
#  git clone https://github.com/Tojaj/createrepo_c.git
#  cd createrepo_c
#  utils/make_tarball.sh %{gitrev}
Source0:        createrepo_c-%{gitrev}.tar.xz
URL:            https://github.com/Tojaj/createrepo_c

BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  file-devel
BuildRequires:  glib2-devel >= 2.22.0
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python-sphinx
BuildRequires:  librpm-devel >= 4.8.0-28
BuildRequires:  sqlite-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
Requires:       %{name}-libs =  %{version}-%{release}
BuildRequires:  bash-completion
Requires: rpm >= 4.9.0
BuildRequires:  drpm >= 0.1.3

%description
C implementation of Createrepo.
A set of utilities (createrepo_c, mergerepo_c, modifyrepo_c)
for generating a common metadata repository from a directory of
rpm packages and maintaining it.

%package libs
Summary:    Library for repodata manipulation

%description libs
Libraries for applications using the createrepo_c library
for easy manipulation with a repodata.


%package devel
Summary:    Library for repodata manipulation
Requires:   pkgconfig >= 1:0.14
Requires:   %{name}-libs =  %{version}-%{release}

%description devel
This package contains the createrepo_c C library and header files.
These development files are for easy manipulation with a repodata.

%package -n python-createrepo_c
Summary:    Python bindings for the createrepo_c library
Requires:   %{name}-libs = %{version}-%{release}

%description -n python-createrepo_c
Python bindings for the createrepo_c library.

%prep
%setup -q -n createrepo_c

%build
%cmake .
make %{?_smp_mflags} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
make doc-c

%check
make tests
make ARGS="-V" test

%install
make install DESTDIR=$RPM_BUILD_ROOT/

%post -n %{name}-libs -p /sbin/ldconfig

%postun -n %{name}-libs -p /sbin/ldconfig

%files
%doc README.md
%doc COPYING
%_mandir/man8/createrepo_c.8.*
%_mandir/man8/mergerepo_c.8.*
%_mandir/man8/modifyrepo_c.8.*
%_mandir/man8/sqliterepo_c.8.*
%{bash_completion}
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c
%{_bindir}/modifyrepo_c
%{_bindir}/sqliterepo_c

%files libs
%doc COPYING
# %{_libdir}/libcreaterepo_c.so.*
/usr/lib64/libcreaterepo_c.so.*

%files devel
# %{_libdir}/libcreaterepo_c.so
# %{_libdir}/pkgconfig/createrepo_c.pc
/usr/lib64/libcreaterepo_c.so
/usr/lib64/pkgconfig/createrepo_c.pc
%{_includedir}/createrepo_c/*
%doc COPYING
%doc doc/html

%files -n python-createrepo_c
%{python_sitearch}/createrepo_c/

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.9.0-5
- Rebuild for new 4.0 release.

