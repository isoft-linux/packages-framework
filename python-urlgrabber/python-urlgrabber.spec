%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: A high-level cross-protocol url-grabber
Name: python-urlgrabber
Version: 3.10.1
Release: 8
Source0: http://urlgrabber.baseurl.org/download/urlgrabber-%{version}.tar.gz
Patch1: urlgrabber-HEAD.patch
Patch2: BZ-1051554-speed-on-404-mirror.patch

License: LGPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: python-devel, python-pycurl
Url: http://urlgrabber.baseurl.org/
Provides: urlgrabber = %{version}-%{release}
Requires: python-pycurl

%description
A high-level cross-protocol url-grabber for python supporting HTTP, FTP 
and file locations.  Features include keepalive, byte ranges, throttling,
authentication, proxies and more.

%prep
%setup -q -n urlgrabber-%{version}
%patch1 -p1
%patch2 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_docdir}/urlgrabber-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc ChangeLog README TODO
%{python_sitelib}/urlgrabber*
%{_bindir}/urlgrabber
%attr(0755,root,root) %{_libexecdir}/urlgrabber-ext-down

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.10.1-8
- Rebuild for new 4.0 release.

