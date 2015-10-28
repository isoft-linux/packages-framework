#in main python
%global with_python3 0 
%global build_wheel 0 
%global with_tests 0

%global srcname pip
%if 0%{?build_wheel}
%global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%if 0%{?with_python3}
%global python3_wheelname %python2_wheelname
%endif
%endif

Name:           python-%{srcname}
Version:        7.0.3
Release:        3%{?dist}
Summary:        A tool for installing and managing Python packages

License:        MIT
URL:            http://www.pip-installer.org
Source0:        http://pypi.python.org/packages/source/p/pip/%{srcname}-%{version}.tar.gz

# to get tests:
# git clone https://github.com/pypa/pip && cd fig
# git checkout 1.5.6 && tar -czvf pip-1.5.6-tests.tar.gz tests/
%if 0%{?with_tests}
Source1:        pip-6.0.8-tests.tar.gz
%endif

Patch0:         pip-1.5rc1-allow-stripping-prefix-from-wheel-RECORD-files.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_tests}
BuildRequires:  python-mock
BuildRequires:  pytest
BuildRequires:  python-pretend
BuildRequires:  python-freezegun
BuildRequires:  python-scripttest
BuildRequires:  python-virtualenv
%endif
%if 0%{?build_wheel}
BuildRequires:  python-pip
BuildRequires:  python-wheel
%endif
Requires:       python-setuptools

%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.


%if 0%{?with_python3}
%package -n python3-pip
Summary:        A tool for installing and managing Python3 packages

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_tests}
BuildRequires:  python3-mock
BuildRequires:  python3-pytest
BuildRequires:  python3-pretend
BuildRequires:  python3-freezegun
BuildRequires:  python3-scripttest
BuildRequires:  python3-virtualenv
%endif
%if 0%{?build_wheel}
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif
Requires:  python3-setuptools

%description -n python3-pip
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}
%if 0%{?with_tests}
tar -xf %{SOURCE1}
%endif

%patch0 -p1

%{__sed} -i '1d' pip/__init__.py

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3


%build
%if 0%{?build_wheel}
%{__python} setup.py bdist_wheel
%else
%{__python} setup.py build
%endif

%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?build_wheel}
%{__python3} setup.py bdist_wheel
%else
%{__python3} setup.py build
%endif
popd
%endif # with_python3


%install
%{__rm} -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?build_wheel}
pip3 install -I dist/%{python3_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}
# TODO: we have to remove this by hand now, but it'd be nice if we wouldn't have to
# (pip install wheel doesn't overwrite)
rm %{buildroot}%{_bindir}/pip
%else
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif
%endif # with_python3

%if 0%{?build_wheel}
pip2 install -I dist/%{python2_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}
%else
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%if 0%{?with_tests}
%check
py.test -m 'not network'
pushd %{py3dir}
py.test-3.4 -m 'not network'
popd
%endif


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.rst docs
%attr(755,root,root) %{_bindir}/pip
%attr(755,root,root) %{_bindir}/pip2*
%{python_sitelib}/pip*

%if 0%{?with_python3}
%files -n python3-pip
%defattr(-,root,root,-)
%doc LICENSE.txt README.rst docs
%attr(755,root,root) %{_bindir}/pip3*
%{python3_sitelib}/pip*
%endif # with_python3

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 7.0.3-3
- Rebuild for new 4.0 release.

