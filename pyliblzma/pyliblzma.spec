Summary:    Python bindings for lzma
Name:       pyliblzma
Version:    0.5.3
Release:    14
License:    LGPLv3+
URL:        https://launchpad.net/pyliblzma
Source0:    http://pypi.python.org/packages/source/p/pyliblzma/%{name}-%{version}.tar.bz2
Patch0:     no-script-liblzma.patch

BuildRequires:    xz-devel python-setuptools python2-devel libffi-devel
#BuildRequires:    python-test
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PylibLZMA provides a python interface for the liblzma library
to read and write data that has been compressed or can be decompressed
by Lasse Collin's lzma utils.

%prep
%setup -qn %{name}-%{version}

%patch0 -p1 

%build
%{__python} setup.py build

%check
#%{__python} setup.py test

%install
rm -rf %{buildroot}
%{__python} setup.py install --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README THANKS ChangeLog NEWS
%attr(0755,-,-) %{python_sitearch}/lzma.so
%{python_sitearch}/liblzma.py*
%{python_sitearch}/%{name}*.egg-info

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.5.3-14
- Rebuild for new 4.0 release.

