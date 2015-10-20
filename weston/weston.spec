%global with_x11 1 

%define         gitdate 

Name:           weston
Version:        1.9.0
Release:        4%{?gitdate:.git%{gitdate}} 
Summary:        Reference compositor for Wayland
License:        BSD and CC-BY-SA
URL:            http://wayland.freedesktop.org/
Source0:        http://wayland.freedesktop.org/releases/%{name}-%{?gitdate:}%{!?gitdate:%{version}}.tar.xz
#git clone git://anongit.freedesktop.org/wayland/weston
#Source0: weston.tar.gz

Requires:       xkeyboard-config 
BuildRequires:  autoconf
BuildRequires:  cairo-devel >= 1.10.0
BuildRequires:  glib2-devel
BuildRequires:  libdrm-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libtool
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-server-devel
BuildRequires:  libwayland-cursor-devel
BuildRequires:  libxkbcommon-devel >= 0.1.0-8
BuildRequires:  mesa-libgbm-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libwayland-egl-devel
BuildRequires:  mtdev-devel
BuildRequires:  pam-devel
BuildRequires:  pixman-devel
BuildRequires:  libinput-devel >= 0.6.0
#BuildRequires:  colord-devel
%if %with_x11
BuildRequires:  pkgconfig(cairo-xcb)
%endif

%description
Weston is the reference wayland compositor that can run on KMS, under X11
or under another compositor.

%if %with_x11
%package x11 
Summary: weston x11 backend and XWayland support
Requires: %name = %{version}

%description x11 
%{summary}
%endif

%package devel
Summary: Libraries and headers for %{name}
Requires: %name = %{version}

%description devel
Libraries and headers for %{name}

%package demo 
Summary: Demo applications for %{name}
Requires: %name = %{version}

%description demo 
Demo applications for %{name}


%prep
%setup -q -n %{name}-%{?gitdate:}%{!?gitdate:%{version}}

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure \
    --disable-static \
    --disable-setuid-install \
    --disable-vaapi-recorder \
    --disable-colord \
    --enable-libinput-backend \
    --enable-demo-clients-install \
    %if %with_x11
    --enable-xwayland \
    --enable-x11-compositor \
    %else
    --disable-xwayland \
    --disable-x11-compositor \
    %endif

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING
%{_bindir}/weston
%{_bindir}/weston-info
%{_bindir}/weston-launch
%{_bindir}/weston-terminal
#need build weston with pango
%{_bindir}/weston-editor

%{_bindir}/wcap-decode
%dir %{_libdir}/weston
%{_libdir}/weston/desktop-shell.so
%{_libdir}/weston/drm-backend.so
%{_libdir}/weston/wayland-backend.so
%{_libdir}/weston/gl-renderer.so
#%{_libdir}/weston/cms-static.so
%{_libdir}/weston/fullscreen-shell.so
%{_libdir}/weston/fbdev-backend.so
%{_libdir}/weston/headless-backend.so
#%{_libdir}/weston/cms-colord.so
%{_libdir}/weston/cms-static.so
%{_libexecdir}/weston-*
%{_mandir}/man1/*.1*
%{_mandir}/man5/weston.ini.5.gz
%{_mandir}/man7/weston-drm.7.gz
%dir %{_datadir}/weston
%{_datadir}/weston/*.png
%{_datadir}/weston/wayland.svg
%{_libdir}/weston/hmi-controller.so
%{_libdir}/weston/ivi-shell.so
%{_datadir}/wayland-sessions/weston.desktop


%if %with_x11
%files x11
%{_libdir}/weston/x11-backend.so
%{_libdir}/weston/xwayland.so
%endif

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/weston
%{_includedir}/weston/*
%{_libdir}/pkgconfig/weston.pc

#weston-editor requires pango
#we do NOT want to introduce this dependency at CoreGUI level
#so, drop it.
%files demo
%{_bindir}/weston-calibrator
%{_bindir}/weston-clickdot
%{_bindir}/weston-cliptest
%{_bindir}/weston-dnd
#%{_bindir}/weston-editor
%{_bindir}/weston-eventdemo
%{_bindir}/weston-flower
%{_bindir}/weston-fullscreen
%{_bindir}/weston-image
%{_bindir}/weston-multi-resource
%{_bindir}/weston-resizor
%{_bindir}/weston-scaler
%{_bindir}/weston-simple-damage
%{_bindir}/weston-simple-egl
%{_bindir}/weston-simple-shm
%{_bindir}/weston-simple-touch
%{_bindir}/weston-smoke
%{_bindir}/weston-stacking
%{_bindir}/weston-subsurfaces
%{_bindir}/weston-transformed
%{_bindir}/weston-presentation-shm
%{_bindir}/weston-simple-dmabuf

%changelog
* Thu Sep 03 2015 Cjacker <cjacker@foxmail.com>
- update to 1.8.92

