%global major_version 1.10

Name:           botan
Version:        %{major_version}.9
Release:        9%{?dist}
Summary:        Crypto library written in C++

License:        BSD
URL:            http://botan.randombit.net/
Source0:        http://botan.randombit.net/releases/Botan-%{version}.tgz
Patch0:         botan-aarch64.patch
Patch1:         botan-1.10-add-ppc64le.patch

BuildRequires:  gcc
BuildRequires:  python
BuildRequires:  python-sphinx
BuildRequires:  python-devel
BuildRequires:  boost-devel

BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel

# do not check .so files in the python_sitelib directory
%global __provides_exclude_from ^(%{python_sitearch}/.*\\.so)$

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
Botan is a BSD-licensed crypto library written in C++. It provides a
wide variety of basic cryptographic algorithms, X.509 certificates and
CRLs, PKCS \#10 certificate requests, a filter/pipe message processing
system, and a wide variety of other features, all written in portable
C++. The API reference, tutorial, and examples may help impart the
flavor of the library.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       bzip2-devel
Requires:       zlib-devel
Requires:       openssl-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
%{summary}

This package contains HTML documentation for %{name}.


%package        python
Summary:        Python bindings for %{name}

%description    python
%{summary}

This package contains the Python binding for %{name}.

Note: The Python binding should be considered alpha software, and the
interfaces may change in the future.


%prep
%setup -q -n Botan-%{version}
%patch0 -p1
%patch1 -p1

%build
# we have the necessary prerequisites, so enable optional modules
%define enable_modules bzip2,zlib,openssl

# fixme: maybe disable unix_procs, very slow.
%define disable_modules gnump

./configure.py \
        --prefix=%{_prefix} \
        --libdir=%{_lib} \
        --cc=gcc \
        --os=linux \
        --cpu=%{_arch} \
        --enable-modules=%{enable_modules} \
        --disable-modules=%{disable_modules} \
        --with-boost-python \
        --with-python-version=%{python_version} \
        --with-sphinx

# (ab)using CXX as an easy way to inject our CXXFLAGS
make CXX="g++ ${CXXFLAGS:-%{optflags}}" %{?_smp_mflags}
make -f Makefile.python \
  CXX="g++ ${CXXFLAGS:-%{optflags}}" %{?_smp_mflags}


%install
make install \
     DESTDIR=%{buildroot}%{_prefix} \
     DOCDIR=%{buildroot}%{_pkgdocdir} \
     INSTALL_CMD_EXEC="install -p -m 755" \
     INSTALL_CMD_DATA="install -p -m 644"

make -f Makefile.python install \
     PYTHON_SITE_PACKAGE_DIR=%{buildroot}%{python_sitearch}

# fixups
find doc/examples -type f -exec chmod -x {} \;
mv doc/examples/python doc/python-examples
cp -a doc/{examples,python-examples,license.txt} \
   %{buildroot}%{_pkgdocdir}
rm -r %{buildroot}%{_pkgdocdir}/manual/{.doctrees,.buildinfo}

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%dir %{_pkgdocdir}
%{_pkgdocdir}/readme.txt
%{_pkgdocdir}/license.txt
%{_libdir}/libbotan-%{major_version}.so.*


%files devel
%{_pkgdocdir}/examples
%{_bindir}/botan-config-%{major_version}
%{_includedir}/*
%exclude %{_libdir}/libbotan-%{major_version}.a
%{_libdir}/libbotan-%{major_version}.so
%{_libdir}/pkgconfig/botan-%{major_version}.pc


%files doc
%dir %{_pkgdocdir}
%{_pkgdocdir}/manual
# next files duplicated on purpose, because -doc doesn't depend on the
# main package
%{_pkgdocdir}/readme.txt
%{_pkgdocdir}/license.txt


%files python
%{_pkgdocdir}/python-examples
%{python_sitearch}/%{name}


%check
make CXX="g++ ${CXXFLAGS:-%{optflags}}" %{?_smp_mflags} check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./check --validate


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.10.9-9
- Rebuild for new 4.0 release.

* Thu Sep 03 2015 Cjacker <cjacker@foxmail.com>
- rebuilt with new boost

