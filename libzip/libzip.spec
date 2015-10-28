Name:		libzip
Version:	1.0.1
Release:	2
Summary:	C library for reading, creating, and modifying zip archives

License:	Public Domain
URL:		http://www.nih.at/libzip
Source0:	http://www.nih.at/libzip/libzip-1.0.1.tar.xz

%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -rf $RPM_BUILD_ROOT%{_libdir}/libzip.a

%files
%{_bindir}/zipmerge
%{_bindir}/zipcmp
%{_libdir}/libzip.so.*
%{_mandir}/man1/zipcmp.1*
%{_mandir}/man1/zipmerge.1*

%files devel
%{_libdir}/libzip.so
%{_libdir}/pkgconfig/libzip.pc
%{_includedir}/zip.h
%dir %{_libdir}/libzip
%{_libdir}/libzip/include/zipconf.h
%{_mandir}/man3/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.1-2
- Rebuild for new 4.0 release.


