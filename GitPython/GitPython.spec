%global with_python3 1

Name:           GitPython
Version:        1.0.1
Release:        2
Summary:        Python Git Library

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/GitPython/
Source0:        http://pypi.python.org/packages/source/G/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools
Requires:       git
Requires:       python-gitdb

%description
GitPython is a python library used to interact with Git repositories.

GitPython provides object model access to your git repository. Once you have
created a repository object, you can traverse it to find parent commit(s),
trees, blobs, etc.

GitPython is a port of the grit library in Ruby created by Tom Preston-Werner
and Chris Wanstrath.

%if %{with python3}
%package -n python3-GitPython
Summary:        Python3 Git Library
Requires:       git
Requires:       python3-gitdb
BuildRequires:  python3-devel python3-setuptools

%description -n python3-GitPython
%{description}
%endif

%prep
%setup -qc
mv %{name}-%{version} python2

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find python2 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

pushd python2
cp AUTHORS CHANGES LICENSE ../
popd

%build
pushd python2
%{__python2} setup.py build
popd

%if %{with python3}
pushd python3
%{__python3} setup.py build
popd
%endif

%install
pushd python2
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
popd
%if %{with python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%files
%license LICENSE
%doc CHANGES AUTHORS
%{python2_sitelib}/GitPython-%{version}-py?.?.egg-info
%{python2_sitelib}/git/

%if %{with python3}
%files -n python3-GitPython
%license LICENSE
%doc CHANGES AUTHORS
%{python3_sitelib}/GitPython-%{version}-py?.?.egg-info
%{python3_sitelib}/git/
%endif

%changelog
