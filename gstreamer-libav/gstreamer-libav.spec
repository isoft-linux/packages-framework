%define majorminor  1.0
%define gstreamer   gstreamer
%define gst_majorminor  1.0

Name: 		%{gstreamer}-libav
Version: 	1.6.0
Release:	1	
Summary: 	GStreamer Streaming-media framework plug-in using libav (FFmpeg).
Group: 		Libraries/Multimedia
License: 	LGPL
URL:		http://gstreamer.net/
Vendor:		GStreamer Backpackers Team <package@gstreamer.net>
Source:		http://gstreamer.freedesktop.org/src/gst-ffmpeg/gst-ffmpeg/gst-libav-%{version}.tar.xz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  	%{gstreamer} >= 0.9.7
BuildRequires: 	%{gstreamer}-devel >= 0.9.7
BuildRequires: 	%{gstreamer}-plugins-base-devel >= 0.9.7
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
rm -rf $RPM_BUILD_ROOT

%makeinstall
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_majorminor}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%{_libdir}/gstreamer-%{gst_majorminor}/*.so
%{_datadir}/gtk-doc/html/*

%changelog
* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

