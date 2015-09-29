%global with_python3 1

Name:           python-enum34
Version:        1.0.4
Release:        2
Group:          Development/Libraries
Summary:        Backport of Python 3.4 Enum
License:        BSD
BuildArch:      noarch
URL:            https://pypi.python.org/pypi/enum34
Source0:        https://pypi.python.org/packages/source/e/enum34/enum34-%{version}.tar.gz

BuildRequires:  python2-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
%endif # if with_python3

%description
Python 3.4 introduced official support for enumerations.  This is a
backport of that feature to Python 3.3, 3.2, 3.1, 2.7, 2.5, 2.5, and 2.4.

An enumeration is a set of symbolic names (members) bound to unique,
constant values. Within an enumeration, the members can be compared by
identity, and the enumeration itself can be iterated over.

This module defines two enumeration classes that can be used to define
unique sets of names and values: Enum and IntEnum. It also defines one
decorator, unique, that ensures only unique member names are present
in an enumeration.

%if 0%{?with_python3}
%package -n python3-enum34
Summary:        Backport of Python 3.4 Enum
Group:          Development/Libraries

%description -n python3-enum34
Python 3.4 introduced official support for enumerations.  This is a
backport of that feature to Python 3.3, 3.2, 3.1, 2.7, 2.5, 2.5, and 2.4.

An enumeration is a set of symbolic names (members) bound to unique,
constant values. Within an enumeration, the members can be compared by
identity, and the enumeration itself can be iterated over.

This module defines two enumeration classes that can be used to define
unique sets of names and values: Enum and IntEnum. It also defines one
decorator, unique, that ensures only unique member names are present
in an enumeration.

%endif # with_python3

%prep
%setup -q -n enum34-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%{__python2} setup.py build

%check
pushd %{buildroot}/%{python2_sitelib}
%{__python2} enum/test_enum.py
popd
%if 0%{?with_python3}
pushd %{buildroot}/%{python3_sitelib}
%{__python3} enum/test_enum.py
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
# remove docs from sitelib, we'll put them in doc dir instead
rm -rf %{buildroot}%{python3_sitelib}/enum/{LICENSE,README,doc}
popd
%endif # with_python3
%{__python2} setup.py install --skip-build --root %{buildroot}
# remove docs from sitelib, we'll put them in doc dir instead
rm -rf %{buildroot}%{python2_sitelib}/enum/{LICENSE,README,doc}

%files
%doc PKG-INFO enum/LICENSE enum/README enum/doc/enum.rst
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-enum34
%doc PKG-INFO enum/LICENSE enum/README enum/doc/enum.rst
%{python3_sitelib}/*
%endif # with_python3

%changelog
