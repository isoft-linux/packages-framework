Name:           python-backports
Version:        1.0
Release:        7%{?dist}
Summary:        Namespace for backported Python features

# Only code is sourced from http://www.python.org/dev/peps/pep-0382/
License:        Public Domain
URL:            https://pypi.python.org/pypi/backports
Source0:        backports.py

BuildRequires:  python2-devel

%description
The backports namespace is a namespace reserved for features backported from
the Python standard library to older versions of Python 2.

Packages that exist in the backports namespace in Fedora should not provide
their own backports/__init__.py, but instead require this package.

Backports to earlier versions of Python 3, if they exist, do not need this
package because of changes made in Python 3.3 in PEP 420
(http://www.python.org/dev/peps/pep-0420/).


%prep


%build


%install
mkdir -pm 755 %{buildroot}%{python_sitelib}/backports
install -pm 644 %{SOURCE0} %{buildroot}%{python_sitelib}/backports/__init__.py
%if "%{python_sitelib}" != "%{python_sitearch}"
mkdir -pm 755 %{buildroot}%{python_sitearch}/backports
install -pm 644 %{SOURCE0} %{buildroot}%{python_sitearch}/backports/__init__.py
%endif

 
%files
%{python_sitelib}/backports
%if "%{python_sitelib}" != "%{python_sitearch}"
%{python_sitearch}/backports
%endif


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0-7
- Rebuild for new 4.0 release.

