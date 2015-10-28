Name:		libchardet
Version:	1.0.4
Release:	2
Summary:	Mozilla's Universal Charset Detector C/C++ API

License:    MPL	
URL:		http://ftp.oops.org/pub/oops/libchardet/
Source0:	http://ftp.oops.org/pub/oops/libchardet/libchardet-%{version}.tar.bz2

%description
Mozilla's Universal Charset Detector C/C++ API


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

rm -rf $RPM_BUILD_ROOT%{_mandir}/ko

%files
%{_libdir}/*.so.*

%files devel
%{_bindir}/chardet-config
%{_libdir}/libchardet.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/chardet.pc
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.4-2
- Rebuild for new 4.0 release.

* Sun Jul 19 2015 Cjacker <cjacker@foxmail.com>
- first build
