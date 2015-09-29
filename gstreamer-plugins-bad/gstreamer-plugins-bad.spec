%define majorminor   1.0
%define gstreamer    gstreamer

%define gst_minver   1.0 
%define gstpb_minver 1.0

Summary: GStreamer streaming media framework "bad" plug-ins
Name: %{gstreamer}-plugins-bad
Version: 1.6.0
Release: 1
# The freeze and nfs plugins are LGPLv2 (only)
License: LGPLv2+ and LGPLv2
Group: Applications/Multimedia
URL: http://gstreamer.freedesktop.org/
Source: http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz

Patch100: gst-plugins-bad-dirty-fix-faad-mp4-crash.patch 

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: %{gstreamer} >= %{gst_minver}
BuildRequires: %{gstreamer}-devel >= %{gst_minver}
BuildRequires: %{gstreamer}-plugins-base-devel >= %{gstpb_minver}

BuildRequires: gettext-devel
BuildRequires: gtk-doc

BuildRequires: bzip2-devel
BuildRequires: jasper-devel
BuildRequires: librsvg2-devel
BuildRequires: openssl-devel
BuildRequires: orc-devel

BuildRequires: mp4v2-devel
BuildRequires: faac-devel
BuildRequires: faad2-devel
BuildRequires: libsndfile-devel
BuildRequires: fribidi-devel
BuildRequires: enca-devel
BuildRequires: libass-devel
BuildRequires: libdvdread-devel
BuildRequires: libdvdnav-devel
BuildRequires: libdc1394-devel

%description
gstreamer-plugins-bad contains plug-ins that aren't
tested well enough, or the code is not of good enough quality.

%package devel
Summary: Development files for the GStreamer media framework "bad" plug-ins
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{gstreamer}-plugins-base-devel

%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that
aren't tested well enough, or the code is not of good enough quality.


%prep
%setup -q -n gst-plugins-bad-%{version}
#%patch100 -p1

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
* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

