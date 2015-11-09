%global with_python3 1

Name:           babel
Version:        1.3
Release:        10%{?dist}
Summary:        Tools for internationalizing Python applications

License:        BSD
URL:            http://babel.pocoo.org/
Source0:        https://pypi.python.org/packages/source/B/Babel/Babel-%{version}.tar.gz
Patch0:         babel-remove-pytz-version.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  pytz

# build the documentation
BuildRequires:  make
BuildRequires:  python-sphinx

Requires:       python-babel
Requires:       python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytz
%endif

%description
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%package -n python-babel
Summary:        Library for internationalizing Python applications

Requires:       python-setuptools
Requires:       pytz

%description -n python-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.

%if 0%{?with_python3}
%package -n python3-babel
Summary:        Library for internationalizing Python applications

Requires:       python3-setuptools
Requires:       python3-pytz

%description -n python3-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.
%endif

%package doc
Summary:        Documentation for Babel
Provides:       python-babel-doc = %{version}-%{release}
%if 0%{?with_python3}
Provides:       python3-babel-doc = %{version}-%{release}
%endif

%description doc
Documentation for Babel

%prep
%setup0 -q -n Babel-%{version}
%patch0 -p1

chmod a-x babel/messages/frontend.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -r . %{py3dir}
%endif

%build
%{__python} setup.py build

# build the docs and remove all source files (.rst, Makefile) afterwards
cd docs
make html
mv _build/html .
rm -rf _* api *.rst conf.py objects.inv Makefile make.bat
mv html/* .
rm -rf html

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}
# install python3 build before python2 build so executables from the former
# don't overwrite those from the latter
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --no-compile --root %{buildroot}
popd
%endif

%{__python} setup.py install --skip-build --no-compile --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README AUTHORS
%{_bindir}/pybabel

%files -n python-babel
%defattr(-,root,root,-)
%{python_sitelib}/Babel-%{version}-py*.egg-info
%{python_sitelib}/babel

%if 0%{?with_python3}
%files -n python3-babel
%defattr(-,root,root,-)
%{python3_sitelib}/Babel-%{version}-py*.egg-info
%{python3_sitelib}/babel
%endif

%files doc
%doc docs/*

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.3-10
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.3-9
- Rebuild for new 4.0 release.

