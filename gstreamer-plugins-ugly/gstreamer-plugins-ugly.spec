%define majorminor 1.0
%define gstreamer gstreamer

%define gst_minver 1.0 

Name: %{gstreamer}-plugins-ugly
Version: 1.6.1
Release: 2
Summary: GStreamer streaming media framework "ugly" plug-ins

License: LGPL
URL: http://gstreamer.freedesktop.org/

Source0: http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.xz

BuildRequires: %{gstreamer}-devel >= %{gst_minver}
BuildRequires: %{gstreamer}-plugins-base-devel >= %{gst_minver}
BuildRequires: check
BuildRequires: gettext-devel
BuildRequires: libXt-devel
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel

BuildRequires: libmad-devel
BuildRequires: x264-devel
BuildRequires: mpeg2dec-devel
BuildRequires: a52dec-devel
BuildRequires: libcdio-devel
BuildRequires: libmad-devel
BuildRequires: libdvdread-devel
BuildRequires: orc-devel

BuildRequires: chrpath

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains well-written plug-ins that can't be shipped in
gstreamer-plugins-good because:
- the license is not LGPL
- the license of the library is not LGPL
- there are possible licensing issues with the code.

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

%files -f gst-plugins-ugly-%{majorminor}.lang
%defattr(-, root, root, -)
%{_libdir}/gstreamer-%{majorminor}/*.so
%{_datadir}/gstreamer-*/presets/GstX264Enc.prs
%doc %{_datadir}/gtk-doc/html/*


%changelog
* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 1.6.1-2
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.6.0-2
- Rebuild for new 4.0 release.

* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

