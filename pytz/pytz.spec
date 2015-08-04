%global with_python3 1

Name:           pytz
Version:        2012d
Release:        8%{?dist}
Summary:        World Timezone Definitions for Python

Group:          Development/Languages
License:        MIT
URL:            http://pytz.sourceforge.net/
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Patch0:         pytz-2012d_zoneinfo.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

Requires: tzdata

%description
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Amost all (over 540) of the Olson timezones are supported.

%if 0%{?with_python3}
%package -n python3-%{name}
Requires:   python3
Summary:    World Timezone Definitions for Python

Group:      Development/Languages
%description -n python3-%{name}
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Amost all (over 540) of the Olson timezones are supported.
%endif

%prep
%setup -q
%patch0 -p0

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3



%install
%{__python} setup.py install --skip-build --root %{buildroot}
chmod +x %{buildroot}%{python_sitelib}/pytz/*.py
rm -rf  %{buildroot}%{python_sitelib}/pytz/zoneinfo

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES.txt LICENSE.txt README.txt
%{python_sitelib}/pytz/
%{python_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-pytz
%doc CHANGES.txt LICENSE.txt README.txt
%{python3_sitelib}/pytz/
%{python3_sitelib}/*.egg-info
%endif # with_python3


%changelog
