%define majorminor  1.0
%define gstreamer   gstreamer
%define gst_majorminor  1.0

Name: %{gstreamer}-vaapi
Version: 0.6.0
Release: 3 
Summary: VA-API support to GStreamer
Group: Libraries/Multimedia
License: LGPL
URL: http://freedesktop.org/wiki/Software/vaapi
Source: http://www.freedesktop.org/software/vaapi/releases/gstreamer-vaapi/gstreamer-vaapi-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: %{gstreamer} >= 0.9.7
BuildRequires: %{gstreamer}-devel >= 0.9.7

%description
gstreamer-vaapi consists in a collection of VA-API based plugins for
GStreamer and helper libraries.

%prep
%setup -q -n gstreamer-vaapi-%{version}

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
* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- rebuild with libva-1.6.1 and gstreamer-1.6.0

* Fri Jul 16 2015 Cjacker <cjacker@foxmail.com>
- update to 0.6.0

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

