%define majorminor 1.0
%define gstreamer gstreamer

%define gst_minver 1.0 

Name: %{gstreamer}-plugins-good
Version: 1.6.1
Release: 3
Summary: GStreamer plug-ins with good code and licensing

License: LGPL
URL: http://gstreamer.freedesktop.org/
Vendor: GStreamer Backpackers Team <package@gstreamer.freedesktop.org>
Source: http://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-%{version}.tar.xz

Requires: %{gstreamer} >= %{gst_minver}
BuildRequires: %{gstreamer}-devel >= %{gst_minver}

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel >= 1.2.0
BuildRequires: pulseaudio-libs-devel

BuildRequires: gstreamer-devel >= %{version}
BuildRequires: gstreamer-plugins-base-devel >= %{version}

BuildRequires: libflac-devel >= 1.1.4
BuildRequires: gdk-pixbuf2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel >= 1.2.0
BuildRequires: libsoup-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXdamage-devel
BuildRequires: libXfixes-devel
BuildRequires: orc-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libspeex-devel
BuildRequires: taglib-devel
BuildRequires: wavpack-devel
BuildRequires: libv4l-devel
BuildRequires: libvpx-devel >= 1.1.0

BuildRequires: libavc1394-devel
BuildRequires: libdv-devel
BuildRequires: libiec61883-devel
BuildRequires: libraw1394-devel

# documentation
BuildRequires:  gtk-doc
BuildRequires:  python-devel

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related. Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

%package x11
Summary: Xorg related plugin of gstreamer
Requires: %{name} = %{version}-%{release}

%description x11
Xorg related plugin of gstreamer

%prep
%setup -q -n gst-plugins-good-%{version}

%build
%configure --disable-fatal-warnings 
make %{?_smp_mflags}

%install
%makeinstall

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang gst-plugins-good-%{majorminor}


%files -f gst-plugins-good-%{majorminor}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING README REQUIREMENTS gst-plugins-good.doap
%{_datadir}/gstreamer-%{majorminor}/presets/*.prs
%{_libdir}/gstreamer-%{majorminor}/*.so
%{_datadir}/gtk-doc/html/*
%exclude %{_libdir}/gstreamer-%{majorminor}/libgstximagesrc.so

%files x11
%{_libdir}/gstreamer-%{majorminor}/libgstximagesrc.so

%changelog
* Tue Jan 10 2017 sulit - 1.6.1-3
- rebuild

* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 1.6.1-2
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.6.0-2
- Rebuild for new 4.0 release.

* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

