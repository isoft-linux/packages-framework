%global with_python3 1

%global mod_name Whoosh

Name:           python-whoosh
Version:        2.5.7
Release:        5%{?dist}
Summary:        Fast, pure-Python full text indexing, search, and spell checking library 

License:        BSD 
URL:            http://pythonhosted.org/Whoosh/
Source0:        https://pypi.python.org/packages/source/W/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  pytest 
BuildRequires:  python-sphinx

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pytest
BuildRequires: python3-sphinx
%endif

%description
Whoosh is a fast, featureful full-text indexing and searching library
implemented in pure Python. Programmers can use it to easily add search
functionality to their applications and websites. Every part of how Whoosh
works can be extended or replaced to meet your needs exactly.

%if 0%{?with_python3}
%package -n python3-whoosh
Summary:    Fast, Python3 full text indexing, search, and spell checking library

%description -n python3-whoosh
Whoosh is a fast, featureful full-text indexing and searching library
implemented in pure Python. Programmers can use it to easily add search
functionality to their applications and websites. Every part of how Whoosh
works can be extended or replaced to meet your needs exactly.
%endif

%prep
%setup -q -n %{mod_name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build
#sphinx-build docs/source docs/html
#rm -f docs/html/.buildinfo
#rm -rf docs/html/.doctrees

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
#rm -f docs/html/.buildinfo
#rm -rf docs/html/.doctrees
popd
%endif

%check
#%{__python2} setup.py test
#
#%if 0%{?with_python3}
#pushd %{py3dir}
#%{__python3} setup.py test
#popd
#%endif

%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif

%files
%doc docs/html/ README.txt LICENSE.txt
%{python2_sitelib}/*.egg-info/
%{python2_sitelib}/whoosh

%if 0%{?with_python3}
%files -n python3-whoosh
%doc README.txt LICENSE.txt docs/html/
%{python3_sitelib}/whoosh
%{python3_sitelib}/*.egg-info/
%endif

%changelog
