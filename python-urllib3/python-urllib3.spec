%global commit a91975b77a2e28394859487fe5ebbf4a3a74e634
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global checkout 20150503git%{shortcommit}

%global gh_owner shazow
%global gh_project urllib3

%global with_python3 1

%global srcname urllib3

Name:           python-%{srcname}
Version:        1.10.4
Release:        4.%{checkout}%{?dist}
Summary:        Python HTTP library with thread-safe connection pooling and file post

License:        MIT
URL:            http://urllib3.readthedocs.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{commit}/%{gh_project}-%{commit}.tar.gz
Source1:        ssl_match_hostname_py3.py
Patch0:         python-urllib3-pyopenssl.patch

# Remove logging-clear-handlers from setup.cfg because it's not available in RHEL6's nose
Patch100:       python-urllib3-old-nose-compat.patch

BuildArch:      noarch

Requires:       ca-certificates

BuildRequires:  python2-devel

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # with_python3


%description
Python HTTP module with connection pooling and file POST abilities.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Requires:       ca-certificates
Requires:       python3-six
Summary:        Python3 HTTP library with thread-safe connection pooling and file post
%description -n python3-%{srcname}
Python3 HTTP module with connection pooling and file POST abilities.
%endif # with_python3


%prep
#%%setup -q -n %{srcname}-%{version}
%setup -q -n %{gh_project}-%{commit}

# Drop the dummyserver tests in koji.  They fail there in real builds, but not
# in scratch builds (weird).
rm -rf test/with_dummyserver/

%if 0%{?rhel} && 0%{?rhel} <= 6
%patch100 -p1
%endif

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}
%{__python2} setup.py install --skip-build --root %{buildroot}

rm -rf %{buildroot}/%{python2_sitelib}/urllib3/packages/six.py*
rm -rf %{buildroot}/%{python2_sitelib}/urllib3/packages/ssl_match_hostname/

mkdir -p %{buildroot}/%{python2_sitelib}/urllib3/packages/
ln -s ../../six.py %{buildroot}/%{python2_sitelib}/urllib3/packages/six.py
ln -s ../../six.pyc %{buildroot}/%{python2_sitelib}/urllib3/packages/six.pyc
ln -s ../../six.pyo %{buildroot}/%{python2_sitelib}/urllib3/packages/six.pyo

ls -alh %{buildroot}/%{python2_sitelib}/urllib3/packages/
ls -alh %{buildroot}/%{python2_sitelib}

# dummyserver is part of the unittest framework
rm -rf %{buildroot}%{python2_sitelib}/dummyserver

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

rm -rf %{buildroot}/%{python3_sitelib}/urllib3/packages/six.py*
rm -rf %{buildroot}/%{python3_sitelib}/urllib3/packages/ssl_match_hostname/

mkdir -p %{buildroot}/%{python3_sitelib}/urllib3/packages/
ln -s ../../six.py %{buildroot}/%{python3_sitelib}/urllib3/packages/six.py
ln -s ../../six.pyc %{buildroot}/%{python3_sitelib}/urllib3/packages/six.pyc
ln -s ../../six.pyo %{buildroot}/%{python3_sitelib}/urllib3/packages/six.pyo
cp %{SOURCE1} %{buildroot}/%{python3_sitelib}/urllib3/packages/ssl_match_hostname.py

ls -alh %{buildroot}/%{python3_sitelib}

# dummyserver is part of the unittest framework
rm -rf %{buildroot}%{python3_sitelib}/dummyserver
popd
%endif # with_python3

%check
#nosetests
#
#%if 0%{?with_python3}
#pushd %{py3dir}
#nosetests-%{python3_version}
#popd
#
#rm -rf %{buildroot}/%{python3_sitelib}/__pycache__*
#%endif # with_python3

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc CHANGES.rst README.rst CONTRIBUTORS.txt
# For noarch packages: sitelib
%{python2_sitelib}/urllib3/
%{python2_sitelib}/urllib3-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
# For noarch packages: sitelib
%{python3_sitelib}/urllib3/
%{python3_sitelib}/urllib3-*.egg-info
%endif # with_python3

%changelog
