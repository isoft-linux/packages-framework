%bcond_without python3

%global srcname pretend

Name:           python-pretend
Version:        1.0.8
Release:        5
Summary:        A library for stubbing in Python

License:        BSD
URL:            https://github.com/alex/pretend
Source0:        https://pypi.python.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif


%description
Pretend is a library to make stubbing with Python easier.


%if %{with python3}
%package -n python3-pretend
Summary:        A library for stubbing in Python
License:        BSD


%description -n python3-pretend
Pretend is a library to make stubbing with Python easier.
%endif


%prep
%setup -q -n %{srcname}-%{version}

# Delete upstream supplied egg-info
rm -rf *.egg-info

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%{__python2} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}


%files
%doc PKG-INFO README.rst LICENSE.rst
%{python2_sitelib}/pretend.py*
%{python2_sitelib}/pretend-%{version}-py2.?.egg-info

%if %{with python3}
%files -n python3-pretend
%doc PKG-INFO README.rst LICENSE.rst
%{python3_sitelib}/pretend.py
%{python3_sitelib}/__pycache__/pretend.cpython-3?.py*
%{python3_sitelib}/pretend-%{version}-py3.?.egg-info
%endif


%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.0.8-5
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.8-4
- Rebuild for new 4.0 release.

