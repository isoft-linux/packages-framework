%global with_python3 1

# we have a circular (build) dependency with the (new) pytest package
# when generating the docs or running the testsuite
%global with_docs 0 
%global run_check 1

%global pytest_version 2.5

Name:           python-py
Version:        1.4.29
Release:        3%{?dist}
Summary:        Library with cross-python path, ini-parsing, io, code, log facilities
License:        MIT and Public Domain
#               main package: MIT, except: doc/style.css: Public Domain
URL:            http://pylib.readthedocs.org/
Source:         http://pypi.python.org/packages/source/p/py/py-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-setuptools
BuildRequires:  python-sphinx
%if 0%{?run_check}
BuildRequires:  pytest >= %{pytest_version}
%endif # run_check
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?run_check}
BuildRequires:  python3-pytest >= %{pytest_version}
%endif # run_check
%endif # with_python3

# needed by the testsuite
BuildRequires:  subversion


%description
The py lib is a Python development support library featuring the
following tools and modules:

  * py.path: uniform local and svn path objects
  * py.apipkg: explicit API control and lazy-importing
  * py.iniconfig: easy parsing of .ini files
  * py.code: dynamic code generation and introspection
  * py.path: uniform local and svn path objects

%if 0%{?with_python3}
%package -n python3-py
Summary:        Library with cross-python path, ini-parsing, io, code, log facilities
Requires:       python3-setuptools

%description -n python3-py
The py lib is a Python development support library featuring the
following tools and modules:

  * py.path: uniform local and svn path objects
  * py.apipkg: explicit API control and lazy-importing
  * py.iniconfig: easy parsing of .ini files
  * py.code: dynamic code generation and introspection
  * py.path: uniform local and svn path objects

%endif # with_python3

%prep
%setup -qc -n py-%{version}
mv py-%{version} python2

pushd python2
# remove shebangs and fix permissions
find -type f -a \( -name '*.py' -o -name 'py.*' \) \
   -exec sed -i '1{/^#!/d}' {} \; \
   -exec chmod u=rw,go=r {} \;

# fix line-endings
sed -i 's/\r//' README.txt
popd

%if 0%{?with_python3}
cp -a python2 python3
%endif # with_python3


%build
pushd python2
%{__python2} setup.py build

%if 0%{?with_docs}
make -C doc html PYTHONPATH=$(pwd)
%endif # with_docs
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with_python3


%install
pushd python2
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# remove hidden file
rm -rf doc/_build/html/.buildinfo
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif # with_python3


%check
# disable failing Subversion checks for now
#%if 0%{?run_check}
#pushd python2
#PYTHONPATH=%{buildroot}%{python2_sitelib} \
#LC_ALL="en_US.UTF-8" \
#py.test -r s -k"-TestWCSvnCommandPath" testing
#popd
#
#%if 0%{?with_python3}
#pushd python3
#PYTHONPATH=%{buildroot}%{python3_sitelib} \
#LC_ALL="en_US.UTF-8" \
#py.test-%{python3_version} -r s -k"-TestWCSvnCommandPath" testing
#popd
#%endif # with_python3
#%endif # run_check


%files
%doc python2/CHANGELOG
%doc python2/README.txt
%if 0%{?_licensedir:1}
%license python2/LICENSE
%else
%doc python2/LICENSE
%endif # licensedir
%if 0%{?with_docs}
%doc python2/doc/_build/html
%endif # with_docs
%{python2_sitelib}/*


%if 0%{?with_python3}
%files -n python3-py
%doc python3/CHANGELOG
%doc python3/README.txt
%if 0%{?_licensedir:1}
%license python2/LICENSE
%else
%doc python2/LICENSE
%endif # licensedir
%if 0%{?with_docs}
# HTML docs generated with Python2 for now
%doc python2/doc/_build/html
%endif # with_docs
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.4.29-3
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.4.29-2
- Rebuild for new 4.0 release.

