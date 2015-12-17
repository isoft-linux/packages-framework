%define majorminor  1.0
%define gstreamer   gstreamer
%define gst_majorminor  1.0

Name: %{gstreamer}-vaapi
Version: 0.7.0
Release: 3 
Summary: VA-API support to GStreamer
License: LGPL
URL: http://freedesktop.org/wiki/Software/vaapi
Source0: http://www.freedesktop.org/software/vaapi/releases/gstreamer-vaapi/gstreamer-vaapi-%{version}.tar.bz2

Patch0: gstreamer-vaapi-fix-glx-pkgconfig.patch

BuildRequires:  glib2-devel >= 2.28
BuildRequires:  %{gstreamer}-devel >= 1.0.0
BuildRequires:  %{gstreamer}-plugins-base-devel >= 1.0.0
BuildRequires:  %{gstreamer}-plugins-bad-devel >= 1.0.0
BuildRequires:  libva-devel >= 1.1.0
BuildRequires:  libdrm-devel
BuildRequires:  libudev-devel
BuildRequires:  libGL-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  libvpx-devel
BuildRequires:  yasm
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(wayland-egl)

BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client) >= 1
BuildRequires:  pkgconfig(wayland-cursor) >= 1
BuildRequires:  pkgconfig(wayland-scanner) >= 1
BuildRequires:  pkgconfig(wayland-server) >= 1

%description
gstreamer-vaapi consists in a collection of VA-API based plugins for
GStreamer and helper libraries.

%prep
%setup -q -n gstreamer-vaapi-%{version}
%patch0 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_majorminor}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%{_libdir}/gstreamer-%{gst_majorminor}/*.so
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%changelog
* Thu Dec 17 2015 Cjacker <cjacker@foxmail.com> - 0.7.0-3
- Fix glx pkgconfig

* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 0.7.0-2
- Update, VP9 decoder

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.6.0-4
- Rebuild for new 4.0 release.

* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- rebuild with libva-1.6.1 and gstreamer-1.6.0

* Thu Jul 16 2015 Cjacker <cjacker@foxmail.com>
- update to 0.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

