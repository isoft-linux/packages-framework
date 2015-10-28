Name: libdmapsharing
Version: 2.9.30
Release: 4%{?dist}
License: LGPLv2+
Source: http://www.flyn.org/projects/libdmapsharing/%{name}-%{version}.tar.gz
URL: http://www.flyn.org/projects/libdmapsharing/
Summary: A DMAP client and server library
BuildRequires: pkgconfig, glib2-devel, libsoup-devel >= 2.32
BuildRequires: gdk-pixbuf2-devel, gstreamer-plugins-base-devel
BuildRequires: pkgconfig(avahi-client) pkgconfig(avahi-glib)
BuildRequires: vala-tools libgee-devel

%description 
libdmapsharing implements the DMAP protocols. This includes support for
DAAP and DPAP.


%package devel
Summary: Libraries/include files for libdmapsharing
Requires: %{name} = %{version}-%{release}

%description devel
libdmapsharing implements the DMAP protocols. This includes support for
DAAP and DPAP.  This package provides the libraries, include files, and
other resources needed for developing applications using libdmapsharing.

%package vala
Summary: Vala language bindings for libdmapsharing
Requires: %{name} = %{version}-%{release}

%description vala
libdmapsharing implements the DMAP protocols. This includes support for
DAAP and DPAP.  This package provides the Vala language bindings for
libdmapsharing.

%prep
%setup -q

%build
%configure --disable-static --disable-tests
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdmapsharing-3.0.la


%files 
%{_libdir}/libdmapsharing-3.0.so.*
%doc AUTHORS COPYING ChangeLog README

%files devel
%{_libdir}/pkgconfig/libdmapsharing-3.0.pc
%{_includedir}/libdmapsharing-3.0/
%{_libdir}/libdmapsharing-3.0.so
%{_libdir}/girepository-1.0/DMAP-3.0.typelib
%{_datadir}/gtk-doc/html/libdmapsharing-3.0
%{_datadir}/gir-1.0/DMAP-3.0.gir

%files vala
%{_datadir}/vala/vapi/libdmapsharing-3.0.vapi

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.9.30-4
- Rebuild for new 4.0 release.

* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- initial build.
