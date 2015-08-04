%global with_python3 1

#uncomment next line for a release candidate or a beta
%global relc %{nil}

Name:           numpy
Version:        1.9.2
Release:        2%{?dist}
Epoch:          1
Summary:        A fast multidimensional array facility for Python

Group:          Development/Languages
# Everything is BSD except for class SafeEval in numpy/lib/utils.py which is Python
License:        BSD and Python
URL:            http://www.numpy.org/
Source0:        http://downloads.sourceforge.net/numpy/%{name}-%{version}%{?relc}.tar.gz

BuildRequires:  python2-devel lapack-devel python-setuptools gcc-gfortran atlas-devel python-nose
Requires:       python-nose
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
%endif
BuildRequires:  Cython

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.

%package f2py
Summary:        f2py for numpy
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       python-devel
Provides:       f2py = %{version}-%{release}
Obsoletes:      f2py <= 2.45.241_1927

%description f2py
This package includes a version of f2py that works properly with NumPy.

%if 0%{?with_python3}
%package -n python3-numpy
Summary:        A fast multidimensional array facility for Python

Group:          Development/Languages
License:        BSD
%description -n python3-numpy
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.

%package -n python3-numpy-f2py
Summary:        f2py for numpy
Group:          Development/Libraries
Requires:       python3-numpy = %{epoch}:%{version}-%{release}
Requires:       python3-devel
Provides:       python3-f2py = %{version}-%{release}
Obsoletes:      python3-f2py <= 2.45.241_1927

%description -n python3-numpy-f2py
This package includes a version of f2py that works properly with NumPy.
%endif # with_python3

%prep
%setup -q -n %{name}-%{version}%{?relc}

# workaround for rhbz#849713
# http://mail.scipy.org/pipermail/numpy-discussion/2012-July/063530.html
rm numpy/distutils/command/__init__.py && touch numpy/distutils/command/__init__.py

# Atlas 3.10 library names
%if 0%{?fedora} >= 21
cat >> site.cfg <<EOF
[atlas]
library_dirs = %{_libdir}/atlas
atlas_libs = satlas
EOF
%endif

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
pushd %{py3dir}
env ATLAS=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python3} setup.py build
popd
%endif # with _python3

env ATLAS=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python} setup.py build

%install
# first install python3 so the binaries are overwritten by the python2 ones
%if 0%{?with_python3}
pushd %{py3dir}
#%%{__python} setup.py install -O1 --skip-build --root %%{buildroot}
# skip-build currently broken, this works around it for now
env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python3} setup.py install --root %{buildroot}
pushd %{buildroot}%{_bindir} &> /dev/null
popd &> /dev/null

popd
%endif # with_python3

#%%{__python} setup.py install -O1 --skip-build --root %%{buildroot}
# skip-build currently broken, this works around it for now
env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python} setup.py install --root %{buildroot}
pushd %{buildroot}%{_bindir} &> /dev/null
# symlink for anyone who was using f2py.numpy
ln -s f2py f2py.numpy
popd &> /dev/null
install -D -p -m 0644 doc/f2py/f2py.1 %{buildroot}%{_mandir}/man1/f2py.1

#symlink for includes, BZ 185079
mkdir -p %{buildroot}/usr/include
ln -s %{python_sitearch}/%{name}/core/include/numpy/ %{buildroot}/usr/include/numpy


%check
pushd doc &> /dev/null
PYTHONPATH="%{buildroot}%{python_sitearch}" %{__python} -c "import pkg_resources, numpy ; numpy.test()" \
%ifarch s390 s390x
|| :
%endif
# don't remove this comment
popd &> /dev/null

%if 0%{?with_python3}
pushd doc &> /dev/null
# there is no python3-nose yet
PYTHONPATH="%{buildroot}%{python3_sitearch}" %{__python3} -c "import pkg_resources, numpy ; numpy.test()" \
%ifarch s390 s390x
|| :
%endif
# don't remove this comment
popd &> /dev/null

%endif # with_python3


%files
%doc LICENSE.txt README.txt THANKS.txt DEV_README.txt COMPATIBILITY site.cfg.example
%dir %{python_sitearch}/%{name}
%{python_sitearch}/%{name}/*.py*
%{python_sitearch}/%{name}/core
%{python_sitearch}/%{name}/distutils
%{python_sitearch}/%{name}/doc
%{python_sitearch}/%{name}/fft
%{python_sitearch}/%{name}/lib
%{python_sitearch}/%{name}/linalg
%{python_sitearch}/%{name}/ma
%{python_sitearch}/%{name}/random
%{python_sitearch}/%{name}/testing
%{python_sitearch}/%{name}/tests
%{python_sitearch}/%{name}/compat
%{python_sitearch}/%{name}/matrixlib
%{python_sitearch}/%{name}/polynomial
%{python_sitearch}/%{name}-*.egg-info
%{_includedir}/numpy

%files f2py
%doc doc/f2py/*.txt
%{_mandir}/man*/*
%{_bindir}/f2py
%{_bindir}/f2py.numpy
%{python_sitearch}/%{name}/f2py

%if 0%{?with_python3}
%files -n python3-numpy
%doc LICENSE.txt README.txt THANKS.txt DEV_README.txt COMPATIBILITY site.cfg.example
%{python3_sitearch}/%{name}/__pycache__
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/%{name}/*.py*
%{python3_sitearch}/%{name}/core
%{python3_sitearch}/%{name}/distutils
%{python3_sitearch}/%{name}/doc
%{python3_sitearch}/%{name}/fft
%{python3_sitearch}/%{name}/lib
%{python3_sitearch}/%{name}/linalg
%{python3_sitearch}/%{name}/ma
%{python3_sitearch}/%{name}/random
%{python3_sitearch}/%{name}/testing
%{python3_sitearch}/%{name}/tests
%{python3_sitearch}/%{name}/compat
%{python3_sitearch}/%{name}/matrixlib
%{python3_sitearch}/%{name}/polynomial
%{python3_sitearch}/%{name}-*.egg-info

%files -n python3-numpy-f2py
%{_bindir}/f2py3
%{python3_sitearch}/%{name}/f2py
%endif # with_python3


%changelog
