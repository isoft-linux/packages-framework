%global _with_python3 1

Name:           python-requests
Version:        2.7.0
Release:        2%{?dist}
Summary:        HTTP library, written in Python, for human beings

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/requests
Source0:        http://pypi.python.org/packages/source/r/requests/requests-%{version}.tar.gz
# Explicitly use the system certificates in ca-certificates.
# https://bugzilla.redhat.com/show_bug.cgi?id=904614
Patch0:         python-requests-system-cert-bundle.patch

# Remove an unnecessary reference to a bundled compat lib in urllib3
Patch1:         python-requests-remove-nested-bundling-dep.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-chardet
BuildRequires:  python-urllib3 >= 1.10

Requires:       ca-certificates
Requires:       python-chardet
Requires:       python-urllib3 >= 1.10

%description
Most existing Python modules for sending HTTP requests are extremely verbose and 
cumbersome. Python’s built-in urllib2 module provides most of the HTTP 
capabilities you should need, but the API is thoroughly broken. This library is 
designed to make HTTP requests easy for developers.

%if 0%{?_with_python3}
%package -n python3-requests
Summary: HTTP library, written in Python, for human beings
BuildRequires:  python3-devel
BuildRequires:  python3-chardet
BuildRequires:  python3-urllib3 >= 1.10
Requires:       python3-chardet
Requires:       python3-urllib3 >= 1.10

%description -n python3-requests
Most existing Python modules for sending HTTP requests are extremely verbose and
cumbersome. Python’s built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.
%endif

%prep
%setup -q -n requests-%{version}

%patch0 -p1
%patch1 -p1

# Unbundle the certificate bundle from mozilla.
rm -rf requests/cacert.pem

%if 0%{?_with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if 0%{?_with_python3}
pushd %{py3dir}
%{__python3} setup.py build

# Unbundle chardet and urllib3.  We replace these with symlinks to system libs.
rm -rf build/lib/requests/packages/chardet
rm -rf build/lib/requests/packages/urllib3

popd
%endif

%{__python} setup.py build

# Unbundle chardet and urllib3.  We replace these with symlinks to system libs.
rm -rf build/lib/requests/packages/chardet
rm -rf build/lib/requests/packages/urllib3

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?_with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
ln -s ../../chardet %{buildroot}/%{python3_sitelib}/requests/packages/chardet
ln -s ../../urllib3 %{buildroot}/%{python3_sitelib}/requests/packages/urllib3
popd
%endif

%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
ln -s ../../chardet %{buildroot}/%{python_sitelib}/requests/packages/chardet
ln -s ../../urllib3 %{buildroot}/%{python_sitelib}/requests/packages/urllib3

## The tests succeed if run locally, but fail in koji.
## They require an active network connection to query httpbin.org
%check

#%%{__python} test_requests.py
#%%if 0%%{?_with_python3}
#pushd %%{py3dir}
#%%{__python3} test_requests.py
#popd
#%%endif

# At very, very least, we'll try to start python and import requests
PYTHONPATH=. %{__python} -c "import requests"

%if 0%{?_with_python3}
pushd %{py3dir}
PYTHONPATH=. %{__python3} -c "import requests"
popd
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc NOTICE README.rst HISTORY.rst
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/requests
%{python_sitelib}/requests/*

%if 0%{?_with_python3}
%files -n python3-requests
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc NOTICE README.rst HISTORY.rst
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/requests/
%endif

%changelog
