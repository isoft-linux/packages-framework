%global modulename html5lib
%global with_python3 1

Name:		python-%{modulename}
Summary:	A python based HTML parser/tokenizer
Version:	0.999
Release:	6
Epoch:		1
Group:		Development/Libraries
License:	MIT
URL:		https://pypi.python.org/pypi/%{modulename}

Source0:	https://pypi.python.org/packages/source/h/%{modulename}/%{modulename}-%{version}.tar.gz	

BuildArch:	noarch
Requires:	python-six
BuildRequires:	python-setuptools
BuildRequires:	python2-devel
BuildRequires:	python-nose
BuildRequires:	python-six

%description
A python based HTML parser/tokenizer based on the WHATWG HTML5 
specification for maximum compatibility with major desktop web browsers.

%if 0%{?with_python3}
%package -n python3-%{modulename}
Summary:	A python based HTML parser/tokenizer 
Group:		Development/Libraries 

Requires:	python3-six
BuildRequires:	python3-devel
BuildRequires:	python-tools
BuildRequires:	python3-nose
BuildRequires:	python3-six
BuildRequires:	python3-setuptools

%description -n python3-%{modulename}
A python based HTML parser/tokenizer based on the WHATWG HTML5 
specification for maximum compatibility with major desktop web browsers.
%endif


%prep
%setup -q -n %{modulename}-%{version} 

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
nosetests

%if 0%{?with_python3}
pushd %{py3dir}
nosetests-%{python3_version}
popd
%endif

%files
%doc CHANGES.rst README.rst LICENSE 
%{python_sitelib}/%{modulename}-*.egg-info
%{python_sitelib}/%{modulename}

%if 0%{?with_python3}
%files -n python3-%{modulename}
%doc CHANGES.rst LICENSE README.rst
%{python3_sitelib}/%{modulename}-*.egg-info
%{python3_sitelib}/%{modulename}
%endif 


%changelog
