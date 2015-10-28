Summary: The Ogg bitstream file format library.
Name:		libogg
Version:	1.3.2
Release:	2.2 
Epoch:		2
License:      BSD
URL:		http://www.xiph.org/
Source:		http://www.xiph.org/pub/ogg/vorbis/download/libogg-%{version}.tar.xz
Patch:		libogg-1.0-m4.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Libogg is a library for manipulating Ogg bitstream file formats.
Libogg supports both making Ogg bitstreams and getting packets from
Ogg bitstreams.

%package devel
Summary: Files needed for development using libogg.
Requires: libogg = %{epoch}:%{version}

%description devel
Libogg is a library used for manipulating Ogg bitstreams. The
libogg-devel package contains the header files and documentation
needed for development using libogg.

%prep
%setup -q -n %{name}-%{version}
%patch -p1 

%build
perl -p -i -e "s/-O20/$RPM_OPT_FLAGS/" configure
perl -p -i -e "s/-ffast-math//" configure
%configure
make %{?_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/usr/share/doc
%files
%defattr(-,root,root)
#%doc AUTHORS CHANGES COPYING README
%{_libdir}/libogg.so.*

%files devel
%defattr(-,root,root)
#%doc doc/*.html
#%doc doc/*.txt
#%doc doc/*.png
#%doc doc/libogg
%dir %{_includedir}/ogg
%{_includedir}/ogg/ogg.h
%{_includedir}/ogg/os_types.h
%{_includedir}/ogg/config_types.h
%{_libdir}/libogg.a
%{_libdir}/libogg.so
%{_libdir}/pkgconfig/ogg.pc
%{_datadir}/aclocal/ogg.m4

%clean 
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2:1.3.2-2.2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

