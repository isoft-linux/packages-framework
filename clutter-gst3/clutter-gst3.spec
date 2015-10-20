Name:           clutter-gst3
Version:        3.0.14
Release:        1
Summary:        GStreamer integration for Clutter

License:        LGPLv2+
URL:            http://www.clutter-project.org
Source0:        http://ftp.gnome.org/pub/GNOME/sources/clutter-gst/3.0/clutter-gst-%{version}.tar.xz

BuildRequires:  clutter-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel

%description
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

The %{name}-devel package contains libraries and header files for
developing applications that use clutter-gst API version 2.0.

%prep
%setup -q -n clutter-gst-%{version}

%build
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Remove the documentation for now as it conflicts with the files in
# clutter-gst-devel. I'll work with upstream to fix this properly.
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%{_libdir}/girepository-1.0/ClutterGst-3.0.typelib
%{_libdir}/gstreamer-1.0/libgstclutter-3.0.so
%{_libdir}/libclutter-gst-3.0.so.*

%files devel
%{_includedir}/clutter-gst-3.0/
%{_libdir}/libclutter-gst-3.0.so
%{_libdir}/pkgconfig/clutter-gst-3.0.pc
%{_datadir}/gir-1.0/ClutterGst-3.0.gir
#doc #{_datadir}/gtk-doc/

%changelog
* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 3.0.14
* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

