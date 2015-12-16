# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pre_release rc1 
Name:           python-xlib
Version:        0.15
Release:        0.12.%{pre_release}%{?dist}
Summary:        X client library for Python

License:        GPLv2+
URL:            http://python-xlib.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/python-xlib/python-xlib-%{version}%{pre_release}.tar.gz
Source1:        defs 
Patch0:         increase-receiving-buffer
Patch1:         fix-unix-socket-in-display
Patch2:         fix-ssh-tunnel-auth 
Patch3:         fix-rhomboid-examples 
Patch4:         python-xlib-0.15rc1-xauthority.patch
Patch5:         r138-mggr-get-rid-of-annoying-Xlib.protocol.request.Query.patch
Patch6:         r139-allow-IPv6-addresses-e.g.-d-Xlib.display.Display-fff.patch
# Fix perl usage
# https://sourceforge.net/p/python-xlib/bugs/41/
Patch7:         python-xlib-perl.patch
BuildArch:      noarch
BuildRequires:  python-devel

%package doc
Summary:        Documentation and examples for python-xlib
Requires:       %{name} = %{version}-%{release}


%description
The Python X Library is a complete X11R6 client-side implementation, 
written in pure Python. It can be used to write low-levelish X Windows 
client applications in Python.

%description doc
Install this package if you want the developers' documentation and examples
that tell you how to program with python-xlib.

%prep
%setup -q -n %{name}-%{version}%{pre_release}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p2
%patch6 -p2
%patch7 -p1 -b .perl

%build
%{__python} setup.py build
cp %{SOURCE1} doc/src/ 
cd doc
make html
cd html
rm Makefile texi2html

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
chmod a-x examples/*.py
 
%files
%doc README COPYING
# For noarch packages: sitelib
%{python_sitelib}/*

%files doc
%doc COPYING examples doc/html


%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 0.15-0.12.rc1
- Initial build

