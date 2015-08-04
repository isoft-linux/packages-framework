Name:	  	prozilla	
Version:    2.0.4	
Release:	1
Summary:	A download accelerator for Linux.
Group:		System Environment/Shells
License:	GPL
Source:		prozilla-2.0.4.tar.bz2
Patch:		prozilla-2.0.4-compile-fix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root


%description
ProZilla is a download accelerator for Linux which gives you a 200% to 300%
improvement in your file downloading speeds.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep

%setup
%patch -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la

%find_lang proz

%clean
rm -rf $RPM_BUILD_ROOT

%files -f proz.lang
%{_bindir}/proz
%{_mandir}/man1/proz.1.gz

%files devel
%{_includedir}/*.h
%{_libdir}/libprozilla.a

%changelog
* Wed Jul 15 2015 Cjacker <cjacker@foxmail.com>
- add devel package.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

