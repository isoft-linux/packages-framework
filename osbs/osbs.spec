%global with_python3 0

%global commit 82fcea79d616b319e1ad5b7a985cd40f579e610b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           osbs
Version:        0.14
Release:        2

Summary:        Python command line client for OpenShift Build Service
License:        BSD
URL:            https://github.com/DBuildService/osbs-client
Source0:        https://github.com/DBuildService/osbs-client/archive/%{commit}/osbs-client-%{commit}.tar.gz

BuildArch:      noarch

Requires:       python-osbs

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
It is able to query OpenShift v3 for various stuff related to building images.
It can initiate builds, list builds, get info about builds, get build logs...
This package contains osbs command line client.

%package -n python-osbs
Summary:        Python 2 module for OpenShift Build Service
License:        BSD
Requires:       python-pycurl
Requires:       python-setuptools
#Requires:       python-requests

%description -n python-osbs
It is able to query OpenShift v3 for various stuff related to building images.
It can initiate builds, list builds, get info about builds, get build logs...
This package contains osbs Python 2 bindings.

%if 0%{?with_python3}
%package -n python3-osbs
Summary:        Python 3 module for OpenShift Build Service
License:        BSD
Requires:       python3-pycurl
Requires:       python3-setuptools
#Requires:       python3-requests

%description -n python3-osbs
It is able to query OpenShift v3 for various stuff related to building images.
It can initiate builds, list builds, get info about builds, get build logs...
This package contains osbs Python 3 bindings.
%endif # with_python3


%prep
%setup -qn osbs-client-%{commit}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
# build python package
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
mv %{buildroot}%{_bindir}/osbs %{buildroot}%{_bindir}/osbs3
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/osbs %{buildroot}%{_bindir}/osbs2
ln -s  %{_bindir}/osbs2 %{buildroot}%{_bindir}/osbs


%files
%doc README.md
%{_bindir}/osbs


%files -n python-osbs
%doc README.md
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_bindir}/osbs2
%if 0%{?rhel}
%{python_sitelib}/osbs/
%{python_sitelib}/osbs-%{version}-py2.*.egg-info/
%else
%{python2_sitelib}/osbs/
%{python2_sitelib}/osbs-%{version}-py2.*.egg-info/
%endif
%dir %{_datadir}/osbs
%{_datadir}/osbs/*.json


%if 0%{?with_python3}
%files -n python3-osbs
%doc README.md
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_bindir}/osbs3
%{python3_sitelib}/osbs/
%{python3_sitelib}/osbs-%{version}-py3.*.egg-info/
%dir %{_datadir}/osbs
%{_datadir}/osbs/*.json
%endif # with_python3

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.14-2
- Rebuild for new 4.0 release.

