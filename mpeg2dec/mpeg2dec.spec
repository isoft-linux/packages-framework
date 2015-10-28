Name:           mpeg2dec
Version:        0.4.1
Release:        3%{?dist}
Summary:        MPEG-2 decoder library and program

License:        LGPL
URL:            http://libmpeg2.sourceforge.net/
Source:         http://libmpeg2.sourceforge.net/files/mpeg2dec-%{version}.tar.gz
Patch0:         mpeg2dec-0.4.1-optflags.patch
Patch1:         mpeg2dec-pic.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool

%description
mpeg2dec is a free library for decoding MPEG-2 and MPEG-1 video
streams. It is released under the terms of the GPL license.

%package        devel
Summary:        MPEG-2 decoder library development files
Requires:       %{name} = %{version}-%{release}, pkgconfig

%description    devel
mpeg2dec-devel contains the files necessary to build packages that use
the mpeg2dec library.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
aclocal
libtoolize -f -c
automake -a
autoconf
%configure \
%ifnarch %{ix86}
    --disable-accel-detect \
%endif
    --enable-shared --disable-sdl
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/extract_mpeg2
%{_bindir}/corrupt_mpeg2
%{_bindir}/mpeg2dec
%{_libdir}/libmpeg2.so.*
%{_libdir}/libmpeg2convert.so.*
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root,-)
%doc CodingStyle doc/libmpeg2.txt doc/sample*.c
%dir %{_includedir}/mpeg2dec
%{_includedir}/mpeg2dec/*.h
%{_libdir}/libmpeg2.a
%{_libdir}/libmpeg2.so
%{_libdir}/libmpeg2convert.a
%{_libdir}/libmpeg2convert.so
%{_libdir}/pkgconfig/libmpeg2.pc
%{_libdir}/pkgconfig/libmpeg2convert.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.4.1-3
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

