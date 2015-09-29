%global with_python3 1

Name:           python-gitdb
Version:        0.6.4
Release:        2
Summary:        A pure-Python git object database

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/packages/source/g/gitdb/gitdb-%{version}.tar.gz#md5=44e4366b8bdfd306b075c3a52c96ae1a
Source0:        gitdb-%{version}.tar.gz
Requires:       python-smmap

BuildRequires:  python-devel, python-nose, python-setuptools

%description
GitDB allows you to access bare git repositories for reading and writing. It
aims at allowing full access to loose objects as well as packs with performance
and scalability in mind. It operates exclusively on streams, allowing to
operate on large objects with a small memory footprint.

%if 0%{?with_python3}
%package -n python3-gitdb
Summary:        Python3 Git Library
Requires:       python3-smmap
BuildRequires:  python3-devel, python3-nose, python3-setuptools

%description -n python3-gitdb
%{description}
%endif

# Filter the private provide
%{?filter_setup:
%filter_provides_in %{python3_sitearch}/gitdb/_perf.so
%filter_setup
}

%prep
%setup -qc -n gitdb-%{version}
mv gitdb-%{version} python2

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find python2 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

pushd python2
cp AUTHORS LICENSE ../
popd

%build
pushd python2
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
popd

%if 0%{?with_python3}
pushd python3
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif

%install
pushd python2
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
chmod 0755 %{buildroot}%{python2_sitearch}/gitdb/_perf.so
popd
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%files
%defattr(-,root,root,-)
%if 0%{?fedora}
%license LICENSE
%else
%doc LICENSE
%endif
%doc AUTHORS
%{python2_sitearch}/gitdb-%{version}-py?.?.egg-info
%{python2_sitearch}/gitdb/

%if 0%{?with_python3}
%files -n python3-gitdb
%license LICENSE
%doc AUTHORS
%{python3_sitearch}/gitdb-%{version}-py?.?.egg-info
%{python3_sitearch}/gitdb/
%endif

%changelog
