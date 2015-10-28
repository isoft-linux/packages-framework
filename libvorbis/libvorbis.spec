Summary:	The Vorbis General Audio Compression Codec.
Name:		libvorbis
Version:	1.3.5
Release:  	4	
Epoch:		1
License:	BSD
URL:		http://www.xiph.org/
Source:		http://downloads.xiph.org/releases/vorbis/libvorbis-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)	
BuildRequires: 	libogg-devel >= 2:1.1

%description
Ogg Vorbis is a fully open, non-proprietary, patent- and royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates from 16 to 128 kbps/channel.

The libvorbis package contains runtime libraries for use in programs
that support Ogg Vorbis.

%package devel
Summary: Development tools for Vorbis applications.
Requires:	libogg-devel >= 2:1.1
Requires:	libvorbis = %{epoch}:%{version}-%{release}
Obsoletes:	vorbis-devel

%description devel
The libvorbis-devel package contains the header files and documentation
needed to develop applications with Ogg Vorbis.

%prep
%setup -q

%build
%configure --with-ogg-libraries=%{_libdir} --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


# create a cleaned up (Makefile free) copy of doc for -devel %doc
cp -a doc _doc
rm `find _doc -name 'Makefile*'`

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README
%{_libdir}/libvorbis.so.*
%{_libdir}/libvorbisfile.so.*
%{_libdir}/libvorbisenc.so.*

%files devel
%defattr(-,root,root)
%doc _doc/*
%{_docdir}/%{name}-%{version}
%{_includedir}/vorbis
%{_libdir}/libvorbis.so
%{_libdir}/libvorbisfile.so
%{_libdir}/libvorbisenc.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/vorbis.m4

%clean 
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:1.3.5-4
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

