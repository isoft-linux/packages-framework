%global with_python3 1

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           python-iniparse
Version:        0.4
Release:        16
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
License:        MIT and Python
URL:            http://code.google.com/p/iniparse/
Source0:        http://iniparse.googlecode.com/files/iniparse-%{version}.tar.gz
Patch0:         fix-issue-28.patch
# The patch upstream (http://code.google.com/p/iniparse/issues/detail?id=22)
# is Python3-only. The patch below uses python-six to create a version that works
# with both Python major versions and is more error-prone.
Patch1:         %{name}-python3-compat.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python2-devel
#BuildRequires:  python-test

Requires:       python-six

%if 0%{?with_python3}
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-devel
#BuildRequires:  python3-test
%endif

BuildArch: noarch

%description
iniparse is an INI parser for Python which is API compatible
with the standard library's ConfigParser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.

%if 0%{?with_python3}
%package -n python3-iniparse
Summary:        Python 3 Module for Accessing and Modifying Configuration Data in INI files
Requires:       python3-six

%description -n python3-iniparse
iniparse is an INI parser for Python 3 which is API compatible
with the standard library's configparser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.
%endif

%prep
%setup -q -n iniparse-%{version}
%patch0 -p1
%patch1 -p0
chmod -c -x html/index.html


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
rm -rf $RPM_BUILD_ROOT
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version} $RPM_BUILD_ROOT/%{_docdir}/python3-iniparse
popd
%endif


%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version} $RPM_BUILD_ROOT%{_pkgdocdir}

# Don't dupe the license
rm -rf $RPM_BUILD_ROOT%{_pkgdocdir}/LICENSE*
rm -rf $RPM_BUILD_ROOT%{_docdir}/python3-iniparse/LICENSE*

%clean
rm -rf $RPM_BUILD_ROOT

%check
#%{__python2} runtests.py

%if 0%{?with_python3}
pushd %{py3dir}
#%{__python3} runtests.py
popd
%endif

%files
%defattr(-,root,root,-)
%doc %{_pkgdocdir}
%{!?_licensedir:%global license %%doc}
%license LICENSE LICENSE-PSF
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-iniparse
%defattr(-,root,root,-)
%doc %{_docdir}/python3-iniparse
%{!?_licensedir:%global license %%doc}
%license LICENSE LICENSE-PSF
%{python3_sitelib}/*
%endif


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.4-16
- Rebuild for new 4.0 release.

* Wed Aug 26 2015 Cjacker <cjacker@foxmail.com>
- initial build from fedora.
