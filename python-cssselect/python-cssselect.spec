# Workaround for epel versions where don't exists python2 macro
%{!?__python2: %global __python2 %{__python}}

%global with_python3 1

%global with_tests 0

Name:           python-cssselect
Version:        0.9.1
Release:        8
Summary:        Parses CSS3 Selectors and translates them to XPath 1.0

License:        BSD
URL:            http://packages.python.org/cssselect/
Source0:        http://pypi.python.org/packages/source/c/cssselect/cssselect-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel python-setuptools
%if 0%{?with_tests}
BuildRequires:  python-lxml
%endif # if with_tests
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
%if 0%{?with_tests}
BuildRequires:  python3-lxml
%endif # if with_tests
%endif # if with_python3

%description
Cssselect parses CSS3 Selectors and translates them to XPath 1.0 expressions. 
Such expressions can be used in lxml or another XPath engine to find the 
matching elements in an XML or HTML document.

%if 0%{?with_python3}
%package -n python3-cssselect
Summary:        Parses CSS3 Selectors and translates them to XPath 1.0

%description -n python3-cssselect
Cssselect parses CSS3 Selectors and translates them to XPath 1.0 expressions. 
Such expressions can be used in lxml or another XPath engine to find the 
matching elements in an XML or HTML document.
%endif # if with_python3

%prep
%setup -q -n cssselect-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%check
%if 0%{?with_tests}
PYTHONPATH=$(pwd) %{__python2} cssselect/tests.py
%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=${py3dir} %{__python3} cssselect/tests.py
popd
%endif # with_python3
%endif # with_tests

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
chmod 755 $RPM_BUILD_ROOT/%{python3_sitelib}/cssselect/tests.py
popd
%endif # with_python3

%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
chmod 755 $RPM_BUILD_ROOT/%{python_sitelib}/cssselect/tests.py

%files
%doc AUTHORS docs README.rst CHANGES LICENSE PKG-INFO
%{python_sitelib}/cssselect*

%if 0%{?with_python3}
%files -n python3-cssselect
%doc AUTHORS docs README.rst CHANGES LICENSE PKG-INFO
%{python3_sitelib}/cssselect*
%endif # with_python3

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 0.9.1-8
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.9.1-7
- Rebuild for new 4.0 release.

