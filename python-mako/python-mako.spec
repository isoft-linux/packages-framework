%global with_python3 1

%global upname Mako

Name: python-mako
Version: 1.0.1
Release: 2%{?dist}
Summary: Mako template library for Python

Group: Development/Languages
# Mostly MIT, but _ast_util.py is Python licensed.
# The documentation contains javascript for search licensed BSD or GPLv2
License: (MIT and Python) and (BSD or GPLv2)
URL: http://www.makotemplates.org/
Source0: https://pypi.python.org/packages/source/M/%{upname}/%{upname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-markupsafe
#BuildRequires: python-beaker
BuildRequires: python-nose
BuildRequires: python-mock
Requires: python-markupsafe
#Requires: python-beaker

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-markupsafe
#BuildRequires: python3-beaker
BuildRequires: python3-mock
BuildRequires: python3-nose
BuildRequires: /usr/bin/2to3
%endif # if with_python3

%description
Mako is a template library written in Python. It provides a familiar, non-XML
syntax which compiles into Python modules for maximum performance. Mako's
syntax and API borrows from the best ideas of many others, including Django
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded
Python (i.e. Python Server Page) language, which refines the familiar ideas of
componentized layout and inheritance to produce one of the most straightforward
and flexible models available, while also maintaining close ties to Python
calling and scoping semantics.

%package doc
Summary: Documentation for the Mako template library for Python
Group: Documentation
License: (MIT and Python) and (BSD or GPLv2)
Requires:   %{name} = %{version}-%{release}

%description doc
Mako is a template library written in Python. It provides a familiar, non-XML
syntax which compiles into Python modules for maximum performance. Mako's
syntax and API borrows from the best ideas of many others, including Django
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded
Python (i.e. Python Server Page) language, which refines the familiar ideas of
componentized layout and inheritance to produce one of the most straightforward
and flexible models available, while also maintaining close ties to Python
calling and scoping semantics.

This package contains documentation in text and HTML formats.


%if 0%{?with_python3}
%package -n python3-mako
Summary: Mako template library for Python 3
Group: Development/Languages
#Requires: python3-beaker
Requires: python3-markupsafe

%description -n python3-mako
Mako is a template library written in Python. It provides a familiar, non-XML
syntax which compiles into Python modules for maximum performance. Mako's
syntax and API borrows from the best ideas of many others, including Django
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded
Python (i.e. Python Server Page) language, which refines the familiar ideas of
componentized layout and inheritance to produce one of the most straightforward
and flexible models available, while also maintaining close ties to Python
calling and scoping semantics.

This package contains the mako module built for use with python3.
%endif # with_python3

%prep
%setup -q -n Mako-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
2to3 --no-diffs -w mako test
%{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/%{_bindir}/mako-render %{buildroot}/%{_bindir}/python3-mako-render
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}

# These are supporting files for building the docs.  No need to ship
rm -rf doc/build

%check
PYTHONPATH=$(pwd) nosetests

%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=$(pwd) nosetests-%{python3_version}
popd
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README.rst examples
%{_bindir}/mako-render
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-mako
%defattr(-,root,root,-)
%doc CHANGES LICENSE README.rst examples
%{_bindir}/python3-mako-render
%{python3_sitelib}/*
%endif

%files doc
%doc doc


%changelog
