%global with_python3 1

%global srcname iso8601

Name:           python-%{srcname}
Version:        0.1.10
Release:        7
Summary:        Simple module to parse ISO 8601 dates

License:        MIT
URL:            http://pypi.python.org/pypi/%{srcname}/
Source0:        http://pypi.python.org/packages/source/i/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
%endif

%description
This module parses the most common forms of ISO 8601 date strings
(e.g. 2007-01-14T20:34:22+00:00) into datetime objects.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Simple module to parse ISO 8601 dates

%description -n python3-%{srcname}
This module parses the most common forms of ISO 8601 date strings
(e.g. 2007-01-14T20:34:22+00:00) into datetime objects.
%endif

%prep
%setup -qn %{srcname}-%{version}

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python3_sitelib}/*
%endif

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 0.1.10-7
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.1.10-6
- Rebuild for new 4.0 release.

