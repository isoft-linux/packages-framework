%global with_python3 1

Name:           pytz
Version:        2015.7
Release:        2%{?dist}
Summary:        World Timezone Definitions for Python

License:        MIT
URL:            http://pytz.sourceforge.net/
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
# Patch to use the system supplied zoneinfo files
Patch0:         pytz-zoneinfo.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  pytest
Requires:       tzdata
Provides:       python2-pytz = %{version}-%{release}

%description
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Almost all (over 540) of the Olson timezones are supported.

%if 0%{?with_python3}
%package -n python3-%{name}
Summary:        World Timezone Definitions for Python
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
Requires:       tzdata

%description -n python3-%{name}
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Almost all (over 540) of the Olson timezones are supported.
%endif

%prep
%setup -q
%patch0 -p1 -b .zoneinfo


%build
%{__python} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif # with_python3


%install
%{__python} setup.py install --skip-build --root %{buildroot}
chmod +x %{buildroot}%{python2_sitelib}/pytz/*.py
rm -r %{buildroot}%{python2_sitelib}/pytz/zoneinfo

%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
rm -r %{buildroot}%{python3_sitelib}/pytz/zoneinfo
%endif # with_python3


%check
PYTHONPATH=%{buildroot}%{python2_sitelib} py.test-%{python2_version} -v
%if 0%{?with_python3}
PYTHONPATH=%{buildroot}%{python2_sitelib} py.test-%{python3_version} -v
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc CHANGES.txt LICENSE.txt README.txt
%{python2_sitelib}/pytz/
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-pytz
%doc CHANGES.txt LICENSE.txt README.txt
%{python3_sitelib}/pytz/
%{python3_sitelib}/*.egg-info
%endif # with_python3


%changelog
* Fri Nov 06 2015 Cjacker <cjacker@foxmail.com> - 2015.7-2
- Update

