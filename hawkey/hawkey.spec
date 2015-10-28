%global libsolv_version 0.6.4-1

%if 0
# Do not build bindings for python3 for RHEL <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:		hawkey
Version:	0.6.0
Release:	3
Summary:	Library providing simplified C and Python API to libsolv
License:	LGPLv2+
URL:		https://github.com/rpm-software-management/%{name}
# git clone https://github.com/rpm-software-management/hawkey.git && cd hawkey && tito build --tgz
Source0:	https://github.com/rpm-software-management/%{name}/archive/%{name}-%{version}.tar.gz
BuildRequires:	libsolv-devel >= %{libsolv_version}
BuildRequires:	cmake expat-devel librpm-devel zlib-devel check-devel
Requires:	libsolv%{?_isa} >= %{libsolv_version}
# prevent provides from nonstandard paths:
%filter_provides_in %{python_sitearch}/.*\.so$
%if %{with python3}
%filter_provides_in %{python3_sitearch}/.*\.so$
%endif
# filter out _hawkey_testmodule.so DT_NEEDED _hawkeymodule.so:
%filter_requires_in %{python_sitearch}/hawkey/test/.*\.so$
%if %{with python3}
%filter_requires_in %{python3_sitearch}/hawkey/test/.*\.so$
%endif
%filter_setup

%description
A Library providing simplified C and Python API to libsolv.

%package devel
Summary:	A Library providing simplified C and Python API to libsolv
Requires:	hawkey%{?_isa} = %{version}-%{release}
Requires:	libsolv-devel

%description devel
Development files for hawkey.

%package -n python-hawkey
Summary:	Python 2 bindings for the hawkey library
BuildRequires:  python2-devel
BuildRequires:  python-nose
%if %{with python3}
BuildRequires:	python-sphinx >= 1.1.3-9
%else
BuildRequires:	python-sphinx
%endif
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python-hawkey
Python 2 bindings for the hawkey library.

%if %{with python3}
%package -n python3-hawkey
Summary:	Python 3 bindings for the hawkey library
BuildRequires:	python3-devel
BuildRequires:	python3-nose
BuildRequires:	python3-sphinx >= 1.1.3-9
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python3-hawkey
Python 3 bindings for the hawkey library.
%endif

%prep
%setup -q -n %{name}-%{version}

%if %{with python3}
rm -rf py3
mkdir ../py3
cp -a . ../py3/
mv ../py3 ./
%endif

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo .
make %{?_smp_mflags}
make doc-man

%if %{with python3}
pushd py3
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DPYTHON_DESIRED:str=3.
make %{?_smp_mflags}
make doc-man
popd
%endif

%check
make ARGS="-V" test
%if %{with python3}
./py3/tests/python/tests/run_nosetests
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT
%if %{with python3}
pushd py3
make install DESTDIR=$RPM_BUILD_ROOT
popd
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING README.rst
#%{_libdir}/libhawkey.so.*
/usr/lib64/libhawkey.so.*

%files devel
#%{_libdir}/libhawkey.so
#%{_libdir}/pkgconfig/hawkey.pc
/usr/lib64/libhawkey.so
/usr/lib64/pkgconfig/hawkey.pc
%{_includedir}/hawkey/
%{_mandir}/man3/hawkey.3.gz

%files -n python-hawkey
%{python_sitearch}/

%if %{with python3}
%files -n python3-hawkey
%{python3_sitearch}/
%exclude %{python3_sitearch}/hawkey/__pycache__
%exclude %{python3_sitearch}/hawkey/test/__pycache__
%endif

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.6.0-3
- Rebuild for new 4.0 release.

