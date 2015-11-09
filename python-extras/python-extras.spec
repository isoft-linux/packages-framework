%global with_python3 1

%global with_tests 1 

Name:           python-extras
Version:        0.0.3
Release:        7%{?dist}
Summary:        Useful extra bits for Python

License:        MIT
URL:            https://github.com/testing-cabal/extras
Source0:        https://pypi.python.org/packages/source/e/extras/extras-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_tests}
BuildRequires:  python-testtools
%endif

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_tests}
BuildRequires:  python3-testtools
%endif # with_tests
%endif

%description
extras is a set of extensions to the Python standard library, originally
written to make the code within testtools cleaner, but now split out for
general use outside of a testing context.


%if 0%{?with_python3}
%package -n python3-extras
Summary:        Useful extra bits for Python

%description -n python3-extras
extras is a set of extensions to the Python standard library, originally
written to make the code within testtools cleaner, but now split out for
general use outside of a testing context.
%endif # with_python3


%prep
%setup -q -n extras-%{version}
# Remove bundled egg-info
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}

find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install

# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check
%if 0%{?with_tests}
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3
%endif # with_tests



%files
%doc LICENSE NEWS README.rst
# For noarch packages: sitelib
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-extras
%doc LICENSE NEWS README.rst
%{python3_sitelib}/*
%endif # with_python3


%changelog
