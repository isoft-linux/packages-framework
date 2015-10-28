%global with_python3 1
Name:		pyxattr
Summary:	Extended attributes library wrapper for Python
Version:	0.5.3
Release:	5
License:	LGPLv2+
URL:		http://pyxattr.k1024.org/
Source:		https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Patch0:		0001-use-Py_ssize_t.patch
BuildRequires:	libattr-devel
BuildRequires:	python2-devel, python-setuptools
%if %{?with_python3}
BuildRequires:	python3-devel, python3-setuptools
%endif # with_python3

%description
Python extension module wrapper for libattr. It allows to query, list,
add and remove extended attributes from files and directories.

%if %{?with_python3}
%package -n python3-%{name}
Summary:	Extended attributes library wrapper for Python 3

%description -n python3-%{name}
Python extension module wrapper for libattr. It allows to query, list,
add and remove extended attributes from files and directories.

Python 3 version.
%endif # with_python3

%prep
%setup -q
%patch0 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
CFLAGS="%{optflags}" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python2} setup.py install --root="%{buildroot}" --prefix="%{_prefix}"

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --root="%{buildroot}" --prefix="%{_prefix}"
popd
%endif # with_python3

%check
# selinux in koji produces unexpected xattrs for tests
export TEST_IGNORE_XATTRS=security.selinux

%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

%files
%defattr(0644,root,root,0755)
%{python2_sitearch}/xattr.so
%{python2_sitearch}/*egg-info
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README

%if %{?with_python3}
%files -n python3-%{name}
%defattr(0644,root,root,0755)
%{python3_sitearch}/xattr.cpython-??m.so
%{python3_sitearch}/*egg-info
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README
%endif # with_python3

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.5.3-5
- Rebuild for new 4.0 release.

* Wed Aug 26 2015 Cjacker <cjacker@foxmail.com>
- initial build, from fedora.
