%global with_python3 1

%global srcname distribute

%define run_check 0%{!?_without_check:1}
##%define run_check 0%{!?_with_check:0}

Name:		Cython
Version:	0.23
##Release:	4.b3%{?dist}
Release:	3%{?dist}
Summary:	A language for writing Python extension modules

%define upstreamversion %{version}
##%%define upstreamversion %{version}b3

License:	Python
URL:		http://www.cython.org
Source:		http://www.cython.org/release/Cython-%{upstreamversion}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3

%if 0%{run_check}
BuildRequires:	numpy libtool
%endif
Requires:	python

%description
This is a development version of Pyrex, a language
for writing Python extension modules.

For more info, see:

    Doc/About.html for a description of the language
    INSTALL.txt	   for installation instructions
    USAGE.txt	   for usage instructions
    Demos	   for usage examples

%if 0%{?with_python3}
%package -n python3-Cython
Summary:	A language for writing Python extension modules

%description -n python3-Cython
This is a development version of Pyrex, a language
for writing Python extension modules.

For more info, see:

    Doc/About.html for a description of the language
    INSTALL.txt	   for installation instructions
    USAGE.txt	   for usage instructions
    Demos	   for usage examples
%endif # with_python3

%prep
%setup -q -n %{name}-%{upstreamversion}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/bin/cython $RPM_BUILD_ROOT/usr/bin/cython3
mv $RPM_BUILD_ROOT/usr/bin/cygdb $RPM_BUILD_ROOT/usr/bin/cygdb3
rm -rf %{buildroot}%{python3_sitelib}/setuptools/tests
popd
%endif

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
rm -rf %{buildroot}%{python_sitelib}/setuptools/tests


%clean
rm -rf $RPM_BUILD_ROOT

%if 0%{run_check}
%check
%{__python} runtests.py

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3
%endif

%files
%{_bindir}/cython
%{_bindir}/cygdb
%{_bindir}/cythonize
%{python_sitearch}/Cython
%{python_sitearch}/cython.py*
%{python_sitearch}/pyximport
%{python_sitearch}/Cython*egg-info

%if 0%{?with_python3}
%files -n python3-Cython
%doc *.txt Demos Doc Tools
%{python3_sitearch}/*
%{_bindir}/cython3
%{_bindir}/cygdb3
%{python3_sitearch}/Cython*egg-info
%endif # with_python3
%doc *.txt Demos Doc Tools


%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 0.23-3
- Rebuild with python 3.5

* Sun Oct 25 2015 cjacker - 0.23-2
- Rebuild for new 4.0 release

