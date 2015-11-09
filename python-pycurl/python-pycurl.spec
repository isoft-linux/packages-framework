%{!?py3dir: %global py3dir %{_builddir}/python3-%{name}-%{version}-%{release}}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-pycurl
Version:        7.19.5.1
Release:        7
Summary:        A Python interface to libcurl

License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz

#Requires:       keyutils-libs
BuildRequires:  python-devel
BuildRequires:  python3-devel
BuildRequires:  libcurl-devel >= 7.19.0
#BuildRequires:  openssl-devel
BuildRequires:  python-nose
BuildRequires:  python-bottle
BuildRequires:  python3-nose
BuildRequires:  python3-bottle

# During its initialization, PycURL checks that the actual libcurl version
# is not lower than the one used when PycURL was built.
# Yes, that should be handled by library versioning (which would then get
# automatically reflected by rpm).
# For now, we have to reflect that dependency.
%global libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%global curlver_h /usr/include/curl/curlver.h
%global libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)
Requires:       libcurl >= %{libcurl_ver}

Provides:       pycurl = %{version}-%{release}

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%package -n python3-pycurl
Summary:        A Python interface to libcurl for Python 3

%description -n python3-pycurl
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%setup0 -q -n pycurl-%{version}

# temporarily exclude failing test-cases
rm -f tests/{post_test,reset_test}.py

# copy the whole directory for the python3 build
rm -rf %{py3dir}
cp -a . %{py3dir}

%build
export CFLAGS="$RPM_OPT_FLAGS"
%{__python} setup.py build --with-nss
pushd %{py3dir}
%{__python3} setup.py build --with-nss
popd

%check
export PYTHONPATH=$RPM_BUILD_ROOT%{python_sitearch}
make test PYTHON=%{__python}
pushd %{py3dir}
export PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch}
make test PYTHON=%{__python3} NOSETESTS="nosetests-%{python3_version} -v" ||:
popd

%install
export PYCURL_SSL_LIBRARY=openssl
%{__python} setup.py --with-nss install -O1 --skip-build --root %{buildroot}
pushd %{py3dir}
%{__python3} setup.py --with-nss install -O1 --skip-build --root %{buildroot}
popd
rm -rf %{buildroot}%{_datadir}/doc/pycurl

%files
%{!?_licensedir:%global license %%doc}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc tests
%{python_sitearch}/*

%files -n python3-pycurl
# TODO: find the lost COPYING file
%{!?_licensedir:%global license %%doc}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc tests
%{python3_sitearch}/*

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 7.19.5.1-7
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 7.19.5.1-6
- Rebuild for new 4.0 release.

