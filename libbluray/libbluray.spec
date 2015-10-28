Name:           libbluray
Version:        0.9.0
Release:        2
Summary:        Library to access Blu-Ray disks for video playback 
License:        LGPLv2+
URL:            http://www.videolan.org/developers/libbluray.html
Source0:        ftp://ftp.videolan.org/pub/videolan/%{name}/%{version}/%{name}-%{version}.tar.bz2


%description
This package is aiming to provide a full portable free open source bluray
library, which can be plugged into popular media players to allow full bluray
navigation and playback on Linux. It will eventually be compatible with all
current titles, and will be easily portable and embeddable in standard players
such as mplayer and vlc.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static \
           --disable-doxygen-pdf \
           --disable-doxygen-ps \
           --disable-doxygen-html \
           --disable-bdjava 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libbluray.pc


%changelog
* Sat Oct 24 2015 builder - 0.9.0-2
- Rebuild for new 4.0 release.

* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- update to 1.9.0
