%global with_x11 1


%define majorminor  1.0
%define gstreamer   gstreamer

%define gst_minver  0.11.0

Name: 		%{gstreamer}-plugins-base
Version: 	1.6.0
Release: 	1
Summary: 	GStreamer streaming media framework plug-ins

Group: 		Applications/Multimedia
License: 	LGPL
URL:		http://gstreamer.freedesktop.org/
Vendor:         GStreamer Backpackers Team <package@gstreamer.freedesktop.org>
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-%{version}.tar.xz

Requires: 	%{gstreamer} >= %{gst_minver}
BuildRequires: 	%{gstreamer}-devel >= %{gst_minver}
BuildRequires:  gobject-introspection-devel >= 0.9.12

BuildRequires:  pulseaudio-libs-devel

Requires:      libogg >= 1.0
Requires:      libvorbis >= 1.0
BuildRequires: libogg-devel >= 1.0
BuildRequires: libvorbis-devel >= 1.0
BuildRequires: alsa-lib-devel
Requires:      alsa-lib
BuildRequires: pango-devel
Requires: pango
BuildRequires: libtheora-devel >= 1.0
Requires:      libtheora >= 1.0

%if %with_x11
BuildRequires: libXv-devel
BuildRequires: libX11-devel
%endif


%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

%package devel
Summary: 	GStreamer Plugin Library Headers
Group: 		Development/Libraries
Requires: 	%{gstreamer}-plugins-base = %{version}

%description devel
GStreamer Plugins Base library development and header files.

%if %with_x11
%package x11
Summary:        Xorg related plugin of gstreamer
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description x11
Xorg related plugin of gstreamer
%endif


%prep
%setup -q -n gst-plugins-base-%{version} 

%build
%configure \
    --disable-gtk-doc --enable-introspection=yes --disable-fatal-warnings

make %{?_smp_mflags}

                                                                                
%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang gst-plugins-base-%{majorminor}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f gst-plugins-base-%{majorminor}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING README REQUIREMENTS gst-plugins-base.doap
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/libgst*.so.*
%{_libdir}/gstreamer-%{majorminor}/*.so
%{_libdir}/girepository-?.?/*.typelib
%if %with_x11
%exclude  %{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
%exclude  %{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so
%endif


%if %with_x11
%files x11
%{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
%{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so
%endif


%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/libgst*.so
# pkg-config files
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-?.?/*.gir
%doc %{_datadir}/gtk-doc/html/*
%doc %{_datadir}/gst-plugins-base/%{majorminor}/license-translations.dict

%changelog
* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

