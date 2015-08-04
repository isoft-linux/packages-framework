%define		gstreamer	gstreamer
%define		majorminor	1.0

%define 	_glib2		2.32.0

Name: 		%{gstreamer}
Version: 	1.5.2
Release: 	1
Summary: 	GStreamer streaming media framework runtime

Group: 		Applications/Multimedia
License: 	LGPL
URL:		http://gstreamer.freedesktop.org/
Source: 	http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: 	glib2-devel >= %{_glib2}
BuildRequires: 	bison
BuildRequires: 	flex
BuildRequires: 	m4
#BuildRequires: 	gtk-doc >= 1.3
BuildRequires:	gettext

# because AM_PROG_LIBTOOL was used in configure.ac
BuildRequires:	gcc

### documentation requirements
#BuildRequires:  python2
#BuildRequires:  openjade
#BuildRequires:	libxslt
#BuildRequires:  docbook-style-dsssl
#BuildRequires:  docbook-style-xsl
#BuildRequires:  docbook-utils

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

%package devel
Summary: 	Libraries/include files for GStreamer streaming media framework
Group: 		Development/Libraries

Requires: 	%{name} = %{version}-%{release}
Requires: 	glib2-devel >= %{_glib2}

%description devel
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new   
plugins.

This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer, as well as general and API
documentation.

%prep
%setup -q -n gstreamer-%{version}

%build
%configure \
  --with-package-name='gstreamer package' \
  --with-package-origin='http://gstreamer.freedesktop.org' \
  --disable-debug \
  --disable-gtk-doc \
  --disable-docbook \
  --enable-introspection=yes

make %{?_smp_mflags}

%install  
rm -rf $RPM_BUILD_ROOT

# Install doc temporarily in order to be included later by rpm
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang gstreamer-%{majorminor}
# Clean out files that should not be part of the rpm. 
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gstreamer-%{majorminor}
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Create empty cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gstreamer-%{majorminor}

#fix some cmake requires.
pushd %{buildroot}%{_includedir}/gstreamer-1.0/gst
ln -sf %{_libdir}/gstreamer-1.0/include/gst/gstconfig.h .
popd


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gstreamer-%{majorminor}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING NEWS README RELEASE TODO
%{_libdir}/libgst*.so.*
%dir %{_libdir}/gstreamer-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/*.so
%{_bindir}/gst-inspect-*
%{_bindir}/gst-launch-*
%{_bindir}/gst-typefind-*
%{_libexecdir}/gstreamer-%{majorminor}/gst-plugin-scanner
%{_libexecdir}/gstreamer-%{majorminor}/gst-ptp-helper
%doc %{_mandir}/man1/*
%{_libdir}/girepository-?.?/*.typelib
%{_datadir}/gir-?.?/*.gir

%{_datadir}/bash-completion/completions/gst-*
%{_datadir}/bash-completion/helpers/*

%files devel
%defattr(-, root, root, -)
%{_includedir}/gstreamer-*
%{_libdir}/gstreamer-?.?/include/gst/gstconfig.h
%{_libdir}/libgst*.so
%{_datadir}/aclocal/*.m4
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

