%global with_python3 1
%global with_check 0 

%global build_wheel 0 

%global srcname setuptools
%if 0%{?build_wheel}
%global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%global python2_record %{python2_sitelib}/%{srcname}-%{version}.dist-info/RECORD
%if 0%{?with_python3}
%global python3_wheelname %python2_wheelname
%global python3_record %{python3_sitelib}/%{srcname}-%{version}.dist-info/RECORD
%endif
%endif

Name:           python-setuptools
Version:        18.0.1
Release:        1%{?dist}
Summary:        Easily build and distribute Python packages

Group:          Applications/System
License:        Python or ZPLv2.0
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://pypi.python.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        psfl.txt
Source2:        zpl.txt

BuildArch:      noarch
BuildRequires:  python2-devel
%if 0%{?build_wheel}
BuildRequires:  python-pip
BuildRequires:  python-wheel
%endif
%if 0%{?with_check}
BuildRequires:  pytest python-mock
%endif # with_check

%if 0%{?with_python3}
BuildRequires:  python3-devel
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-mock
%endif # with_check
%if 0%{?build_wheel}
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif # build_wheel
%endif # with_python3

# We're now back to setuptools as the package.
# Keep the python-distribute name active for a few releases.  Eventually we'll
# want to get rid of the Provides and just keep the Obsoletes
Provides: python-distribute = %{version}-%{release}
Obsoletes: python-distribute < 0.6.36-2

%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

%if 0%{?with_python3}
%package -n python3-setuptools
Summary:        Easily build and distribute Python 3 packages
Group:          Applications/System

# Note: Do not need to Require python3-backports-ssl_match_hostname because it
# has been present since python3-3.2.  We do not ship python3-3.0 or
# python3-3.1 anywhere

%description -n python3-setuptools
Setuptools is a collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}

# We can't remove .egg-info (but it doesn't matter, since it'll be rebuilt):
#  The problem is that to properly execute setuptools' setup.py,
#   it is needed for setuptools to be loaded as a Distribution
#   (with egg-info or .dist-info dir), it's not sufficient
#   to just have them on PYTHONPATH
#  Running "setup.py install" without having setuptools installed
#   as a distribution gives warnings such as
#    ... distutils/dist.py:267: UserWarning: Unknown distribution option: 'entry_points'
#   and doesn't create "easy_install" and .egg-info directory
# Note: this is only a problem if bootstrapping wheel or building on RHEL,
#  otherwise setuptools are installed as dependency into buildroot

# Remove bundled exes
rm -f setuptools/*.exe
# These tests require internet connection
rm setuptools/tests/test_integration.py 

%if 0%{?with_python3}
rm -rf %{py3dir}
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
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?build_wheel}
pip3 install -I dist/%{python3_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}

# TODO: we have to remove this by hand now, but it'd be nice if we wouldn't have to
# (pip install wheel doesn't overwrite)
rm %{buildroot}%{_bindir}/easy_install

sed -i '/\/usr\/bin\/easy_install,/d' %{buildroot}%{python3_record}
%else
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif

rm -rf %{buildroot}%{python3_sitelib}/setuptools/tests
%if 0%{?build_wheel}
sed -i '/^setuptools\/tests\//d' %{buildroot}%{python3_record}
%endif

install -p -m 0644 %{SOURCE1} %{SOURCE2} %{py3dir}
find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f
chmod +x %{buildroot}%{python3_sitelib}/setuptools/command/easy_install.py
popd
%endif # with_python3

%if 0%{?build_wheel}
pip2 install -I dist/%{python2_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}
%else
%{__python2} setup.py install --skip-build --root %{buildroot}
%endif

rm -rf %{buildroot}%{python2_sitelib}/setuptools/tests
%if 0%{?build_wheel}
sed -i '/^setuptools\/tests\//d' %{buildroot}%{python2_record}
%endif

install -p -m 0644 %{SOURCE1} %{SOURCE2} .
find %{buildroot}%{python2_sitelib} -name '*.exe' | xargs rm -f
chmod +x %{buildroot}%{python2_sitelib}/setuptools/command/easy_install.py

%if 0%{?with_check}
%check
LANG=en_US.utf8 PYTHONPATH=$(pwd) py.test

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.utf8 PYTHONPATH=$(pwd) py.test-%{python3_version}
popd
%endif # with_python3
%endif # with_check

%files
%doc *.txt docs
%{python2_sitelib}/*
%{_bindir}/easy_install
%{_bindir}/easy_install-2.*

%if 0%{?with_python3}
%files -n python3-setuptools
%doc psfl.txt zpl.txt docs
%{python3_sitelib}/*
%{_bindir}/easy_install-3.*
%endif # with_python3

%changelog
