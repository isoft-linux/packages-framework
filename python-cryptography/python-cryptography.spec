%global with_python3 1

Name:           python-cryptography
Version:        1.3.1
Release:        1%{?dist}
Summary:        PyCA's cryptography library

License:        ASL 2.0 or BSD
URL:            https://cryptography.io/en/latest/
Source0:        https://pypi.python.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz
Patch0:         %{name}-1.3.1-setuptools.patch

BuildRequires:  openssl-devel

BuildRequires:  python-devel
BuildRequires:  pytest
BuildRequires:  python-setuptools
BuildRequires:  python-pretend
BuildRequires:  python-iso8601
BuildRequires:  python-cryptography-vectors = %{version}
BuildRequires:  python-pyasn1-modules >= 0.1.8
BuildRequires:  python2-hypothesis

BuildRequires:  python-idna >= 2.0
BuildRequires:  python-pyasn1 >= 0.1.8
BuildRequires:  python-six >= 1.4.1
BuildRequires:  python-cffi >= 1.4.1
BuildRequires:  python-enum34
BuildRequires:  python-ipaddress

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-pretend
BuildRequires:  python3-iso8601
BuildRequires:  python3-cryptography-vectors = %{version}
BuildRequires:  python3-pyasn1-modules >= 0.1.8
BuildRequires:  python3-hypothesis

BuildRequires:  python3-idna >= 2.0
BuildRequires:  python3-pyasn1 >= 0.1.8
BuildRequires:  python3-six >= 1.4.1
BuildRequires:  python3-cffi >= 1.4.1
%endif

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%package -n  python2-cryptography
Group:          Development/Libraries
Summary:        PyCA's cryptography library
Obsoletes:      python-cryptography <= %{version}-%{release}

%if 0%{?with_python3}
%{?python_provide:%python_provide python2-cryptography}
%else
Provides:       python-cryptography
%endif

Requires:       openssl
Requires:       python-idna >= 2.0
Requires:       python-pyasn1 >= 0.1.8
Requires:       python-six >= 1.4.1
Requires:       python-cffi >= 1.4.1
Requires:       python-enum34
Requires:       python-ipaddress

%description -n python2-cryptography
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%if 0%{?with_python3}
%package -n  python3-cryptography
Group:          Development/Libraries
Summary:        PyCA's cryptography library
%{?python_provide:%python_provide python3-cryptography}

Requires:       openssl
Requires:       python3-idna >= 2.0
Requires:       python3-pyasn1 >= 0.1.8
Requires:       python3-six >= 1.4.1
Requires:       python3-cffi >= 1.4.1

%description -n python3-cryptography
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.
%endif

%prep
%autosetup -p1 -n cryptography-%{version}

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


%files -n python2-cryptography
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python_sitearch}/*


%if 0%{?with_python3}
%files -n python3-cryptography
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python3_sitearch}/*
%endif


%changelog
* Fri Jul 08 2016 xiaotian.wu@i-soft.com.cn - 1.3.1-1
- update to 1.3.1

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 0.8.2-3
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.8.2-2
- Rebuild for new 4.0 release.

* Thu Oct 08 2015 Cjacker <cjacker@foxmail.com>
- downgrade from yetist 
