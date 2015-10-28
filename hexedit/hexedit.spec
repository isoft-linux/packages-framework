Summary: A hexadecimal file viewer and editor.
Name: hexedit
Version: 1.2.12
Release: 4.2
License: GPL
Url: http://merd.net/pixel
Source: http://merd.net/pixel/%{name}-%{version}.src.tgz
Patch: hexedit-1.2.2-config.patch
BuildRequires: ncurses-devel

%description
Hexedit shows a file both in ASCII and in hexadecimal. The file can be a device as
the file is read a piece at a time. Hexedit can be used to modify the file
and search through it.

%prep
%setup -q -n %{name}
%patch -p1 -b .config

%build
export CFLAGS="$RPM_OPT_FLAGS"
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall mandir=$RPM_BUILD_ROOT%{_mandir}

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/hexedit
%{_mandir}/*/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.2.12-4.2
- Rebuild for new 4.0 release.

