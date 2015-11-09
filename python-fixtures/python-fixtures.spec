%global pypi_name fixtures
%global with_python3 1

Name:           python-%{pypi_name}
Version:        0.3.14
Release:        5%{?dist}
Summary:        Fixtures, reusable state for writing clean tests and more

License:        ASL 2.0 or BSD
URL:            https://launchpad.net/python-fixtures
Source0:        http://pypi.python.org/packages/source/f/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel

Requires:       python-testtools

%description
Fixtures defines a Python contract for reusable state / support logic,
primarily for unit testing. Helper and adaption logic is included to
make it easy to write your own fixtures using the fixtures contract.
Glue code is provided that makes using fixtures that meet the Fixtures
contract in unittest compatible test cases easy and straight forward.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Fixtures, reusable state for writing clean tests and more
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-testtools

%description -n python3-%{pypi_name}
Fixtures defines a Python contract for reusable state / support logic,
primarily for unit testing. Helper and adaption logic is included to
make it easy to write your own fixtures using the fixtures contract.
Glue code is provided that makes using fixtures that meet the Fixtures
contract in unittest compatible test cases easy and straight forward.

%endif


%prep
%setup -q -n %{pypi_name}-%{version}

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif


%build
%{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif
%{__python} setup.py install --skip-build --root %{buildroot}


%files
%doc README GOALS NEWS Apache-2.0 BSD COPYING
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README GOALS NEWS Apache-2.0 BSD COPYING
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Fri Nov 06 2015 Cjacker <cjacker@foxmail.com> - 0.3.14-5
- Rebuild

