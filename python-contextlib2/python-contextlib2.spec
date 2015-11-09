%global with_python3 1

%{!?_licensedir: %global license %%doc}

%global modname contextlib2

Name:               python-contextlib2
Version:            0.4.0
Release:            2%{?dist}
Summary:            Backports and enhancements for the contextlib module

License:            Python
URL:                http://pypi.python.org/pypi/contextlib2
Source0:            https://pypi.python.org/packages/source/c/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:          noarch

BuildRequires:      python2-devel

%if 0%{?with_python3}
BuildRequires:      python3-devel
%endif

%description
contextlib2 is a backport of the standard library's contextlib module to
earlier Python versions.

It also serves as a real world proving ground for possible future
enhancements to the standard library version.

%if 0%{?with_python3}
%package -n python3-contextlib2
Summary:            Backports and enhancements for the contextlib module

%description -n python3-contextlib2
contextlib2 is a backport of the standard library's contextlib module to
earlier Python versions.

It also serves as a real world proving ground for possible future
enhancements to the standard library version.
%endif

%prep
%setup -q -n %{modname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%check
%{__python2} test_contextlib2.py
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} test_contextlib2.py
popd
%endif

%files
%doc README.txt VERSION.txt NEWS.rst
%license LICENSE.txt
%{python2_sitelib}/%{modname}.py*
%{python2_sitelib}/%{modname}-%{version}*

%if 0%{?with_python3}
%files -n python3-contextlib2
%doc README.txt VERSION.txt NEWS.rst
%license LICENSE.txt
%{python3_sitelib}/%{modname}.py*
%{python3_sitelib}/__pycache__/%{modname}*
%{python3_sitelib}/%{modname}-%{version}-*
%endif

%changelog
