%global with_python3 1

%{!?__python2: %global __python2 /usr/bin/python2}
%global srcname hypothesis


Name:           python-%{srcname}
Version:        3.4.0
Release:        2%{?dist}
Summary:        A library for property based testing

License:        MPLv2.0
URL:            https://github.com/DRMacIver/hypothesis
Source0:        https://github.com/DRMacIver/hypothesis/archive/%{version}.tar.gz#/hypothesis-%{version}.tar.gz
# disable Sphinx extensions that require Internet access
Patch0:         %{srcname}-2.0.0-offline.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-sphinx
BuildRequires:  python-enum34

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

%description
Hypothesis is a library for testing your Python code against a much
larger range of examples than you would ever want to write by
hand. It’s based on the Haskell library, Quickcheck, and is designed
to integrate seamlessly into your existing Python unit testing work
flow.


%package     -n python2-%{srcname}
Summary:        A library for property based testing
Obsoletes:      python-%{srcname} < 1.11.1-1
Requires:       python-enum34

%if 0%{?with_python3}
%{?python_provide:%python_provide python2-%{srcname}}
Suggests:       numpy
Suggests:       pytz
%else
Provides:       python-hypothesis = %{version}-%{release}
%endif

%description -n python2-%{srcname}
Hypothesis is a library for testing your Python code against a much
larger range of examples than you would ever want to write by
hand. It’s based on the Haskell library, Quickcheck, and is designed
to integrate seamlessly into your existing Python unit testing work
flow.


%if 0%{?with_python3}
%package     -n python3-%{srcname}
Summary:        A library for property based testing
%{?python_provide:%python_provide python3-%{srcname}}

Suggests:       python3-numpy
Suggests:       python3-pytz

%description -n python3-%{srcname}
Hypothesis is a library for testing your Python code against a much
larger range of examples than you would ever want to write by
hand. It’s based on the Haskell library, Quickcheck, and is designed
to integrate seamlessly into your existing Python unit testing work
flow.
%endif


%prep
%autosetup -n %{srcname}-python-%{version} -p1

# remove shebang, mergedbs gets installed in sitelib
%{__sed} -i -e 1,2d src/hypothesis/tools/mergedbs.py


%build
%if 0%{?with_python3}
%py2_build
%py3_build
READTHEDOCS=True sphinx-build -b man docs docs/_build/man
%else
%{__python2} setup.py build
%endif


%install
%if 0%{?with_python3}
%py2_install
%py3_install
%{__install} -Dp -m 644 docs/_build/man/hypothesis.1 \
             $RPM_BUILD_ROOT%{_mandir}/man1/hypothesis.1
%else
%{__python2} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}
%endif


%files -n python2-%{srcname}
%license LICENSE.txt
%doc README.rst
%{python2_sitelib}/*
%if 0%{?with_python3}
%{_mandir}/man1/hypothesis.1*
%endif

%if 0%{?with_python3}
%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/*
%{_mandir}/man1/hypothesis.1*
%endif

%changelog
* Fri Jul 08 2016 xiaotian.wu@i-soft.com.cn - 3.4.0-2
- rebuilt

* Fri Jul 08 2016 xiaotian.wu@i-soft.com.cn - 3.4.0-1
- init
