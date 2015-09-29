%global with_python3 1

Name:           python-kitchen
Version:        1.2.1
Release:        3
Summary:        Small, useful pieces of code to make python coding easier

Group:          Development/Languages
License:        LGPLv2+
URL:            https://pypi.python.org/pypi/kitchen/
Source0:        https://fedorahosted.org/releases/k/i/kitchen/kitchen-%{version}.tar.gz

# http://git.io/8KLw1Q
Patch0:         python-kitchen-expose-base64-py34.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-nose
# For the subprocess test
# BuildRequires:  python-test

# sphinx needs to be more recent to build the html docs
BuildRequires: python-sphinx

# At present, chardet isn't present in epel but it's a soft dep
BuildRequires: python-chardet
Requires: python-chardet

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-nose
# BuildRequires:  python3-test
BuildRequires:  python3-sphinx
BuildRequires:  python3-chardet
%endif

%description
kitchen includes functions to make gettext easier to use, handling unicode
text easier (conversion with bytes, outputting xml, and calculating how many
columns a string takes), and compatibility modules for writing code that uses
python-2.7 modules but needs to run on python-2.3.

%package doc
Summary:        API documentation for the Kitchen python2 module
# Currently discussing guidelines about doc subpackages Requiring the main package:
# https://lists.fedoraproject.org/pipermail/packaging/2013-June/009191.html
#Requires: %{name} = %{version}-%{release}
%description doc
kitchen includes functions to make gettext easier to use, handling unicode
text easier (conversion with bytes, outputting xml, and calculating how many
columns a string takes), and compatibility modules for writing code that uses
python-2.7 modules but needs to run on python-2.3.

This package contains the API documenation for programming with the
python-2 version of the kitchen library.

%if 0%{?with_python3}
%package -n python3-kitchen
Summary:    Small, useful pieces of code to make python 3 coding easier
Group:      Development/Languages

Requires:   python3
Requires:   python3-chardet

%description -n python3-kitchen
kitchen includes functions to make gettext easier to use, handling unicode
text easier (conversion with bytes, outputting xml, and calculating how many
columns a string takes).

This is the python3 version of the kitchen module.

%package -n python3-kitchen-doc
Summary:    API documentation for the Kitchen python3 module
#Requires: %{name} = %{version}-%{release}
%description -n python3-kitchen-doc
kitchen includes functions to make gettext easier to use, handling unicode
text easier (conversion with bytes, outputting xml, and calculating how many
columns a string takes).

This package contains the API documenation for programming with the
python-3 version of the kitchen library.
%endif


%prep
%setup -q -n kitchen-%{version}

%patch0 -p1

# Remove bundled egg info, if any.
rm -rf *.egg*

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

# Build docs

sphinx-build kitchen2/docs/ build/sphinx/html
cp -pr build/sphinx/html .
rm -rf html/.buildinfo

%if 0%{?with_python3}
pushd %{py3dir}
sphinx-build-3 kitchen3/docs/ build/sphinx/html
cp -pr build/sphinx/html .
rm -rf html/.buildinfo
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%check
# In current mock, the PATH isn't being reset.  This causes failures in some
# subprocess tests as a check tests /root/bin/PROGRAM and fails with Permission
# Denied instead of File Not Found.  reseting the PATH works around this.
#PATH=/bin:/usr/bin
#PYTHONPATH=.:kitchen2/ nosetests kitchen2/tests/

%if 0%{?with_python3}
pushd %{py3dir}
#PYTHONPATH=.:kitchen3/ nosetests-%{python3_version} kitchen3/tests/
popd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.rst NEWS.rst COPYING COPYING.LESSER
%{python2_sitelib}/*

%files doc
%doc COPYING COPYING.LESSER kitchen2/docs/*
%doc html

%if 0%{?with_python3}
%files -n python3-kitchen
%defattr(-,root,root,-)
%doc README.rst NEWS.rst COPYING COPYING.LESSER
%{python3_sitelib}/*

%files -n python3-kitchen-doc
%doc COPYING COPYING.LESSER kitchen3/docs/*
%doc html
%endif

%changelog
