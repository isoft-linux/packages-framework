%global module_name backports.ssl_match_hostname

Name:           python-backports-ssl_match_hostname
Version:        3.4.0.2
Release:        5%{?dist}
Summary:        The ssl.match_hostname() function from Python 3

License:        Python
URL:            https://bitbucket.org/brandon/backports.ssl_match_hostname
Source0:        http://pypi.python.org/packages/source/b/%{module_name}/%{module_name}-%{version}.tar.gz

# https://bitbucket.org/brandon/backports.ssl_match_hostname/pull-request/1
Patch0:         python-backports-ssl_match_hostname-namespace.patch
Patch1:         backports.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-backports

%description
The Secure Sockets layer is only actually secure if you check the hostname in
the certificate returned by the server to which you are connecting, and verify
that it matches to hostname that you are trying to reach.

But the matching logic, defined in RFC2818, can be a bit tricky to implement on
your own. So the ssl package in the Standard Library of Python 3.2 now includes
a match_hostname() function for performing this check instead of requiring
every application to implement the check separately.

This backport brings match_hostname() to users of earlier versions of Python.
The actual code inside comes verbatim from Python 3.2.


%prep
%setup -qn %{module_name}-%{version}
%patch0 -p1
%patch1 -p1

mv src/backports/ssl_match_hostname/README.txt ./
mv src/backports/ssl_match_hostname/LICENSE.txt ./

%build
python setup.py build

%install
python setup.py install --skip-build --root %{buildroot}
rm -f %{buildroot}%{python_sitelib}/backports/__init__.py*

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc README.txt
%{python_sitelib}/backports/ssl_match_hostname/
%{python_sitelib}/backports.ssl_match_hostname-%{version}-*-nspkg.pth
%{python_sitelib}/backports.ssl_match_hostname-%{version}-*.egg-info/

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.4.0.2-5
- Rebuild for new 4.0 release.

