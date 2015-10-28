%global with_python3 1

%global prever a5

%{!?python_sitearch: %global python_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

# tracer.so is a private object, don't include it in the provides
%global _use_internal_dependency_generator 0
%global __find_provides /bin/sh -c "%{_rpmconfigdir}/find-provides | grep -v -E '(tracer.so)' || /bin/true"
%global __find_requires /bin/sh -c "%{_rpmconfigdir}/find-requires | grep -v -E '(tracer.so)' || /bin/true"

Name:           python-coverage
Summary:        Code coverage testing module for Python
Version:        4.0
Release:        0.8.%{?prever}%{?dist}
License:        BSD and (MIT or GPLv2)
URL:            http://nedbatchelder.com/code/modules/coverage.html
Source0:        http://pypi.python.org/packages/source/c/coverage/coverage-%{version}%{?prever}.tar.gz
# https://bitbucket.org/ned/coveragepy/issue/363/annotate-command-hits-unicode-happy-fun
Patch0:		python-coverage-4.0a5-unicodefix.patch
BuildRequires:  python-setuptools, python2-devel
Requires:       python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-setuptools, python3-devel
%endif # with_python3

%description
Coverage.py is a Python module that measures code coverage during Python 
execution. It uses the code analysis tools and tracing hooks provided in the 
Python standard library to determine which lines are executable, and which 
have been executed.

%if 0%{?with_python3}
%package -n python3-coverage
Summary:        Code coverage testing module for Python 3
# As the "coverage" executable requires the setuptools at runtime (#556290),
# so the "python3-coverage" executable requires python3-setuptools:
Requires:       python3-setuptools

%description -n python3-coverage
Coverage.py is a Python 3 module that measures code coverage during Python
execution. It uses the code analysis tools and tracing hooks provided in the 
Python standard library to determine which lines are executable, and which 
have been executed.
%endif # with_python3

%prep
%setup -q -n coverage-%{version}%{?prever}
%patch0 -p1

find . -type f -exec chmod 0644 \{\} \;
sed -i 's/\r//g' README.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # if with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # if with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/%{_bindir}/coverage %{buildroot}/%{_bindir}/python3-coverage
popd
%endif # if with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}

# rename binaries, make compat symlinks
pushd %{buildroot}%{_bindir}
mv coverage python-coverage

rm -rf coverage-2* coverage2

for i in python2-coverage coverage coverage2 coverage-%{?python2_shortver}; do
  ln -s python-coverage $i
done

rm -rf coverage-3* coverage3

for i in coverage3 coverage-%{?python3_shortver}; do
  ln -s	python3-coverage $i
done
popd

%files
%doc README.txt
%{_bindir}/coverage
%{_bindir}/coverage2
%{_bindir}/coverage-2*
%{_bindir}/python-coverage
%{_bindir}/python2-coverage
%{python_sitearch}/coverage/
%{python_sitearch}/coverage*.egg-info/

%if 0%{?with_python3}
%files -n python3-coverage
%{_bindir}/coverage-3*
%{_bindir}/coverage3
%{_bindir}/python3-coverage
%{python3_sitearch}/coverage/
%{python3_sitearch}/coverage*.egg-info/
%endif # if with_python3


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.0-0.8.a5
- Rebuild for new 4.0 release.

