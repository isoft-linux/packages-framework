%global with_python3 1

%global pylib_version 1.4.29

Name:           pytest
Version:        2.7.2
Release:        2
Summary:        Simple powerful testing with Python

License:        MIT
URL:            http://pytest.org
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-setuptools
BuildRequires:  python-py >= %{pylib_version}
Requires:       python-py >= %{pylib_version}
BuildRequires:  python-sphinx
BuildRequires:  python-docutils
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-py >= %{pylib_version}
%endif # with_python3
# pytest was separated from pylib at that point
Conflicts:      python-py < 1.4.0

# used by the testsuite, if present:
# if pexpect is present, the testsuite fails on F19 due to
# http://bugs.python.org/issue17998
#BuildRequires:  python-pexpect
BuildRequires:  python-mock
#BuildRequires:  python-twisted-core
%if 0%{?with_python3}
#BuildRequires:  python3-pexpect
BuildRequires:  python3-mock
%endif # with_python3


%description
py.test provides simple, yet powerful testing for Python.


%if 0%{?with_python3}
%package -n python3-pytest
Summary:        Simple powerful testing with Python
Requires:       python3-setuptools
Requires:       python3-py >= %{pylib_version}


%description -n python3-pytest
py.test provides simple, yet powerful testing for Python.
%endif # with_python3


%prep
%setup -qc -n %{name}-%{version}

mv %{name}-%{version} python2

%if 0%{?with_python3}
cp -a python2 python3
%endif # with_python3


%build
pushd python2
%{__python2} setup.py build

#for l in doc/* ; do
#  make -C $l html PYTHONPATH=$(pwd)
#done

popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with_python3


%install
pushd python2
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# remove shebangs from all scripts
find %{buildroot}%{python2_sitelib} -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;

#mkdir -p _htmldocs/html
#for l in doc/* ; do
#  # remove hidden file
#  rm ${l}/_build/html/.buildinfo
#  mv ${l}/_build/html _htmldocs/html/${l##doc/}
#done
#
#rst2html README.rst > README.html
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# remove shebangs from all scripts
find %{buildroot}%{python3_sitelib} -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;

popd
%endif # with_python3

# use 2.X per default
pushd %{buildroot}%{_bindir}
ln -snf py.test-%{python2_version} py.test
popd


%check
pushd python2
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python2_sitelib} \
  %{buildroot}%{_bindir}/py.test-%{python2_version} -r s testing
popd

%if 0%{?with_python3}
pushd python3
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{buildroot}%{_bindir}/py.test-%{python3_version} -r s testing
popd
%endif # with_python3


%files
# %doc python2/_htmldocs/html
%if 0%{?_licensedir:1}
%license python2/LICENSE
%else
%doc python2/LICENSE
%endif # licensedir
%{_bindir}/py.test
%{_bindir}/py.test-%{python2_version}
%{python2_sitelib}/*


%if 0%{?with_python3}
%files -n python3-pytest
# %doc python2/_htmldocs/html
%if 0%{?_licensedir:1}
%license python3/LICENSE
%else
%doc python3/LICENSE
%endif # licensedir
%{_bindir}/py.test-%{python3_version}
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.7.2-2
- Rebuild for new 4.0 release.

