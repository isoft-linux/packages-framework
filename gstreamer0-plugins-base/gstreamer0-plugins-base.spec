%define         gstreamer       gstreamer0
%define         majorminor      0.10
%define         gstreamer_version %{majorminor}.36

Name:           %{gstreamer}-plugins-base
Version:        %{gstreamer_version}
Release:        14%{?dist}
Summary:        GStreamer streaming media framework base plug-ins

License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
#Source:         http://gstreamer.freedesktop.org/src/gst-plugins-base/pre/gst-plugins-base-%{version}.tar.bz2
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-%{version}.tar.xz
# https://bugzilla.gnome.org/show_bug.cgi?id=652342 - fixes RB CD rip

Requires:       %{gstreamer} >= %{gstreamer_version}
Requires:       iso-codes
BuildRequires:  %{gstreamer}-devel >= %{gstreamer_version}
BuildRequires:  iso-codes-devel
BuildRequires:  gobject-introspection-devel >= 0.6.3

BuildRequires:  gettext
BuildRequires:  gcc

BuildRequires:  alsa-lib-devel
BuildRequires:  libcdio-paranoia-devel 
BuildRequires:  gtk2-devel
BuildRequires:  libgudev-devel
BuildRequires:  libogg-devel >= 1.0
BuildRequires:  liboil-devel >= 0.3.6
BuildRequires:  libtheora-devel >= 1.0
BuildRequires:  libvisual-devel
BuildRequires:  libvorbis-devel >= 1.0
BuildRequires:  libXv-devel
BuildRequires:  orc-devel >= 0.4.11
BuildRequires:  pango-devel
BuildRequires:  pkgconfig

BuildRequires:  chrpath

# documentation
BuildRequires:  gtk-doc >= 1.3

Patch0: 0001-missing-plugins-Remove-the-mpegaudioversion-field.patch
Patch1: 0001-audioresample-Fix-build-on-x86-if-emmintrin.h-is-ava.patch
Patch2: 0002-audioresample-It-s-HAVE_EMMINTRIN_H-not-HAVE_XMMINTR.patch

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains a set of well-maintained base plug-ins.

%prep
%setup -q -n gst-plugins-base-%{version}
%patch0 -p1 -b .mpegaudioversion
%patch1 -p1 -b .0001
%patch2 -p1 -b .0002

%build
%configure \
  --enable-experimental \
  --disable-gtk-doc \
  --enable-orc \
  --disable-gnome_vfs \
  --disable-static

make %{?_smp_mflags} ERROR_CFLAGS=""

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstadder.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstalsa.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudioconvert.so
#chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstcdparanoia.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstdecodebin.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstdecodebin2.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstencodebin.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstffmpegcolorspace.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstogg.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstpango.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstplaybin.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgsttheora.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgsttypefindfunctions.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideoscale.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvolume.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvorbis.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstaudio-0.10.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstcdda-0.10.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstriff-0.10.so.*

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_bindir}/gst-visualise*
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/gst-visualise*

%find_lang gst-plugins-base-%{majorminor}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f gst-plugins-base-%{majorminor}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING README REQUIREMENTS

# libraries
%{_libdir}/libgstinterfaces-%{majorminor}.so.*
%{_libdir}/libgstaudio-%{majorminor}.so.*
%{_libdir}/libgstcdda-%{majorminor}.so.*
%{_libdir}/libgstfft-%{majorminor}.so.*
%{_libdir}/libgstriff-%{majorminor}.so.*
%{_libdir}/libgsttag-%{majorminor}.so.*
%{_libdir}/libgstnetbuffer-%{majorminor}.so.*
%{_libdir}/libgstrtp-%{majorminor}.so.*
%{_libdir}/libgstvideo-%{majorminor}.so.*
%{_libdir}/libgstpbutils-%{majorminor}.so.*
%{_libdir}/libgstrtsp-%{majorminor}.so.*
%{_libdir}/libgstsdp-%{majorminor}.so.*
%{_libdir}/libgstapp-%{majorminor}.so.*

# gobject-introspection files
%{_libdir}/girepository-1.0/GstApp-0.10.typelib
%{_libdir}/girepository-1.0/GstAudio-0.10.typelib
%{_libdir}/girepository-1.0/GstFft-0.10.typelib
%{_libdir}/girepository-1.0/GstInterfaces-0.10.typelib
%{_libdir}/girepository-1.0/GstNetbuffer-0.10.typelib
%{_libdir}/girepository-1.0/GstPbutils-0.10.typelib
%{_libdir}/girepository-1.0/GstRiff-0.10.typelib
%{_libdir}/girepository-1.0/GstRtp-0.10.typelib
%{_libdir}/girepository-1.0/GstRtsp-0.10.typelib
%{_libdir}/girepository-1.0/GstSdp-0.10.typelib
%{_libdir}/girepository-1.0/GstTag-0.10.typelib
%{_libdir}/girepository-1.0/GstVideo-0.10.typelib

# base plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstadder.so
%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiorate.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioresample.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiotestsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstdecodebin.so
%{_libdir}/gstreamer-%{majorminor}/libgstdecodebin2.so
%{_libdir}/gstreamer-%{majorminor}/libgstencodebin.so
%{_libdir}/gstreamer-%{majorminor}/libgstffmpegcolorspace.so
%{_libdir}/gstreamer-%{majorminor}/libgstgdp.so
%{_libdir}/gstreamer-%{majorminor}/libgstgio.so
%{_libdir}/gstreamer-%{majorminor}/libgstplaybin.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubparse.so
%{_libdir}/gstreamer-%{majorminor}/libgsttcp.so
%{_libdir}/gstreamer-%{majorminor}/libgsttypefindfunctions.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideorate.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoscale.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideotestsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstvolume.so

# base plugins with dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstalsa.so
#%{_libdir}/gstreamer-%{majorminor}/libgstcdparanoia.so
%{_libdir}/gstreamer-%{majorminor}/libgstlibvisual.so
%{_libdir}/gstreamer-%{majorminor}/libgstogg.so
%{_libdir}/gstreamer-%{majorminor}/libgstpango.so
%{_libdir}/gstreamer-%{majorminor}/libgsttheora.so
%{_libdir}/gstreamer-%{majorminor}/libgstvorbis.so
%{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
%{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so

%package -n %{gstreamer}-plugins-base-tools
Summary:        tools for GStreamer streaming media framework base plugins
Requires:       %{name} = %{version}-%{release}

%description -n %{gstreamer}-plugins-base-tools
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains the command-line tools for the base plugins.
These include:

* gst-discoverer

%files -n %{gstreamer}-plugins-base-tools
%defattr(-, root, root, -)
%{_bindir}/gst-discoverer-%{majorminor}

%package devel
Summary:        GStreamer Base Plugins Development files
Requires:       %{name} = %{version}-%{release}

%description devel
GStreamer Base Plugins library development and header files. Documentation
is provided by the gstreamer-plugins-base-devel-docs package.

%files devel
%defattr(-, root, root)
# plugin helper library headers
%dir %{_includedir}/gstreamer-%{majorminor}/gst/app
%{_includedir}/gstreamer-%{majorminor}/gst/app/gstappbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/gstappsink.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/gstappsrc.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/audio
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioclock.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiodecoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioencoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiofilter.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioiec61937.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiosink.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiosrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstbaseaudiosink.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstbaseaudiosrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstringbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/mixerutils.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/multichannel.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/cdda
%{_includedir}/gstreamer-%{majorminor}/gst/cdda/gstcddabasesrc.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/floatcast
%{_includedir}/gstreamer-%{majorminor}/gst/floatcast/floatcast.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/fft
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstfft*.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/interfaces
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/colorbalance.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/colorbalancechannel.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/interfaces-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/mixer.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/mixeroptions.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/mixertrack.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/navigation.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/propertyprobe.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/tuner.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/tunerchannel.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/tunernorm.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/videoorientation.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/streamvolume.h
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/xoverlay.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/netbuffer
%{_includedir}/gstreamer-%{majorminor}/gst/netbuffer/gstnetbuffer.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/pbutils
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/codec-utils.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/descriptions.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/encoding-profile.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/encoding-target.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/gstdiscoverer.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/gstpluginsbaseversion.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/install-plugins.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/missing-plugins.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/pbutils.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/pbutils-enumtypes.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/riff
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-ids.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-media.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-read.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/rtp
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstbasertpaudiopayload.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstbasertpdepayload.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstbasertppayload.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtcpbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtppayloads.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/rtsp
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsp-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspbase64.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspconnection.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspdefs.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspextension.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspmessage.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsprange.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsptransport.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspurl.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/sdp/
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/gstsdp.h
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/gstsdpmessage.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/tag
%{_includedir}/gstreamer-%{majorminor}/gst/tag/xmpwriter.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/gsttagdemux.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/gsttagmux.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/tag.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/video
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideofilter.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideosink.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-overlay-composition.h

%{_libdir}/libgstaudio-%{majorminor}.so
%{_libdir}/libgstinterfaces-%{majorminor}.so
%{_libdir}/libgstnetbuffer-%{majorminor}.so
%{_libdir}/libgstriff-%{majorminor}.so
%{_libdir}/libgstrtp-%{majorminor}.so
%{_libdir}/libgsttag-%{majorminor}.so
%{_libdir}/libgstvideo-%{majorminor}.so
%{_libdir}/libgstcdda-%{majorminor}.so
%{_libdir}/libgstpbutils-%{majorminor}.so
%{_libdir}/libgstrtsp-%{majorminor}.so
%{_libdir}/libgstsdp-%{majorminor}.so
%{_libdir}/libgstfft-%{majorminor}.so
%{_libdir}/libgstapp-%{majorminor}.so

%dir %{_datadir}/gst-plugins-base
%{_datadir}/gst-plugins-base/license-translations.dict

%{_datadir}/gir-1.0/GstApp-0.10.gir
%{_datadir}/gir-1.0/GstAudio-0.10.gir
%{_datadir}/gir-1.0/GstFft-0.10.gir
%{_datadir}/gir-1.0/GstInterfaces-0.10.gir
%{_datadir}/gir-1.0/GstNetbuffer-0.10.gir
%{_datadir}/gir-1.0/GstPbutils-0.10.gir
%{_datadir}/gir-1.0/GstRiff-0.10.gir
%{_datadir}/gir-1.0/GstRtp-0.10.gir
%{_datadir}/gir-1.0/GstRtsp-0.10.gir
%{_datadir}/gir-1.0/GstSdp-0.10.gir
%{_datadir}/gir-1.0/GstTag-0.10.gir
%{_datadir}/gir-1.0/GstVideo-0.10.gir

# pkg-config files
%{_libdir}/pkgconfig/*.pc

%package devel-docs
Summary: Developer documentation for GStreamer Base plugins library
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description devel-docs
This package contains developer documentation for the GStreamer Base Plugins
library.

%files devel-docs
%defattr(-, root, root)
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%doc %{_datadir}/gtk-doc/html/gst-plugins-base-libs-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gst-plugins-base-plugins-%{majorminor}

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.10.36-14
- Rebuild for new 4.0 release.

