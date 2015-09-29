%define         gstreamer       gstreamer0
%define         majorminor      0.10

%define         _glib2                  2.22
%define         _libxml2                2.4.0
%define         _gobject_introspection  0.6.3

Name:           %{gstreamer}
Version:        0.10.36
Release:        13%{?dist}
Summary:        GStreamer streaming media framework runtime

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
#Source:         http://gstreamer.freedesktop.org/src/gstreamer/pre/gstreamer-%{version}.tar.xz
Source:         http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.xz
# http://cgit.freedesktop.org/gstreamer/gstreamer/patch/?id=60516f4
Patch0:         gstreamer-0.10.36-bison3.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       %{gstreamer}-tools >= %{version}

BuildRequires:  glib2-devel >= %{_glib2}
BuildRequires:  libxml2-devel >= %{_libxml2}
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  m4
BuildRequires:  check-devel
BuildRequires:  gtk-doc >= 1.3
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  gobject-introspection-devel >= %{_gobject_introspection}
# We need to use the system libtool or else we end up with RPATHs
BuildRequires:  libtool
BuildRequires:  chrpath

# because AM_PROG_LIBTOOL was used in configure.ac
BuildRequires:  gcc

# For the GStreamer RPM provides
Patch1:         gstreamer-inspect-rpm-format.patch
Source1:        gstreamer.prov
Source2:        gstreamer.attr

### documentation requirements
BuildRequires:  python2
BuildRequires:  openjade
BuildRequires:  libxslt
BuildRequires:  docbook-style-dsssl
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-utils
BuildRequires:  ghostscript

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

%package devel
Summary:        Libraries/include files for GStreamer streaming media framework
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel >= %{_glib2}
Requires:       libxml2-devel >= %{_libxml2}
Requires:       check-devel

%description devel
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new   
plugins.

This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer. If you plan to develop applications
with GStreamer, consider installing the gstreamer-devel-docs package and the
documentation packages for any plugins you intend to use.

%package devel-docs
Summary: Developer documentation for GStreamer streaming media framework
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
# for /usr/share/gtk-doc/html
Requires: gtk-doc
BuildArch: noarch

%description devel-docs
This package contains developer documentation for the GStreamer streaming
media framework.

%package -n %{gstreamer}-tools
Summary:        common tools and files for GStreamer streaming media framework
Group:          Applications/Multimedia
# gst-feedback uses these
Requires:       which, pkgconfig

%description -n %{gstreamer}-tools
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new   
plugins.

This package contains wrapper scripts for the command-line tools that work
with different major/minor versions of GStreamer.

%prep
%setup -q -n gstreamer-%{version}
%patch0 -p1 -b .bison3
%patch1 -p1 -b .rpm-provides

%build
%configure \
  --disable-gtk-doc \
  --enable-debug \
  --disable-tests \
  --disable-examples

make %{?_smp_mflags} ERROR_CFLAGS="" LIBTOOL="%{_bindir}/libtool"

%install  
rm -rf $RPM_BUILD_ROOT

# Install doc temporarily in order to be included later by rpm
make install DESTDIR=$RPM_BUILD_ROOT

# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstbase-0.10.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstcoreindexers.so

%find_lang gstreamer-%{majorminor}
# Clean out files that should not be part of the rpm. 
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Create empty cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gstreamer-%{majorminor}
# Add the provides script
install -m0755 -D %{SOURCE1} $RPM_BUILD_ROOT%{_rpmconfigdir}/gstreamer.prov
# Add the gstreamer plugin file attribute entry (rpm >= 4.9.0)
install -m0644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs/gstreamer.attr

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gstreamer-%{majorminor}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING NEWS README RELEASE
%{_libdir}/libgstreamer-%{majorminor}.so.*
%{_libdir}/libgstbase-%{majorminor}.so.*
%{_libdir}/libgstcontroller-%{majorminor}.so.*
%{_libdir}/libgstdataprotocol-%{majorminor}.so.*
%{_libdir}/libgstnet-%{majorminor}.so.*
%{_libexecdir}/gstreamer-%{majorminor}/

%dir %{_libdir}/gstreamer-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoreindexers.so

%{_libdir}/girepository-1.0/Gst-0.10.typelib
%{_libdir}/girepository-1.0/GstBase-0.10.typelib
%{_libdir}/girepository-1.0/GstCheck-0.10.typelib
%{_libdir}/girepository-1.0/GstController-0.10.typelib
%{_libdir}/girepository-1.0/GstNet-0.10.typelib

%{_bindir}/gst-feedback-%{majorminor}
%{_bindir}/gst-inspect-%{majorminor}
%{_bindir}/gst-launch-%{majorminor}
%{_bindir}/gst-typefind-%{majorminor}
%{_bindir}/gst-xmlinspect-%{majorminor}
%{_bindir}/gst-xmllaunch-%{majorminor}

%doc %{_mandir}/man1/gst-feedback-%{majorminor}.*
%doc %{_mandir}/man1/gst-inspect-%{majorminor}.*
%doc %{_mandir}/man1/gst-launch-%{majorminor}.*
%doc %{_mandir}/man1/gst-typefind-%{majorminor}.*
%doc %{_mandir}/man1/gst-xmlinspect-%{majorminor}.*
%doc %{_mandir}/man1/gst-xmllaunch-%{majorminor}.*

%files -n %{gstreamer}-tools
%defattr(-, root, root, -)
%{_bindir}/gst-feedback
%{_bindir}/gst-inspect
%{_bindir}/gst-launch
%{_bindir}/gst-typefind
%{_bindir}/gst-xmlinspect
%{_bindir}/gst-xmllaunch

%files devel
%defattr(-, root, root, -)
%dir %{_includedir}/gstreamer-%{majorminor}
%dir %{_includedir}/gstreamer-%{majorminor}/gst
%{_includedir}/gstreamer-%{majorminor}/gst/*.h

%{_includedir}/gstreamer-%{majorminor}/gst/base
%{_includedir}/gstreamer-%{majorminor}/gst/check
%{_includedir}/gstreamer-%{majorminor}/gst/controller
%{_includedir}/gstreamer-%{majorminor}/gst/dataprotocol
%{_includedir}/gstreamer-%{majorminor}/gst/net

%{_libdir}/libgstreamer-%{majorminor}.so
%{_libdir}/libgstdataprotocol-%{majorminor}.so
%{_libdir}/libgstbase-%{majorminor}.so
%{_libdir}/libgstcheck-%{majorminor}.so*
%{_libdir}/libgstcontroller-%{majorminor}.so
%{_libdir}/libgstnet-%{majorminor}.so

%{_datadir}/gir-1.0/Gst-0.10.gir
%{_datadir}/gir-1.0/GstBase-0.10.gir
%{_datadir}/gir-1.0/GstCheck-0.10.gir
%{_datadir}/gir-1.0/GstController-0.10.gir
%{_datadir}/gir-1.0/GstNet-0.10.gir

%{_datadir}/aclocal/gst-element-check-%{majorminor}.m4
%{_libdir}/pkgconfig/gstreamer-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-dataprotocol-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{majorminor}.pc

%{_rpmconfigdir}/gstreamer.prov
%{_rpmconfigdir}/fileattrs/gstreamer.attr

%files devel-docs
%defattr(-, root, root, -)
%doc %{_datadir}/gtk-doc/html/gstreamer-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gstreamer-libs-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gstreamer-plugins-%{majorminor}

%changelog
