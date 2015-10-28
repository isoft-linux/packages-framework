%global with_python3 1
%global mod_name mock

Name:           python-mock
Version:        1.0.1
Release:        6%{?dist}
Summary:        A Python Mocking and Patching Library for Testing

License:        BSD
URL:            http://www.voidspace.org.uk/python/%{mod_name}/
Source0:        http://pypi.python.org/packages/source/m/%{mod_name}/%{mod_name}-%{version}.tar.gz
Source1:        LICENSE.txt

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-unittest2

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif


%description
Mock is a Python module that provides a core mock class. It removes the need
to create a host of stubs throughout your test suite. After performing an
action, you can make assertions about which methods / attributes were used and
arguments they were called with. You can also specify return values and set
needed attributes in the normal way.

%if 0%{?with_python3}
%package -n python3-mock
Summary:        A Python Mocking and Patching Library for Testing

%description -n python3-mock
Mock is a Python module that provides a core mock class. It removes the need
to create a host of stubs throughout your test suite. After performing an
action, you can make assertions about which methods / attributes were used and
arguments they were called with. You can also specify return values and set
needed attributes in the normal way.

%endif


%prep
%setup -q -n %{mod_name}-%{version}
cp -p %{SOURCE1} .

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -ap . %{py3dir}
%endif


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%check
%{__python} setup.py test


%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc docs/ README.txt PKG-INFO LICENSE.txt
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{mod_name}.py*

%if 0%{?with_python3}
%files -n python3-mock
%doc docs/ README.txt PKG-INFO LICENSE.txt
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{mod_name}.py*
%{python3_sitelib}/__pycache__/%{mod_name}*
%endif


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.1-6
- Rebuild for new 4.0 release.

