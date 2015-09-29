%define majorminor  1.0
%define gstreamer   gstreamer

%define gst_minver  1.0 

Name: 		%{gstreamer}-plugins-ugly
Version: 	1.6.0
Release: 	1
Summary: 	GStreamer streaming media framework "ugly" plug-ins

Group: 		Applications/Multimedia
License: 	LGPL
URL:		http://gstreamer.freedesktop.org/
Vendor:         GStreamer Backpackers Team <package@gstreamer.freedesktop.org>
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.xz

Requires: 	%{gstreamer} >= %{gst_minver}
BuildRequires: 	%{gstreamer}-devel >= %{gst_minver}
BuildRequires:  libmad-devel
BuildRequires:  x264-devel
BuildRequires:  mpeg2dec-devel
BuildRequires:  a52dec-devel
BuildRequires:  libcdio-devel
Provides:       gstreamer-sid = %{version}-%{release}
Provides:       gstreamer-mad = %{version}-%{release}
Provides:       gstreamer-a52dec = %{version}-%{release}
Provides:       gstreamer-dvdread = %{version}-%{release}
Provides:       gstreamer-mpeg2dec = %{version}-%{release}

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains well-written plug-ins that can't be shipped in
gstreamer-plugins-good because:
- the license is not LGPL
- the license of the library is not LGPL
- there are possible licensing issues with the code.

# %package devel
# Summary:        Development files for GStreamer Ugly Plugins
# Group:          Development/Libraries
#
# Requires:       %{name} = %{version}-%{release}
#
# %description devel
# GStreamer is a streaming media framework, based on graphs of elements which
# operate on media data.
#
# This package contains well-written plug-ins that can't be shipped in
# gstreamer-plugins-good because:
# - the license is not LGPL
# - the license of the library is not LGPL
# - there are possible licensing issues with the code.
# 
# This package contains development files and documentation.

%prep
%setup -q -n gst-plugins-ugly-%{version}
%build
%configure \
    --disable-gtk-doc 

make %{?_smp_mflags}
                                                                                
%install
rm -rf $RPM_BUILD_ROOT

# Install doc temporarily in order to be included later by rpm
%makeinstall

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang gst-plugins-ugly-%{majorminor}

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files -f gst-plugins-ugly-%{majorminor}.lang
%defattr(-, root, root, -)
%{_libdir}/gstreamer-%{majorminor}/*.so
%{_datadir}/gstreamer-*/presets/GstX264Enc.prs
%doc %{_datadir}/gtk-doc/html/*


%changelog
* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

