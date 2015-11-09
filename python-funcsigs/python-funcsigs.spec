%global mod_name funcsigs 

Name:           python-funcsigs
Version:        0.4 
Release:        3%{?dist}
Summary:        Python function signatures 

License:        BSD
URL:            http://www.voidspace.org.uk/python/%{mod_name}/
Source0:        http://pypi.python.org/packages/source/f/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-unittest2

%description
funcsigs is a backport of the PEP 362 function signature features from Python 3.3’s inspect module. 
The backport is compatible with Python 2.6, 2.7 as well as 3.2 and up.

%prep
%setup -q -n %{mod_name}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%check
%{__python} setup.py test

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{mod_name}

%changelog
* Fri Nov 06 2015 Cjacker <cjacker@foxmail.com> - 0.4-3
- Initial build

