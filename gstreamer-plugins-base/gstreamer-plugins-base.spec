%global with_x11 1


%define majorminor 1.0
%define gstreamer gstreamer

%define gst_minver 1.0 

Name: %{gstreamer}-plugins-base
Version: 1.6.1
Release: 2
Summary: GStreamer streaming media framework plug-ins

License: LGPL
URL: http://gstreamer.freedesktop.org/
Vendor: GStreamer Backpackers Team <package@gstreamer.freedesktop.org>
Source: http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-%{version}.tar.xz

Requires: %{gstreamer} >= %{gst_minver}
BuildRequires: %{gstreamer}-devel >= %{gst_minver}
BuildRequires: gobject-introspection-devel >= 0.9.12

BuildRequires: gstreamer-devel >= %{version}
BuildRequires: gobject-introspection-devel >= 1.31.1
BuildRequires: iso-codes-devel

BuildRequires: alsa-lib-devel
BuildRequires: libcdio-paranoia-devel
BuildRequires: libogg-devel >= 1.0
BuildRequires: libtheora-devel >= 1.1
BuildRequires: libvisual-devel
BuildRequires: libvorbis-devel >= 1.0
BuildRequires: libXv-devel
BuildRequires: libX11-devel
BuildRequires: orc-devel >= 0.4.18
BuildRequires: pango-devel
BuildRequires: pkgconfig

BuildRequires: chrpath

# documentation
BuildRequires: gtk-doc >= 1.3

Requires: iso-codes

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related. Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

%package devel
Summary: GStreamer Plugin Library Headers
Requires: %{gstreamer}-plugins-base = %{version}

%description devel
GStreamer Plugins Base library development and header files.

%if %with_x11
%package x11
Summary: Xorg related plugin of gstreamer
Requires: %{name} = %{version}-%{release}

%description x11
Xorg related plugin of gstreamer
%endif


%prep
%setup -q -n gst-plugins-base-%{version} 

%build
%configure \
    --disable-gtk-doc \
    --enable-introspection=yes \
    --disable-fatal-warnings

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
%exclude %{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
%exclude %{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so
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
* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 1.6.1-2
- Update to 1.6.1

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.6.0-2
- Rebuild for new 4.0 release.

* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

