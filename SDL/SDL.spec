Summary: A cross-platform multimedia library
Name: SDL
Version: 1.2.15
Release: 10
Source0: %{name}-%{version}.tar.gz
Patch0: SDL-1.2.10-GrabNotViewable.patch  
Patch1: SDL-1.2.15-const_XData32.patch

# Proposed to upstream as sdl1680, rh891973
Patch2:     SDL-1.2.15-x11-Bypass-SetGammaRamp-when-changing-gamma.patch
# Upstream fix for sdl1486, rh990677
Patch5:     SDL-1.2.15-ignore_insane_joystick_axis.patch
# Do not use backing store by default, sdl2383, rh1073057, rejected by
# upstream
Patch6:     SDL-1.2.15-no-default-backing-store.patch
# Fix processing keyboard events if SDL_EnableUNICODE() is enabled, sdl2325,
# rh1126136, in upstream after 1.2.15
Patch7:     SDL-1.2.15-SDL_EnableUNICODE_drops_keyboard_events.patch
Patch8: SDL-remove-esd.patch

URL: http://www.libsdl.org/
License: LGPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: alsa-lib-devel
BuildRequires:  coreutils
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  libXext-devel
BuildRequires:  libX11-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  make
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

%ifarch %{ix86}
BuildRequires: nasm
%endif

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.

%package devel
Summary: Files needed to develop Simple DirectMedia Layer applications
Requires: SDL = %{version}-%{release} alsa-lib-devel
Requires:   alsa-lib-devel
Requires:   mesa-libGL-devel
Requires:   mesa-libGLU-devel
Requires:   libX11-devel
Requires:   libXext-devel
Requires:   libXrandr-devel
Requires:   libXrender-devel

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device. This package provides the libraries, include files, and other
resources needed for developing SDL applications.

%package static
Summary: Files needed to develop static Simple DirectMedia Layer applications
Requires: SDL-devel = %{version}-%{release}

%description static
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device. This package provides the static libraries needed for developing
static SDL applications.

%prep
%setup -q -b0
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
aclocal
libtoolize
autoconf
%configure \
   --disable-video-svga \
   --disable-video-ggi \
   --disable-video-aalib \
   --enable-sdl-dlopen \
   --enable-arts-shared \
   --enable-esd-shared \
   --enable-pulseaudio-shared \
   --enable-alsa \
   --disable-video-ps3 \
   --disable-rpath

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# remove libtool .la file
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl.pc
%{_includedir}/SDL
%{_datadir}/aclocal/*
%{_mandir}/man3/SDL*.3*

%files static
%defattr(-,root,root)
%{_libdir}/lib*.a


%changelog
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 1.2.15-10
- Rebuild

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.2.15-9
- Rebuild for new 4.0 release.

