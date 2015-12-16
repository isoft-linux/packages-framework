Name:           python3-xlib
Version:        0.15
Release:        2%{?dist}
Summary:        Python 3 port of Xlib

License:        GPLv2+
URL:            https://github.com/LiuLang/python3-xlib
# Source from git hub https://github.com/LiuLang/python3-xlib/archive/master.zip
Source0:        https://pypi.python.org/packages/source/p/python3-xlib/python3-xlib-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:	python3-devel
BuildRequires:	python3-setuptools


%description

python3-xlib is python3 version of python-xlib, The Python X Library is a 
complete X11R6 client-side implementation, written in pure Python. It can 
be used to write low-levelish X Windows client applications in Python.


%prep
%setup -q

%build
python3 setup.py build


%install
python3 setup.py install --root=%{buildroot} 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{python3_sitelib}/Xlib/
%{python3_sitelib}/*.egg-info


%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 0.15-2
- Initial build

