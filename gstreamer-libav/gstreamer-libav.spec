%define majorminor 1.0
%define gstreamer gstreamer
%define gst_majorminor 1.0

Name: %{gstreamer}-libav
Version: 1.6.1
Release: 2
Summary: GStreamer Streaming-media framework plug-in using libav (FFmpeg).
License: LGPL
URL: http://gstreamer.net/
Source0: http://gstreamer.freedesktop.org/src/gst-ffmpeg/gst-ffmpeg/gst-libav-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: %{gstreamer} >= 0.9.7
BuildRequires: %{gstreamer}-devel >= 0.9.7
BuildRequires: %{gstreamer}-plugins-base-devel >= 0.9.7
BuildRequires: bzip2-devel xz-devel zlib-devel
BuildRequires: orc-devel

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related. Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This plugin contains the libav (formerly FFmpeg) codecs, containing codecs for most popular
multimedia formats.

%prep
%setup -q -n gst-libav-%{version}

%build
export CFLAGS="$CFLAGS -fno-strict-aliasing"
%configure \
    --disable-fatal-warnings \
    --enable-orc

make %{?_smp_mflags}

%install
%makeinstall

rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_majorminor}/*.a

%files
%defattr(-, root, root, -)
%{_libdir}/gstreamer-%{gst_majorminor}/*.so
%{_datadir}/gtk-doc/html/*

%changelog
* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 1.6.1-2
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.6.0-2
- Rebuild for new 4.0 release.

* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

