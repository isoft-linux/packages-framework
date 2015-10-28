# Created by pyp2rpm-0.4.2
%global pypi_name jsonschema

%global with_python3 1

Name:           python-%{pypi_name}
Version:        2.4.0
Release:        2%{?dist}
Summary:        An implementation of JSON Schema validation for Python

License:        MIT
URL:            http://pypi.python.org/pypi/jsonschema
Source0:        http://pypi.python.org/packages/source/j/jsonschema/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python-mock

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-mock
%endif


%description
jsonschema is JSON Schema validator currently based on
http://tools.ietf.org/html/draft-zyp-json-schema-03

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        An implementation of JSON Schema validation for Python
%description -n python3-%{pypi_name}
jsonschema is JSON Schema validator currently based on
http://tools.ietf.org/html/draft-zyp-json-schema-03
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
    %{__python3} setup.py build
popd
%endif
%{__python} setup.py build


%install
%if 0%{?with_python3}
pushd %{py3dir}
    %{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
%if 0%{?with_python3}
pushd %{py3dir}
    %{_bindir}/nosetests-3* -v
popd
%endif
%{_bindir}/nosetests -v

%files
%doc README.rst COPYING
%{_bindir}/jsonschema
%{python_sitelib}/%{pypi_name}/
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst COPYING
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif


%changelog
