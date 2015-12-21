%global with_python3 1
%global __python3 python3

Name:           python-six
Version:        1.10.0
Release:        2%{?dist}
Summary:        Python 2 and 3 compatibility utilities

License:        MIT
URL:            http://pypi.python.org/pypi/six/
Source0:        http://pypi.python.org/packages/source/s/six/six-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
# For use by selftests:
BuildRequires:  pytest
BuildRequires:  python-pluggy
#BuildRequires:  tkinter
%if 0%{?with_python3}
BuildRequires:  python3-devel
# For use by selftests:
BuildRequires:  python3-pytest
BuildRequires:  python3-pluggy
#BuildRequires:  python3-tkinter
%endif

%description
python-six provides simple utilities for wrapping over differences between
Python 2 and Python 3.

This is the Python 2 build of the module.

%if 0%{?with_python3}
%package -n python3-six
Summary:        Python 2 and 3 compatibility utilities

%description -n python3-six
python-six provides simple utilities for wrapping over differences between
Python 2 and Python 3.

This is the Python 3 build of the module.
%endif

%prep
%setup -q -n six-%{version}
%if 0%{?with_python3}
rm -rf %{py3dir}
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
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%check
py.test -rfsxX test_six.py
%if 0%{?with_python3}
pushd %{py3dir}
py.test-%{python3_version} -rfsxX test_six.py
popd
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README documentation/index.rst
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-six
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README documentation/index.rst
%{python3_sitelib}/*
%endif


%changelog
* Mon Dec 21 2015 Cjacker <cjacker@foxmail.com> - 1.10.0-2
- Update

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.9.0-4
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.9.0-3
- Rebuild for new 4.0 release.

