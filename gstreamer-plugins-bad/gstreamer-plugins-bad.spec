%define majorminor   1.0
%define gstreamer    gstreamer

%define gst_minver   1.0 
%define gstpb_minver 1.0

Summary: GStreamer streaming media framework "bad" plug-ins
Name: %{gstreamer}-plugins-bad
Version: 1.6.1
Release: 2 
# The freeze and nfs plugins are LGPLv2 (only)
License: LGPLv2+ and LGPLv2
URL: http://gstreamer.freedesktop.org/
Source: http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz

Patch100: gst-plugins-bad-dirty-fix-faad-mp4-crash.patch 

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: %{gstreamer} >= %{gst_minver}
BuildRequires: %{gstreamer}-devel >= %{gst_minver}
BuildRequires: %{gstreamer}-plugins-base-devel >= %{gstpb_minver}

BuildRequires:  check
BuildRequires:  gettext-devel
BuildRequires:  libXt-devel
BuildRequires:  gtk-doc
BuildRequires:  gobject-introspection-devel

BuildRequires:  bzip2-devel
BuildRequires:  gsm-devel
BuildRequires:  jasper-devel
BuildRequires:  libdvdnav-devel
BuildRequires:  libexif-devel
BuildRequires:  libmpcdec-devel
BuildRequires:  liboil-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libsndfile-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  openssl-devel
BuildRequires:  orc-devel
BuildRequires:  wavpack-devel
BuildRequires:  opus-devel
BuildRequires:  nettle-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  gnutls-devel
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  gtk3-devel >= 3.4
BuildRequires:  bluez-libs-devel >= 5.0
BuildRequires:  libwebp-devel

BuildRequires:  chrpath

BuildRequires:  libass-devel
BuildRequires:  libcurl-devel
BuildRequires:  libvdpau-devel
BuildRequires:  openal-devel
BuildRequires:  openjpeg-devel
BuildRequires:  OpenEXR-devel

%description
gstreamer-plugins-bad contains plug-ins that aren't
tested well enough, or the code is not of good enough quality.

%package devel
Summary: Development files for the GStreamer media framework "bad" plug-ins
Requires: %{name} = %{version}-%{release}
Requires: %{gstreamer}-plugins-base-devel

%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that
aren't tested well enough, or the code is not of good enough quality.


%prep
%setup -q -n gst-plugins-bad-%{version}

%build
%configure \
    --enable-debug \
    --disable-static \
    --disable-gtk-doc \
    --enable-experimental \
    --disable-fatal-warnings \
    --disable-opencv \
    --without-x \
    --disable-sdl 
 
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR="%{buildroot}"

%find_lang gst-plugins-bad-%{majorminor}

#backward compability, some cmake requires.
pushd %{buildroot}/%{_includedir}/gstreamer-1.0/gst/gl
ln -sf %{_libdir}/gstreamer-1.0/include/gst/gl/gstglconfig.h .
popd

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gst-plugins-bad-%{majorminor}.lang
%defattr(-,root,root,-)
%{_libdir}/libgst*.so.*
%{_libdir}/gstreamer-%{majorminor}/*.so
%{_libdir}/girepository-?.?/*.typelib
%{_datadir}/gstreamer-?.?/presets/GstFreeverb.prs

%files devel
%defattr(-,root,root,-)
%{_libdir}/libgst*.so
%{_includedir}/gstreamer-*
%{_libdir}/gstreamer-?.?/include/gst/gl/gstglconfig.h
%{_libdir}/pkgconfig/*.pc
%doc %{_datadir}/gtk-doc/*
%{_datadir}/gir-?.?/*.gir

%changelog
* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 1.6.1-2
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.6.0-2
- Rebuild for new 4.0 release.

* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

