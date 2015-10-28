Name:           python-dateutil
Version:        2.4.2
Release:        3%{?dist}
Epoch:          1
Summary:        Powerful extensions to the standard datetime module

License:        Python
URL:            https://github.com/dateutil/dateutil
Source0:        https://github.com/dateutil/dateutil/archive/%{version}.tar.gz
# https://github.com/dateutil/dateutil/issues/11
Patch0:         python-dateutil-system-zoneinfo.patch
Patch1:         python-dateutil-timelex-string.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-six
Requires:       tzdata
Requires:       python-six
Conflicts:      python-vobject <= 0.8.1c-10

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 2.

%package -n python3-dateutil
Summary:        Powerful extensions to the standard datetime module
BuildRequires:  python3-devel
BuildRequires:  python3-six
Requires:       tzdata
Requires:       python3-six

%description -n python3-dateutil
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 3.

%package doc
Summary: API documentation for python-dateutil
%description doc
This package contains %{summary}.

%prep
%autosetup -p0 -n dateutil-%{version}
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%{__python2} setup.py build
%{__python3} setup.py build
make -C docs html

%install
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files
%license LICENSE
%doc NEWS README.rst
%{python2_sitelib}/dateutil/
%{python2_sitelib}/*.egg-info

%files -n python3-dateutil
%license LICENSE
%doc NEWS README.rst
%{python3_sitelib}/dateutil/
%{python3_sitelib}/*.egg-info

%files doc
%license LICENSE
%doc docs/_build/html

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:2.4.2-3
- Rebuild for new 4.0 release.

