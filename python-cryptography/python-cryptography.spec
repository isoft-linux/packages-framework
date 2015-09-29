%global with_python3 1

%global reqs() %1-idna >= 2.0 %1-pyasn1 %1-six >= 1.4.1 %1-cffi >= 0.8
%global breqs() %1-setuptools %1-pretend %1-iso8601 %1-cryptography-vectors = %{version}

Name:           python-cryptography
Version:        1.0
Release:        1
Summary:        PyCA's cryptography library

Group:          Development/Libraries
License:        ASL 2.0 or BSD
URL:            https://cryptography.io/en/latest/
Source0:        https://pypi.python.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz

BuildRequires:  openssl-devel
Requires:       openssl

BuildRequires:  python2-devel
BuildRequires:  pytest %breqs python
BuildRequires:  python-enum34 python-ipaddress %reqs python
Requires:       python-enum34 python-ipaddress %reqs python

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest %breqs python3
BuildRequires:  %reqs python3
%endif


%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%if 0%{?with_python3}
%package -n  python3-cryptography
Group:          Development/Libraries
Summary:        PyCA's cryptography library

Requires:       openssl
Requires:       %reqs python3

%description -n python3-cryptography
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.
%endif

%prep
%setup -q -n cryptography-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete

%{__python2} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}
popd
%endif


%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif


%files
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python_sitearch}/*


%if 0%{?with_python3}
%files -n python3-cryptography
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python3_sitearch}/*
%endif


%changelog
