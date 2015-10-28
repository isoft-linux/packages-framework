%global with_python3 1

%global module pyasn1
%global modules_version 0.0.6

Name:           python-pyasn1
Version:        0.1.8
Release:        3
Summary:        ASN.1 tools for Python
License:        BSD
Source0:        http://downloads.sourceforge.net/pyasn1/pyasn1-%{version}.tar.gz
Source1:        http://downloads.sourceforge.net/pyasn1/pyasn1-modules-%{modules_version}.tar.gz
URL:            http://pyasn1.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
This is an implementation of ASN.1 types and codecs in the Python programming
language.

%package modules
Summary:    Modules for pyasn1
Requires:   python-pyasn1 >= %{version}-%{release}

%description modules
ASN.1 types modules for python-pyasn1.

%package -n python3-pyasn1
Summary:    ASN.1 tools for Python 3

%description -n python3-pyasn1
This is an implementation of ASN.1 types and codecs in the Python 3 programming
language.

%package -n python3-pyasn1-modules
Summary:    Modules for pyasn1
Requires:   python3-pyasn1 >= %{version}-%{release}

%description -n python3-pyasn1-modules
ASN.1 types modules for python3-pyasn1.


%prep
%setup -n %{module}-%{version} -q -b1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
cp -a ../pyasn1-modules-%{modules_version} %{py3dir}-modules
%endif


%build
%{__python} setup.py build
pushd ../pyasn1-modules-%{modules_version}
%{__python} setup.py build
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
pushd %{py3dir}-modules
%{__python3} setup.py build
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
pushd %{py3dir}-modules
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
pushd ../pyasn1-modules-%{modules_version}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd


%check
# PYTHONPATH is required because the the tests expect python{,3}-pyasn1
# to be installed.
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitelib}:$PYTHONPATH" %{__python2} test/suite.py
%if %{with python3}
pushd %{py3dir}
PYTHONPATH="$RPM_BUILD_ROOT%{python3_sitelib}:$PYTHONPATH" %{__python3} test/suite.py
popd
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README doc/*.html
%license LICENSE
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}-*.egg-info/

%files modules
%defattr(-,root,root,-)
%{python_sitelib}/%{module}_modules/
%{python_sitelib}/%{module}_modules-%{modules_version}-*.egg-info/

%if 0%{?with_python3}
%files -n python3-pyasn1
%defattr(-,root,root,-)
%doc README doc/*.html
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-%{version}-*.egg-info/

%files -n python3-pyasn1-modules
%defattr(-,root,root,-)
%{python3_sitelib}/%{module}_modules/
%{python3_sitelib}/%{module}_modules-%{modules_version}-*.egg-info/
%endif

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.1.8-3
- Rebuild for new 4.0 release.

