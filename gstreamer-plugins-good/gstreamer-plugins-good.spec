%global with_x11 1

%define majorminor  1.0
%define gstreamer   gstreamer

%define gst_minver  1.0 

Name: 		%{gstreamer}-plugins-good
Version: 	1.6.0
Release: 	1
Summary: 	GStreamer plug-ins with good code and licensing

Group: 		Applications/Multimedia
License: 	LGPL
URL:		http://gstreamer.freedesktop.org/
Vendor:         GStreamer Backpackers Team <package@gstreamer.freedesktop.org>
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-%{version}.tar.xz

Requires: 	  %{gstreamer} >= %{gst_minver}
BuildRequires: 	  %{gstreamer}-devel >= %{gst_minver}

BuildRequires:  libvpx-devel
BuildRequires:  libspeex-devel
BuildRequires:  libflac-devel
BuildRequires:  libdv-devel
BuildRequires:  libraw1394-devel
BuildRequires:  libavc1394-devel
BuildRequires:  libiec61883-devel
BuildRequires:  wavpack-devel

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel >= 1.2.0
BuildRequires: pulseaudio-libs-devel

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

%if %with_x11
%package x11
Summary:        Xorg related plugin of gstreamer
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description x11
Xorg related plugin of gstreamer
%endif

%prep
%setup -q -n gst-plugins-good-%{version}

%build
%configure --disable-fatal-warnings 
make %{?_smp_mflags}
                                                                                
%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
                                                                                
# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang gst-plugins-good-%{majorminor}

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%post

%files -f gst-plugins-good-%{majorminor}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING README REQUIREMENTS gst-plugins-good.doap
%{_datadir}/gstreamer-%{majorminor}/presets/*.prs
%{_libdir}/gstreamer-%{majorminor}/*.so
%{_datadir}/gtk-doc/html/*
%if %with_x11
%exclude  %{_libdir}/gstreamer-%{majorminor}/libgstximagesrc.so
%endif



%if %with_x11
%files x11
%{_libdir}/gstreamer-%{majorminor}/libgstximagesrc.so
%endif



%changelog
* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

