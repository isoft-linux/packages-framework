Name:	    vcdimager	
Version:	0.7.24
Release:	2
Summary:    VideoCD authoring solution for mastering, extracting and analyzing Video CDs and Super Video CDs	

License:	GPLv2+
URL:        http://www.vcdimager.org	
Source0:	%name-%version.tar.gz

BuildRequires:  libcdio-devel	
Requires:	libcdio

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

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a
rm -rf $RPM_BUILD_ROOT%{_infodir}

%files
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%{_includedir}/libvcd
%{_libdir}/*.so
%{_libdir}/pkgconfig/libvcdinfo.pc
%changelog
* Sat Oct 24 2015 builder - 0.7.24-2
- Rebuild for new 4.0 release.


