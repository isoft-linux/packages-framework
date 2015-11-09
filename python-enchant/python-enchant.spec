%global with_python3 1

Name:           python-enchant
Version:        1.6.6
Release:        4%{?dist}
Summary:        Python bindings for Enchant spellchecking library

License:        LGPLv2+
URL:            http://packages.python.org/pyenchant/
Source0:        http://pypi.python.org/packages/source/p/pyenchant/pyenchant-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  enchant-devel

# Python 2 build requirements:
BuildRequires:  python2-devel
BuildRequires:  python-setuptools >= 0:0.6a9
# For running tests
BuildRequires:  python-nose

# Python 3 build requirements:
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 0:0.6a9
# For running tests
BuildRequires:  python3-nose
%endif # if with_python3

# Work around a problem with libenchant versioning
# (python-enchant-1.3.1 failed to work with enchant-1.4.2-2.fc10)
Requires:       enchant >= 1.5.0

# Package was arch specific before
Obsoletes:      python-enchant < 1.6.5

Provides:       PyEnchant

%description
PyEnchant is a spellchecking library for Python, based on the Enchant
library by Dom Lachowicz.

%if 0%{?with_python3}
%package -n python3-enchant
Summary:        Python 3 bindings for Enchant spellchecking library

%description -n python3-enchant
PyEnchant is a spellchecking library for Python 3, based on the Enchant
library by Dom Lachowicz.
%endif # with_python3

%prep
%setup -q -n pyenchant-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT --single-version-externally-managed
rm -rf $RPM_BUILD_ROOT/%{python3_sitelib}/*.egg-info
# Directories used in windows build
rm -rf $RPM_BUILD_ROOT/%{python3_sitelib}/enchant/lib
rm -rf $RPM_BUILD_ROOT/%{python3_sitelib}/enchant/share
popd
%endif # with_python3
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT --single-version-externally-managed
rm -rf $RPM_BUILD_ROOT/%{python_sitelib}/*.egg-info
# Directories used in windows build
rm -rf $RPM_BUILD_ROOT/%{python_sitelib}/enchant/lib
rm -rf $RPM_BUILD_ROOT/%{python_sitelib}/enchant/share

%check
#need Xwindow support
pushd $RPM_BUILD_ROOT/%{python_sitelib}
# There is no dictionary for language C, need to use en_US
export LANG=en_US.UTF-8
#xvfb-run /usr/bin/nosetests-2.*
popd

# Tests are failing in python3 because of collision between 
# local and stdlib tokenize module
pushd $RPM_BUILD_ROOT/%{python3_sitelib}
# There is no dictionary for language C, need to use en_US
export LANG=en_US.UTF-8
#xvfb-run /usr/bin/nosetests-3.*
popd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt TODO.txt
%dir %{python_sitelib}/enchant
%dir %{python_sitelib}/enchant/checker
%dir %{python_sitelib}/enchant/tokenize
%{python_sitelib}/enchant/*.py
%{python_sitelib}/enchant/*.py[co]
%{python_sitelib}/enchant/*/*.py
%{python_sitelib}/enchant/*/*.py[co]

%if 0%{?with_python3}
%files -n python3-enchant
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt TODO.txt
%dir %{python3_sitelib}/enchant
%dir %{python3_sitelib}/enchant/__pycache__
%dir %{python3_sitelib}/enchant/checker
%dir %{python3_sitelib}/enchant/checker/__pycache__
%dir %{python3_sitelib}/enchant/tokenize
%dir %{python3_sitelib}/enchant/tokenize/__pycache__
%{python3_sitelib}/enchant/*.py
%{python3_sitelib}/enchant/__pycache__/*.py[co]
%{python3_sitelib}/enchant/checker/*.py
%{python3_sitelib}/enchant/checker/__pycache__/*.py[co]
%{python3_sitelib}/enchant/tokenize/*.py
%{python3_sitelib}/enchant/tokenize/__pycache__/*.py[co]
%endif # with_python3


%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.6.6-4
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.6.6-3
- Rebuild for new 4.0 release.

