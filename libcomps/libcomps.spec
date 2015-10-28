%define python3_build 1


Name:           libcomps
Version:        0.1.6
Release:        15
Summary:        Comps XML file manipulation library

License:        GPLv2+
URL:            https://github.com/midnightercz/libcomps/
Source0:        https://github.com/midnightercz/libcomps/archive/libcomps-%{version}.tar.gz
BuildRequires:  libxml2-devel
BuildRequires:  check-devel
BuildRequires:  expat-devel
BuildRequires:  cmake

%description
Libcomps is library for structure-like manipulation with content of
comps XML files. Supports read/write XML file, structure(s) modification.

%package doc
Summary:        Documentation files for libcomps library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
BuildRequires:  doxygen

%description doc
Documentation files for libcomps library

%package -n python-libcomps-doc
Summary:        Documentation files for python bindings libcomps library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
BuildRequires:  python-sphinx

%description -n python-libcomps-doc
Documentation files for python bindings libcomps library

%package devel
Summary:        Development files for libcomps library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libcomps library

%package -n python-libcomps
Summary:        Python2 bindings for libcomps library
BuildRequires:  python-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python-libcomps
Python2 bindings for libcomps library

%if %python3_build
%package -n python3-libcomps
Summary:        Python3 bindings for libcomps library
BuildRequires:  python3-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-libcomps
Python3 bindings for libcomps library
%endif

%prep
%setup -qn %{name}-%{version}

%if %python3_build == 1
rm -rf py3
mkdir ../py3
cp -a . ../py3/
mv ../py3 ./
%endif

%build
%cmake -DPYTHON_DESIRED:STRING=2 libcomps/
make %{?_smp_mflags}
make %{?_smp_mflags} docs
make %{?_smp_mflags} pydocs

%if %python3_build == 1
pushd py3
%cmake -DPYTHON_DESIRED:STRING=3 libcomps/
make %{?_smp_mflags}
popd
%endif


%check
make test
%if %{python3_build}
pushd py3
make pytest
popd
%endif

%install
make install DESTDIR=%{buildroot}

%if %{python3_build}
pushd py3
make install DESTDIR=%{buildroot}
popd
%endif

%clean
rm -rf $buildroot

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
/usr/lib64/libcomps.so.*
%doc README.md COPYING

%files devel
/usr/lib64/libcomps.so
%{_includedir}/*

%files doc
%doc docs/libcomps-doc/html

%files -n python-libcomps-doc
%doc src/python/docs/html

%files -n python-libcomps
%{_libdir}/python2*
%exclude %{_libdir}/python2/libcomps/__pycache__

%if %{python3_build}
%files -n python3-libcomps
%{_libdir}/python3*
%exclude %{_libdir}/python3/libcomps/__pycache__
%endif

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.1.6-15
- Rebuild for new 4.0 release.

