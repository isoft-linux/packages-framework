%global with_python3 1

Name:           pyxdg
Version:        0.25
Release:        2%{?dist}
Summary:        Python library to access freedesktop.org standards
License:        LGPLv2
URL:            http://freedesktop.org/Software/pyxdg
Source0:        http://people.freedesktop.org/~takluyver/%{name}-%{version}.tar.gz
# https://bugs.freedesktop.org/show_bug.cgi?id=61817
Patch0:		pyxdg-0.25-find-first-mimetype-match.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=73878
Patch1:		pyxdg-0.25-CVE-2014-1624.patch
BuildArch:      noarch
# These are needed for the nose tests.
BuildRequires:	python-nose, hicolor-icon-theme
BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3

Provides: python-xdg

%description
PyXDG is a python library to access freedesktop.org standards 

%if 0%{?with_python3}
%package -n python3-pyxdg
Summary: Python3 library to access freedesktop.org standards
Provides: python3-xdg

%description -n python3-pyxdg
PyXDG is a python library to access freedesktop.org standards. This
package contains a Python 3 version of PyXDG.
%endif # with_python3

%prep
%setup -q
%patch0 -p1 -b .pngfix
%patch1 -p1 -b .CVE-2014-1624

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT 

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root=$RPM_BUILD_ROOT
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT 

%check
nosetests

%if 0%{?with_python3}
pushd %{py3dir}
nosetests
popd
%endif # with_python3

%clean
rm -rf $RPM_BUILD_ROOT 

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO
%{python_sitelib}/xdg
%{python_sitelib}/pyxdg-*.egg-info

%if 0%{?with_python3}
%files -n python3-pyxdg
%doc AUTHORS COPYING ChangeLog README TODO
%{python3_sitelib}/xdg
%{python3_sitelib}/pyxdg-*.egg-info
%endif #with_python3

%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 0.25-2
- Initial build

