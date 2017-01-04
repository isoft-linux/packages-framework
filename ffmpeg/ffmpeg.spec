#build with sdl or not, sdl only used by ffplay.
#ffplay had some issues with xorg intel driver.
#Patch0 used to fix ffplay crash Xorg issue.
#But not fix ffplay resize segfault issue.
#So, add this option to enable or disable build with SDL.
%define withsdl 1 

Summary: Hyper fast MPEG1/MPEG4/H263/RV and AC3/MPEG audio encoder
Name: ffmpeg
Version: 3.2.2
Release: 1
License: GPLv3
Source: http://ffmpeg.org/releases/%{name}-%{version}.tar.xz
#Patch0: ffmpeg-fix-ffplay-crash-Xorg-with-intel-driver.patch
 
URL: http://ffmpeg.sourceforge.net/
BuildRequires: freetype-devel, zlib-devel, bzip2-devel xz-devel
BuildRequires: libtheora-devel, libvorbis-devel
BuildRequires: xvidcore-devel
BuildRequires: yasm >= 1.2.0
BuildRequires: x264-devel 
BuildRequires: x265-devel 
BuildRequires: libcdio-devel
BuildRequires: libcdio-paranoia-devel
BuildRequires: libvpx-devel
BuildRequires: libxcb-devel
BuildRequires: libva-devel libvdpau-devel
BuildRequires: libspeex-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: faac-devel
BuildRequires: alsa-lib-devel
BuildRequires: libX11-devel libXv-devel libXext-devel
BuildRequires: openjpeg-devel
BuildRequires: libbluray-devel
BuildRequires: libmfx-devel
BuildRequires: lame-devel

BuildRequires: libdc1394-devel libraw1394-devel
BuildRequires: wavpack-devel
BuildRequires: openal-devel
BuildRequires: libv4l-devel
BuildRequires: fontconfig-devel freetype-devel fribidi-devel
BuildRequires: libass-devel

#for ffplay
%if %{withsdl}
BuildRequires: SDL-devel
%endif

BuildRequires: doxygen

Requires: %{name}-libs = %{version}-%{release}

%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

%package libs 
Summary: Runtime libraries for ffmpeg
%description libs
Runtime libraries for ffmpeg

#%package shared-devel
#Summary: Shared development libraries for ffmpeg
#Requires: %{name}-libs = %{version}-%{release}
#Requires: %{name}-devel = %{version}-%{release}
#
#%description shared-devel
#Shared development libraries for ffmpeg
#
#%package static-devel
#Summary: Static development libraries for ffmpeg
#Requires: %{name}-devel = %{version}-%{release}
#
#%description static-devel
#Static development libraries for ffmpeg

%package devel
Summary: Development headers, libraries and pkgconfig files for ffmpeg
Requires: %{name}-libs = %{version}-%{release}

%description devel
Development headers, libraries and pkgconfig files for ffmpeg.

%prep
%setup -q
#%patch0 -p1

%build
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --shlibdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-shared \
    --enable-runtime-cpudetect \
    --enable-libbluray \
    --enable-libcdio \
%if %{withsdl}
    --enable-sdl \
%else
    --disable-sdl \
%endif
    --enable-libdc1394 \
    --enable-libpulse \
    --enable-libspeex \
    --enable-libvpx \
    --enable-libwavpack \
    --enable-openal \
    --enable-gpl \
    --enable-version3 \
    --enable-nonfree \
    --enable-postproc \
    --enable-avfilter \
    --enable-pthreads \
    --enable-x11grab \
    --enable-libopenjpeg \
    --enable-libfaac \
    --enable-libtheora \
    --enable-libvorbis \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libxvid \
    --enable-vaapi \
    --enable-vdpau \
    --enable-libmfx \
    --enable-libv4l2 \
    --enable-fontconfig \
    --enable-libass \
    --enable-libfribidi \
    --enable-libfreetype \
    --enable-libmp3lame \
    --disable-static \
    --disable-libcelt \
    --disable-libiec61883 \
    --disable-libmodplug \
    --disable-libopencv \
    --disable-avisynth \
    --disable-stripping \
    --enable-doc \
    --extra-cflags="-fPIC" 
    

#--disable-symver

make %{?_smp_mflags}

#generate doxygen docs
pushd doc
mkdir -p doc/doxy
doxygen
popd


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

#install docs
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/ffmpeg-devel
cp -r doc/doc/doxy/* $RPM_BUILD_ROOT/%{_docdir}/ffmpeg-devel

#ensure to remove static libraries.
#since we do not ship dependent multimedia static libraries, the ffmpeg static libraries is useless.
rm -rf  

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/ffmpeg
%{_bindir}/ffprobe
%{_bindir}/ffserver
%if %{withsdl}
%{_bindir}/ffplay
%endif
%dir %{_datadir}/ffmpeg
%{_datadir}/ffmpeg/*.ffpreset
%{_datadir}/ffmpeg/ffprobe.xsd
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*

#%files shared-devel
#%defattr(-,root,root,-)

#%files static-devel
#%defattr(-,root,root,-)
#%{_libdir}/*.a

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%dir %{_docdir}/ffmpeg-devel
%{_docdir}/ffmpeg-devel/*
%{_datadir}/ffmpeg/examples/*
%{_docdir}/ffmpeg-devel
%{_mandir}/man3/*


%changelog
* Wed Jan 04 2017 sulit - 3.2.2-1
- upgrade ffmpeg to 3.2.2

* Mon May 09 2016 sulit <sulitsrc@gmail.com> - 2.8.7-2
- update to official release 2.8.7

* Thu Dec 17 2015 Cjacker <cjacker@foxmail.com> - 2.8.3-2
- Update

* Wed Dec 02 2015 Cjacker <cjacker@foxmail.com> - 2.8.1-9
- Enable lame

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 2.8.1-8
- Disable build with SDL, add an option to control it

* Wed Nov 11 2015 Cjacker <cjacker@foxmail.com> - 2.8.1-7
- need setup VideoMode. but crash when resize video window

* Wed Nov 11 2015 Cjacker <cjacker@foxmail.com> - 2.8.1-6
- try to fix ffplay fullscreen crash

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 2.8.1-5
- Fix ffplay crash Xorg when using intel driver

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.8.1-4
- Rebuild for new 4.0 release.

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 2.8.1-3
- add SDL-devel requires, enable ffplay

* Mon Oct 19 2015 Cjacker <cjacker@foxmail.com> - 2.8.1-2
- update
