%global with_python3 1

Name:           python-cryptography
Version:        0.8.2
Release:        2%{?dist}
Summary:        PyCA's cryptography library

License:        ASL 2.0 or BSD
URL:            https://cryptography.io/en/latest/
Source0:        https://pypi.python.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz
Patch0:		cryptography-fix-dsa-double-free.patch

BuildRequires:  openssl-devel
BuildRequires:  python-enum34

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-cffi >= 0.8
BuildRequires:  python-six
BuildRequires:  python-cryptography-vectors = %{version}
BuildRequires:  python-pyasn1
BuildRequires:  python-iso8601
BuildRequires:  python-pretend
BuildRequires:  pytest

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi >= 0.8
BuildRequires:  python3-six
BuildRequires:  python3-cryptography-vectors = %{version}
BuildRequires:  python3-pyasn1
BuildRequires:  python3-iso8601
BuildRequires:  python3-pretend
BuildRequires:  python3-pytest
%endif

Requires:       openssl
Requires:       python-enum34
Requires:       python-cffi >= 0.8
Requires:       python-six >= 1.6.1
Requires:       python-pyasn1

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%if 0%{?with_python3}
%package -n  python3-cryptography
Summary:        PyCA's cryptography library

Requires:       openssl
Requires:       python3-cffi >= 0.8
Requires:       python3-six >= 1.6.1
Requires:       python3-pyasn1

%description -n python3-cryptography
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.
%endif

%prep
%setup -q -n cryptography-%{version}
%patch0 -p1

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
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.8.2-2
- Rebuild for new 4.0 release.

* Thu Oct 08 2015 Cjacker <cjacker@foxmail.com>
- downgrade from yetist 
