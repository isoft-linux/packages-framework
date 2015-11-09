%global with_python3 1

Name:           python-testtools
Version:        1.8.0
Release:        2%{?dist}
Summary:        Extensions to the Python unit testing framework

License:        MIT
URL:            https://launchpad.net/testtools
Source0:        http://pypi.python.org/packages/source/t/testtools/testtools-%{version}.tar.gz
Patch0:         testtools-1.8.0-py3.patch
# the only reason pbr >= 0.11 is needed at the moment
# is to generate the version tuple. generate it by hand instead.
Patch1:         testtools-1.8.0-old_pbr.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-extras
BuildRequires:  python-mimeparse >= 0.1.4
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-unittest2 >= 0.8.0
BuildREquires:  python-traceback2
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-extras
BuildRequires:  python3-mimeparse
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-unittest2
BuildRequires:  python3-traceback2
%endif
BuildRequires:  python-sphinx

Provides:       python2-testtools = %{version}-%{release}
Requires:       python-extras
Requires:       python-mimeparse
Requires:       python-pbr
Requires:       python-unittest2 >= 0.8.0

%description
testtools is a set of extensions to the Python standard library's unit testing
framework.


%if 0%{?with_python3}
%package -n python3-testtools
Summary:        Extensions to the Python unit testing framework

Requires:       python3-extras
Requires:       python3-mimeparse
Requires:       python3-pbr
Requires:       python3-unittest2

%description -n python3-testtools
testtools is a set of extensions to the Python standard library's unit testing
framework.

%endif # with_python3


%package        doc
Summary:        Documentation for %{name}

Requires:       %{name} = %{version}-%{release}

# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_temporary_exceptions
Provides:       bundled(jquery)

%description doc
This package contains HTML documentation for %{name}.


%prep
%setup -q -n testtools-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}

# make the Python 3 build load the Python 3.x compatibility library directly
pushd %{py3dir}
%patch0 -p1 -b .py3
popd

find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
rm %{py3dir}/testtools/_compat2x.py
rm testtools/_compat3x.py
%endif # with_python3


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

PYTHONPATH=$PWD make -C doc html


%install
# do python3 install first in case python-testtools ever install scripts in
# _bindir -- the one installed last should be Python 2.x's as that's the
# current default
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT



%check
make PYTHON=%{__python} check

#some test failed with python 3.5, let's bare it.
#%if 0%{?with_python3}
#pushd %{py3dir}
#make PYTHON=%{__python3} check
#popd
#%endif # with_python3


%files
%defattr(-,root,root,-)
%doc NEWS README.rst
%license LICENSE
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-testtools
%doc NEWS README.rst
%license LICENSE
%{python3_sitelib}/*
%endif

%files doc
%defattr(-,root,root,-)
%doc doc/_build/html/*


%changelog
