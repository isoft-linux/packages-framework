%global with_python3 1
%global pypi_name chardet
Name:           python-%{pypi_name}
Version:        2.2.1
Release:        3%{?dist}
Summary:        Character encoding auto-detection in Python

Group:          Development/Languages
License:        LGPLv2
URL:            https://github.com/%{pypi_name}/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel, python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel, python3-setuptools
%endif # with_python3

%description
Character encoding auto-detection in Python. As 
smart as your browser. Open source.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Character encoding auto-detection in Python 3

%description -n python3-%{pypi_name}
Character encoding auto-detection in Python. As 
smart as your browser. Open source.

Python 3 version.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
sed -ie '1d' %{pypi_name}/chardetect.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Do Python 3 first not to overwrite the entrypoint
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_bindir}/{,python3-}chardetect
popd
%endif # with_python3

%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/chardetect

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/python3-chardetect
%endif # with_python3


%changelog
