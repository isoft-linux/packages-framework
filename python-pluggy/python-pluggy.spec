%global pypiname pluggy

%{!?__python2:%global __python2 %{__python}}
%{!?python2_sitelib:   %global python2_sitelib  %{python_sitelib}}
%{!?python2_sitearch:  %global python2_sitearch %{python_sitearch}}
%{!?python2_version:   %global python2_version  %{python_version}}

%global with_python3 1

Name:           python-pluggy
Version:        0.3.0
Release:        3%{?dist}
Summary:        The plugin manager stripped of pytest specific details

License:        MIT
URL:            https://github.com/hpk42/pluggy
Source0:        http://pypi.python.org/packages/source/t/%{pypiname}/%{pypiname}-%{version}.tar.gz


BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  pytest
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
%endif # with python3

%description
The plugin manager stripped of pytest specific details.

%if 0%{?with_python3}
%package -n python3-%{pypiname}
Summary:  The plugin manager stripped of pytest specific details.

%description -n python3-%{pypiname}
The plugin manager stripped of pytest specific details.

%endif # with python3


%prep
%setup -qc
mv %{pypiname}-%{version} python2

pushd python2
cp -a LICENSE ..
cp -a README.rst ..

rm -rf {pypiname}.egg-info
popd

%if 0%{?with_python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
%{__python2} setup.py build
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with python3


%install
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif # with python3

pushd python2
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
popd


%check
pushd python2
py.test test_pluggy.py
popd

%if 0%{?with_python3}
pushd python3
py.test-3.4 test_pluggy.py
popd
%endif


%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypiname}.py
%{python2_sitelib}/%{pypiname}.pyc
%{python2_sitelib}/%{pypiname}.pyo
%{python2_sitelib}/%{pypiname}-%{version}-py%{python2_version}.egg-info


%if 0%{?with_python3}
%files -n python3-%{pypiname}
%{python3_sitelib}/%{pypiname}.py
%{python3_sitelib}/__pycache__/%{pypiname}.cpython-*.pyc
%{python3_sitelib}/__pycache__/%{pypiname}.cpython-*.pyo
%{python3_sitelib}/%{pypiname}-%{version}-py%{python3_version}.egg-info
%doc README.rst
%license LICENSE
%endif # with python3


%changelog
