%global with_python3 1

Name:           python-pycparser
Summary:        C parser and AST generator written in Python
Version:        2.14
Release:        2%{?dist}
License:        BSD
Group:          System Environment/Libraries
URL:            http://github.com/eliben/pycparser
Source0:        http://github.com/eliben/pycparser/archive/release_v%{version}.tar.gz
Source1:        pycparser-0.91.1-remove-relative-sys-path.py

Patch100:       pycparser-2.10-ply.patch
# This is Fedora-specific; I don't think we should request upstream to
# remove embedded libraries from their distribuution, when we can remove
# them during packaging.

BuildArch:      noarch

BuildRequires:  python2-devel python-setuptools

# for unit tests
BuildRequires:  dos2unix
BuildRequires:  python-ply

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
# for unit tests
BuildRequires:  python3-ply       
%endif # if with_python3

Requires:       python-ply

%description
pycparser is a complete parser for the C language, written in pure Python.
It is a module designed to be easily integrated into applications that
need to parse C source code.

%if 0%{?with_python3}
%package -n python3-pycparser
Summary:        C parser and AST generator written in Python
Group:          System Environment/Libraries
Requires:       python3-ply

%description -n python3-pycparser
pycparser is a complete parser for the C language, written in pure Python.
It is a module designed to be easily integrated into applications that
need to parse C source code.
%endif # if with_python3

%prep
%setup -q -n pycparser-release_v%{version}
%patch100 -p1 -F5 -b .ply

# remove embedded copy of ply
rm -rf pycparser/ply

# examples
%{__python} %{SOURCE1} examples
dos2unix LICENSE

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
%endif # with_python3

%build
%{__python} setup.py build
pushd build/lib/pycparser
%{__python} _build_tables.py
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
pushd build/lib/pycparser
%{__python3} _build_tables.py
popd
popd
%endif # with_python3

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%check
%{__python} tests/all_tests.py 

%if 0%{?with_python3}
%{__python3} tests/all_tests.py 
pushd %{py3dir}
popd
%endif # with_python3
 
%files
%doc examples LICENSE
%{python_sitelib}/pycparser/
%{python_sitelib}/pycparser-*.egg-info

%if 0%{?with_python3}
%files -n python3-pycparser
%{python3_sitelib}/pycparser/
%{python3_sitelib}/pycparser-*.egg-info
%endif # with_python3

%changelog
