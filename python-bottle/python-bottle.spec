%global srcname bottle

Name:           python-%{srcname}
Version:        0.12.6
Release:        3%{?dist}
Summary:        Fast and simple WSGI-framework for small web-applications

License:        MIT
URL:            http://bottlepy.org
Source0:        http://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
Bottle is a fast and simple micro-framework for small web-applications. 
It offers request dispatching (Routes) with URL parameter support, Templates, 
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and 
template engines. All in a single file and with no dependencies other than the 
Python Standard Library.

%package -n python3-%{srcname}
Summary:        Fast and simple WSGI-framework for small web-applications

%description -n python3-%{srcname}
Bottle is a fast and simple micro-framework for small web-applications. 
It offers request dispatching (Routes) with URL parameter support, Templates, 
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and 
template engines. All in a single file and with no dependencies other than the 
Python Standard Library.

%prep
%setup -q -n %{srcname}-%{version}
sed -i '/^#!/d' bottle.py

rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%{__python} setup.py build

pushd %{py3dir}
%{__python3} setup.py build
popd

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm %{buildroot}%{_bindir}/bottle.py

pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
rm %{buildroot}%{_bindir}/bottle.py
popd

%files
%doc README.rst PKG-INFO
%{python_sitelib}/*

%files -n python3-%{srcname}
%doc README.rst PKG-INFO
%{python3_sitelib}/*

%changelog
* Fri Nov 06 2015 Cjacker <cjacker@foxmail.com> - 0.12.6-3
- Initial build

