Summary: The GNU line editor.
Name: ed
Version: 1.9 
Release: 2
License: GPL
Source: ftp://ftp.gnu.org/gnu/ed/%{name}-%{version}.tar.gz
URL: 	http://www.gnu.org/software/ed/

%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

Ed was the original UNIX editor, and may be used by some programs.  In
general, however, you probably don't need to install it and you probably
won't use it.

%prep
%setup -q

%build
chmod 755 configure
./configure --prefix=/usr
make %{?_smp_mflags}

%install
%makeinstall mandir=$RPM_BUILD_ROOT%{_mandir}/man1
rm -rf $RPM_BUILD_ROOT%{_infodir}
%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README TODO
%{_bindir}/*
%{_mandir}/*/*


%changelog
* Sat Oct 24 2015 builder - 1.9-2
- Rebuild for new 4.0 release.

* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
