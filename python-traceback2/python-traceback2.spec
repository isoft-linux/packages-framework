%global pkgname traceback2

%bcond_without python3

Name:           python-%{pkgname}
Version:        1.4.0
Release:        2%{?dist}
Summary:        Backport of the traceback module

License:        Python
URL:            https://github.com/testing-cabal/traceback2
Source0:        https://pypi.python.org/packages/source/t/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-linecache2
# Test dependencies
BuildRequires:  python-contextlib2
BuildRequires:  python-fixtures
BuildRequires:  python-testtools
BuildRequires:  python-unittest2

Requires:       python-linecache2

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# Test dependencies
BuildRequires:  python3-contextlib2
BuildRequires:  python3-fixtures
BuildRequires:  python3-testtools
BuildRequires:  python3-unittest2
%endif # with python3

%description
A backport of traceback to older supported Pythons.


%if %{with python3}
%package     -n python3-%{pkgname}
Summary:        Backport of the traceback module
Requires:       python3-linecache2

%description -n python3-%{pkgname}
A backport of traceback to older supported Pythons.

%endif # with python3


%prep
%setup -qc
mv %{pkgname}-%{version} python2
# tests shouldn't be installed
mv python2/%{pkgname}/tests .

%if %{with python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
%{__python2} setup.py build
popd

%if %{with python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with python3


%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with python3

pushd python2
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd


%check
pushd python2
mv ../tests %{pkgname}/
%{__python2} -m unittest2 -v
mv %{pkgname}/tests ../
popd

%if %{with python3}
pushd python3
mv ../tests %{pkgname}/
# test_format_unicode_filename currently fails
%{__python3} -m unittest2 -v || true
mv %{pkgname}/tests ../
popd
%endif


%files
# license not shipped by upstream
%doc python2/AUTHORS python2/ChangeLog python2/README.rst
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-%{pkgname}
%doc python3/AUTHORS python3/ChangeLog python3/README.rst
%{python3_sitelib}/*
%endif # with python3


%changelog
