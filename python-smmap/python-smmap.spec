%global with_python3 1

Name:           python-smmap
Version:        0.9.0
Release:        2
Summary:        Sliding window memory map manager

License:        BSD
URL:            https://github.com/Byron/smmap
# Download from https://pypi.python.org/packages/source/s/smmap/smmap-0.9.0.tar.gz#md5=d7932d5ace206bf4ae15198cf36fb6ab
Source0:        http://pypi.python.org/packages/source/s/smmap/smmap-0.9.0.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools, python-nose

%description
A pure python implementation of a sliding window memory map manager

%if 0%{?with_python3}
%package -n python3-smmap
Summary:        Python3 Sliding window memory map manager
BuildRequires:  python3-devel, python3-setuptools, python3-nose

%description -n python3-smmap
%{description}
%endif # if with_python3

%prep
%setup -qc -n smmap-%{version}
mv smmap-%{version} python2

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find python2 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
pushd python2
%{__python2} setup.py build
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with_python3

%check
pushd python2
nosetests
popd
%if 0%{?with_python3}
pushd python3
nosetests
popd
%endif # with_python3

%install
pushd python2
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python2_sitelib}/smmap/test
popd
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif # with_python3


%files
%{python2_sitelib}/smmap/
%{python2_sitelib}/smmap-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-smmap
%{python3_sitelib}/smmap-%{version}-py?.?.egg-info
%{python3_sitelib}/smmap/
%endif # with_python3

%changelog
