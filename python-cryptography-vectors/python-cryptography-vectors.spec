%global with_python3 1

%global modname cryptography-vectors
%global pymodname cryptography_vectors

Name:               python-%{modname}
Version:            1.3.1
Release:            1%{?dist}
Summary:            Test vectors for the cryptography package

License:            ASL 2.0 or BSD
URL:                http://pypi.python.org/pypi/cryptography-vectors
Source0:            https://pypi.python.org/packages/source/c/%{modname}/cryptography_vectors-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python2-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:      python3-devel python3-setuptools
%endif

%description
Test vectors for the cryptography package.

The only purpose of this package is to be a building requirement for
python-cryptography, otherwise it has no use. Don’t install it unless
you really know what you are doing.

%package -n  python2-%{modname}
Group:          Development/Libraries
Summary:        Test vectors for the cryptography package
Obsoletes:      python-cryptography-vectors <= %{version}-%{release}

%if 0%{?with_python3}
%{?python_provide:%python_provide python2-%{modname}}
%else
Provides:       python-%{modname}
%endif

%description -n python2-%{modname}
Test vectors for the cryptography package.

The only purpose of this package is to be a building requirement for
python-cryptography, otherwise it has no use. Don’t install it unless
you really know what you are doing.

%if 0%{?with_python3}
%package -n  python3-%{modname}
Group:          Development/Libraries
Summary:        Test vectors for the cryptography package

%{?python_provide:%python_provide python3-%{modname}}

%description -n python3-%{modname}
Test vectors for the cryptography package.

The only purpose of this package is to be a building requirement for
python-cryptography, otherwise it has no use. Don’t install it unless
you really know what you are doing.
%endif

%prep
%setup -q -n %{pymodname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
%if 0%{?with_python3}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%files -n python2-%{modname}
%doc LICENSE
%{python2_sitelib}/%{pymodname}/
%{python2_sitelib}/%{pymodname}-%{version}*

%if 0%{?with_python3}
%files -n python3-%{modname}
%doc LICENSE
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}*
%endif

%changelog
* Fri Jul 08 2016 xiaotian.wu@i-soft.com.cn - 1.3.1-1
- update to 1.3.1

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 0.8.2-3
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.8.2-2
- Rebuild for new 4.0 release.

* Thu Oct 08 2015 Cjacker <cjacker@foxmail.com>
- downgrade from yetist. 
