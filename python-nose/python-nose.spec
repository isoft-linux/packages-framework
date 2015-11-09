%{!?python3_version: %global python3_version %(%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])")}

%global with_python3 1


%global upstream_name nose

# Enable building without docs to avoid a circular dependency between this and python-sphinx
%global with_docs 0 

Name:           python-nose
Version:        1.3.7
Release:        4%{?dist}
Summary:        Discovery-based unittest extension for Python

License:        LGPLv2+ and Public Domain
URL:            http://somethingaboutorange.com/mrl/projects/nose/
Source0:        http://pypi.python.org/packages/source/n/nose/nose-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-coverage >= 3.4-1
%endif
BuildRequires: python-setuptools
BuildRequires: dos2unix
BuildRequires:  python-coverage >= 3.4-1
Requires:       python-setuptools

%description
nose extends the test loading and running features of unittest, making
it easier to write, find and run tests.

By default, nose will run tests in files or directories under the
current working directory whose names include "test" or "Test" at a
word boundary (like "test_this" or "functional_test" or "TestClass"
but not "libtest"). Test output is similar to that of unittest, but
also includes captured stdout output from failing tests, for easy
print-style debugging.

These features, and many more, are customizable through the use of
plugins. Plugins included with nose provide support for doctest, code
coverage and profiling, flexible attribute-based test selection,
output capture and more.

%package docs
Summary:        Nose Documentation
BuildRequires:  python-sphinx
Requires: python-nose

%description docs
Documentation for Nose

%if 0%{?with_python3}
%package -n python3-%{upstream_name}
Summary:        Discovery-based unittest extension for Python3
Requires:       python3-setuptools

%description -n python3-%{upstream_name}
nose extends the test loading and running features of unittest, making
it easier to write, find and run tests.

By default, nose will run tests in files or directories under the
current working directory whose names include "test" or "Test" at a
word boundary (like "test_this" or "functional_test" or "TestClass"
but not "libtest"). Test output is similar to that of unittest, but
also includes captured stdout output from failing tests, for easy
print-style debugging.

These features, and many more, are customizable through the use of
plugins. Plugins included with nose provide support for doctest, code
coverage and profiling, flexible attribute-based test selection,
output capture and more.

This package installs the nose module and nosetests3 program that can discover
python3 unittests.
%endif # with_python3

%prep
%setup -q -n %{upstream_name}-%{version}

dos2unix examples/attrib_plugin.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
rm %{buildroot}%{_bindir}/nosetests
mkdir -m 0755 -p %{buildroot}%{_mandir}/man1/
mv %{buildroot}%{_prefix}/man/man1/nosetests.1 %{buildroot}%{_mandir}/man1/nosetests-%{python3_version}.1
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot} \
           --install-data=%{_datadir}

%if 0%{?with_docs}
pushd doc
make html
rm -rf .build/html/.buildinfo .build/html/_sources
mv .build/html ..
rm -rf .build
popd
%endif # with_docs
cp -a doc reST
rm -rf reST/.static reST/.templates


%check
%{__python} selftest.py

#some test failed with python 3.5, 
#https://github.com/nose-devs/nose/issues/928

#%if 0%{?with_python3}
#pushd %{py3dir}
#export PYTHONPATH=`pwd`/build/lib
#%{__python3} setup.py build_tests
## Various selftests fail with Python 3.3b1; skip them for now using "-e"
## (reported upstream as https://github.com/nose-devs/nose/issues/538 )
#%{__python3} selftest.py \
#    -v
#popd
#%endif # with_python3

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG lgpl.txt NEWS README.txt
%{_bindir}/nosetests
%{_bindir}/nosetests-%{python_version}
%{_mandir}/man1/nosetests.1.gz
%{python_sitelib}/nose*

%if 0%{?with_python3}
%files -n python3-%{upstream_name}
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG lgpl.txt NEWS README.txt
%{_bindir}/nosetests-%{python3_version}
%{_mandir}/man1/nosetests-%{python3_version}.1.gz
%{python3_sitelib}/nose*
%endif

%files docs
%defattr(-,root,root,-)
%doc reST examples
%if 0%{?with_docs}
%doc html
%endif # with_docs

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.3.7-4
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.3.7-3
- Rebuild for new 4.0 release.

