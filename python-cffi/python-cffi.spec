%global with_python3 1

Name:           python-cffi
Version:        1.1.2 
Release:        1%{?dist}
Group:          Development/Libraries
Summary:        Foreign Function Interface for Python to call C code
License:        BSD
URL:            http://cffi.readthedocs.org/
Source0:        http://pypi.python.org/packages/source/c/cffi/cffi-%{version}.tar.gz

BuildRequires:  libffi-devel python-sphinx
BuildRequires:  python2-devel python-setuptools Cython python-pycparser
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools python3-Cython python3-pycparser
%endif # if with_python3

Requires:       python-pycparser

# Do not check .so files in the python_sitelib directory
# or any files in the application's directory for provides
%global __provides_exclude_from ^(%{python_sitearch}|%{python3_sitearch})/.*\\.so$

%description
Foreign Function Interface for Python, providing a convenient and
reliable way of calling existing C code from Python. The interface is
based on LuaJIT’s FFI.

%if 0%{?with_python3}
%package -n python3-cffi
Summary:        Foreign Function Interface for Python 3 to call C code
Group:          Development/Libraries
Requires:       python3-pycparser

%description -n python3-cffi
Foreign Function Interface for Python, providing a convenient and
reliable way of calling existing C code from Python. The interface is
based on LuaJIT’s FFI.
%endif # with_python3

%package doc
Summary:        Documentation for CFFI
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for CFFI, the Foreign Function Interface for Python.

%prep
%setup -q -n cffi-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%{__python} setup.py build
cd doc
make html
rm build/html/.buildinfo

#%check
## The following test procedure works when I run it manually, but fails
## from rpmbuild, complaining that it can't import _cffi_backend, and I'm
## not sure how to make it work
#python setup_base.py build
#PYTHONPATH=build/lib.linux-* py.test c/ testing/

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}
popd
%endif # with_python3
%{__python} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}

%files
%doc LICENSE PKG-INFO
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-cffi
%doc LICENSE PKG-INFO
%{python3_sitearch}/*
%endif # with_python3

%files doc
%doc doc/build/html

%changelog
* Mon Sep 07 2015 Cjacker <cjacker@foxmail.com>
- update to 1.1.2
