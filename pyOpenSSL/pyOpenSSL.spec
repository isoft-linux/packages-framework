%global with_python3 1

Summary: Python wrapper module around the OpenSSL library
Name: pyOpenSSL
Version: 0.15.1
Release: 1
Source0: http://pypi.python.org/packages/source/p/pyOpenSSL/pyOpenSSL-%{version}.tar.gz

BuildArch: noarch
License: ASL 2.0
Group: Development/Libraries
Url: http://pyopenssl.sourceforge.net/

BuildRequires: python-setuptools
BuildRequires: python-sphinx

BuildRequires: python2-devel
BuildRequires: python-cryptography
Requires: python-cryptography
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-cryptography
%endif

%description
High-level wrapper around a subset of the OpenSSL library, includes among others
 * SSL.Connection objects, wrapping the methods of Python's portable
   sockets
 * Callbacks written in Python
 * Extensive error-handling mechanism, mirroring OpenSSL's error codes

%if 0%{?with_python3}
%package -n python3-pyOpenSSL
Summary: Python wrapper module around the OpenSSL library
Requires: python3-cryptography

%description -n python3-pyOpenSSL
High-level wrapper around a subset of the OpenSSL library, includes among others
 * SSL.Connection objects, wrapping the methods of Python's portable
   sockets
 * Callbacks written in Python
 * Extensive error-handling mechanism, mirroring OpenSSL's error codes
%endif

%package doc
Summary: Documentation for pyOpenSSL
BuildArch: noarch

%description doc
Documentation for pyOpenSSL

%prep
%setup -q -n pyOpenSSL-%{version}

%build
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

CFLAGS="%{optflags} -fno-strict-aliasing" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags} -fno-strict-aliasing" %{__python3} setup.py build
popd
%endif

%{__make} -C doc html

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%files
%{python_sitelib}/OpenSSL/
%{python_sitelib}/pyOpenSSL-*.egg-info

%if 0%{?with_python3}
%files -n python3-pyOpenSSL
%{python3_sitelib}/OpenSSL/
%{python3_sitelib}/pyOpenSSL-*.egg-info
%endif

%files doc
%doc examples doc/_build/html

%changelog
