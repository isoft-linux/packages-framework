Summary:	Software decoder for DV format video
Name:		libdv
Version:	1.0.0
Release:	2
Epoch:		0
License:	LGPL
URL:		http://libdv.sourceforge.net/
Source:		http://dl.sf.net/libdv/libdv-%{version}.tar.gz
Patch1:		libdv-0.104-no-exec-stack.patch
Patch2:		libdv-1.0.0-pic.patch
Patch3:		libdv-1.0.0-gtk2.patch
Patch4:     libdv-1.0.0-dso-linking.patch
Patch5:     libdv-disable-sdl.patch
BuildRequires:	autoconf, automake, libtool
ExcludeArch:	s390 s390x

%package	devel
Summary:	Development package for libdv
Requires:	%{name} = %{epoch}:%{version}-%{release}

%package	tools
Summary:	Basic tools to manipulate Digital Video streams
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description
The Quasar DV codec (libdv) is a software codec for DV video, the
encoding format used by most digital camcorders, typically those that
support the IEEE 1394 (a.k.a. FireWire or i.Link) interface. libdv was
developed according to the official standards for DV video: IEC 61834
and SMPTE 314M.

%description tools
This package contains some basic programs to display and encode
digital video streams. This programs uses the Quasar DV codec (libdv),
a software codec for DV video, the encoding format used by most
digital camcorders, typically those that support the IEEE 1394
(a.k.a. FireWire or i.Link) interface.

%description devel
This package contains development files for libdv.

%prep
%setup -q
%patch1 -p0 -b .no-exec-stack
%patch2 -p1 -b .pic
%patch3 -p1 -b .gtk2
%patch4 -p1
%patch5 -p1

autoreconf -ivf

%build
%configure --with-pic
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/libdv.a
rm $RPM_BUILD_ROOT%{_libdir}/libdv.la
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING COPYRIGHT ChangeLog
%{_libdir}/libdv.so.*

%files tools
%defattr(-,root,root,-)
%doc README.*
%{_bindir}/dubdv
%{_bindir}/dvconnect
%{_bindir}/encodedv
%{_mandir}/man1/dubdv.1.gz
%{_mandir}/man1/dvconnect.1.gz
%{_mandir}/man1/encodedv.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libdv/
%{_libdir}/libdv.so
%{_libdir}/pkgconfig/libdv.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0:1.0.0-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

