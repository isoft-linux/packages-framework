%global pypi_name wheel
%bcond_without python3

Name:           python-%{pypi_name}
Version:        0.24.0
Release:        4%{?dist}
Summary:        A built-package format for Python

License:        MIT
URL:            https://bitbucket.org/pypa/wheel
Source0:        https://pypi.python.org/packages/source/w/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools

BuildRequires:  pytest
BuildRequires:  python-jsonschema
BuildRequires:  python-keyring

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-keyring
BuildRequires:  python3-jsonschema
%endif # if with_python3


%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

%if 0%{with python3}
%package -n     python3-%{pypi_name}
Summary:        A built-package format for Python

%description -n python3-%{pypi_name}
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

This is package contains Python 3 version of the package.
%endif # with_python3


%prep
%setup -q -n %{pypi_name}-%{version}

# remove unneeded shebangs
sed -ie '1d' %{pypi_name}/{egg2wheel,wininst2wheel}.py

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
pushd %{buildroot}%{_bindir}
for f in $(ls); do mv $f python3-$f; done
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}


%check
# remove setup.cfg that makes pytest require pytest-cov (unnecessary dep)
#rm setup.cfg
#PYTHONPATH=$(pwd) py.test --ignore build 
## no test for Python 3, no python3-jsonschema yet
#%if %{with python3}
#pushd %{py3dir}
#rm setup.cfg
#PYTHONPATH=$(pwd) py.test-%{python3_version} --ignore build
#popd
#%endif # with_python3


%files
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/wheel
%{python_sitelib}/%{pypi_name}*
%exclude %{python_sitelib}/%{pypi_name}/test
%if %{with python3}

%files -n python3-%{pypi_name}
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/python3-wheel
%{python3_sitelib}/%{pypi_name}*
%exclude %{python3_sitelib}/%{pypi_name}/test
%endif # with_python3


%changelog
