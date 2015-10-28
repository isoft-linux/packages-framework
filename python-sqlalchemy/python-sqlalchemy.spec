%global with_python3 1
%global srcname SQLAlchemy

Name:           python-sqlalchemy
Version:        1.0.6
Release:        2%{?dist}
Summary:        Modular and flexible ORM library for python

License:        MIT
URL:            http://www.sqlalchemy.org/
Source0:        http://pypi.python.org/packages/source/S/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python2-devel >= 2.6
BuildRequires:  python-setuptools
BuildRequires:  python-mock
BuildRequires:  pytest

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
%endif

%description
SQLAlchemy is an Object Relational Mappper (ORM) that provides a flexible,
high-level interface to SQL databases.  Database and domain concepts are
decoupled, allowing both sides maximum flexibility and power. SQLAlchemy
provides a powerful mapping layer that can work as automatically or as manually
as you choose, determining relationships based on foreign keys or letting you
define the join conditions explicitly, to bridge the gap between database and
domain.

This package includes the python 2 version of the module.

%if 0%{?with_python3}
%package -n python3-sqlalchemy
Summary:        Modular and flexible ORM library for python

%description -n python3-sqlalchemy
SQLAlchemy is an Object Relational Mappper (ORM) that provides a flexible,
high-level interface to SQL databases.  Database and domain concepts are
decoupled, allowing both sides maximum flexibility and power. SQLAlchemy
provides a powerful mapping layer that can work as automatically or as manually
as you choose, determining relationships based on foreign keys or letting you
define the join conditions explicitly, to bridge the gap between database and
domain.

This package includes the python 3 version of the module.
%endif # with_python3

# Filter unnecessary dependencies
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\\.so$

%prep
%setup -q -n %{srcname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
CFLAGS="%{optflags}" %{__python2} setup.py --with-cextensions build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py --with-cextensions build
popd
%endif

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python2_sitelib}
%{__python2} setup.py --with-cextensions install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
mkdir -p %{buildroot}%{python3_sitelib}
%{__python3} setup.py --with-cextensions install --skip-build --root %{buildroot}
popd
%endif

# remove unnecessary scripts for building documentation
rm -rf doc/build

%clean
rm -rf %{buildroot}

%check
pytest2="py.test-$(%{__python2} -c 'from __future__ import print_function; import sys; vi=sys.version_info; print("{0}.{1}".format(vi.major, vi.minor))')"
PYTHONPATH=. "$pytest2" test

%if 0%{?with_python3}
pushd %{py3dir}
pytest3="py.test-$(%{__python3} -c 'from __future__ import print_function; import sys; vi=sys.version_info; print("{0}.{1}".format(vi.major, vi.minor))')"
PYTHONPATH=. "$pytest3" test
popd
%endif


%files
%defattr(-,root,root,-)
%doc README.rst LICENSE PKG-INFO CHANGES doc examples
%{python2_sitearch}/*

%if 0%{?with_python3}
%files -n python3-sqlalchemy
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO doc examples
%{python3_sitearch}/*
%endif # with_python3

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.6-2
- Rebuild for new 4.0 release.

