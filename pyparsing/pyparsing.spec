%global with_python3 1

Summary:        An object-oriented approach to text processing
Name:           pyparsing
Version:        2.0.6
Release:        2%{?dist}
Group:          Development/Libraries
License:        MIT
URL:            http://pyparsing.wikispaces.com/
Source0:        http://downloads.sourceforge.net/pyparsing/pyparsing-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  dos2unix
BuildRequires:  python-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

%description
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

%package        doc
Summary:        Documentation for pyparsing
Group:          Development/Libraries

%description    doc
The package contains documentation for pyparsing.

%if 0%{?with_python3}
%package     -n python3-pyparsing
Summary:        An object-oriented approach to text processing (Python 3 version)
Group:          Development/Libraries

%description -n python3-pyparsing
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

This is the Python 3 version.
%endif

%prep
%setup -q
mv docs/pyparsingClassDiagram.PNG docs/pyparsingClassDiagram.png
rm docs/pyparsingClassDiagram.JPG
dos2unix -k CHANGES LICENSE README

%build
%{py2_build}
%if 0%{?with_python3}
%{py3_build}
%endif

%install
# Install python 3 first, so that python 2 gets precedence:
%if 0%{?with_python3}
%{py3_install}
%endif
%{py2_install}

%files
%license LICENSE
%doc CHANGES README
%{python_sitelib}/pyparsing*egg-info
%{python_sitelib}/pyparsing.py*

%if 0%{?with_python3}
%files -n python3-pyparsing
%license LICENSE
%doc CHANGES README LICENSE
%{python3_sitelib}/pyparsing*egg-info
%{python3_sitelib}/pyparsing.py*
%{python3_sitelib}/__pycache__/pyparsing*
%endif

%files doc
%license LICENSE
%doc CHANGES README HowToUsePyparsing.html docs examples htmldoc

%changelog
* Mon Nov 23 2015 Cjacker <cjacker@foxmail.com> - 2.0.6-2
- Update

