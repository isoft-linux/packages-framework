Name: jasper
Version: 1.900.1
Release: 2
Summary: JasPer
License: Modified BSD
Source: http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-1.900.1.zip
Patch0: jpc_dec.c.patch
Patch1: libjasper-stepsizes-overflow.patch
Patch2: jasper-1.900.1-CVE-2008-3520.patch
Patch3: jasper-1.900.1-CVE-2008-3522.patch
Patch4: jasper-1.900.1-bnc725758.patch

Requires: libjpeg
BuildRequires: libjpeg-devel
URL: http://www.ece.uvic.ca/~mdadams/jasper/

%description 
JasPer is a collection        
of software (i.e., a library and application programs) for the coding 
and manipulation of images.  This software can handle image data in a 
variety of formats.  One such format supported by JasPer is the JPEG-2000 
format defined in ISO/IEC 15444-1:2000.

%package devel
Summary: Include Files and Documentation
Requires: %{name} = %{version}

%description devel
JasPer is a collection        
of software (i.e., a library and application programs) for the coding 
and manipulation of images.  This software can handle image data in a 
variety of formats.  One such format supported by JasPer is the JPEG-2000 
code stream format defined in ISO/IEC 15444-1:2000.

%prep
%setup
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure --enable-shared --without-x --disable-opengl
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README LICENSE ChangeLog
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libdir}/lib*.so
%{_mandir}/man1/*.gz

%files devel
%defattr(-, root, root)
%dir %{_includedir}/jasper
%{_includedir}/jasper/*
%{_libdir}/lib*.a

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.900.1-2
- Rebuild for new 4.0 release.

* Thu Apr 5 2007 Xuqing Kuang <xqkuang@redflag-linux.com> - 1.900.1-1
- initial version
