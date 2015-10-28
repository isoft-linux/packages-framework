Summary:   GLib wrapper around libusb1
Name:      libgusb
Version:   0.2.5
Release:   2 
License:   LGPLv2+
URL:       https://gitorious.org/gusb/
Source0:   http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz

BuildRequires: glib2-devel >= 2.16.1
BuildRequires: libtool
BuildRequires: libgudev-devel
BuildRequires: libusb-devel
BuildRequires: gobject-introspection-devel
BuildRequires: vala-devel
BuildRequires: vala-tools

%description
GUsb is a GObject wrapper for libusb1 that makes it easy to do
asynchronous control, bulk and interrupt transfers with proper
cancellation and integration into a mainloop.

%package devel
Summary: Libraries and headers for gusb
Requires: %{name} = %{version}-%{release}

%description devel
GLib headers and libraries for gusb.

%prep
%setup -q

%build
%configure \
        --disable-static                \
        --enable-vala=yes               \
        --enable-introspection=yes      \
        --disable-gtk-doc               \
        --enable-gudev                  \
        --disable-dependency-tracking

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libgusb.la

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README AUTHORS NEWS COPYING
%{_libdir}/libgusb.so.?
%{_libdir}/libgusb.so.?.0.*
%{_libdir}/girepository-1.0/GUsb-1.0.typelib

%files devel
%defattr(-,root,root,-)
%{_includedir}/gusb-1
%{_libdir}/libgusb.so
%{_libdir}/pkgconfig/gusb.pc
%{_datadir}/gtk-doc/html/gusb
%{_datadir}/gir-1.0/GUsb-1.0.gir
%{_datadir}/vala/vapi/gusb.vapi

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.2.5-2
- Rebuild for new 4.0 release.

