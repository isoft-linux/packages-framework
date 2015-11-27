Name:	    gupnp	
Version:    0.20.14
Release:	2
Summary:    A framework for creating UPnP devices & control points	

License:	GPL
URL:		http://www.gnome.org
Source0:	%{name}-%{version}.tar.xz
BuildRequires: gssdp-devel

%description
GUPnP is an object-oriented open source framework for creating UPnP
devices and control points, written in C using GObject and libsoup.
The GUPnP API is intended to be easy to use, efficient and flexible.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
%description devel
%{summary}.



%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


rm -rf $RPM_BUILD_ROOT%{_libdir}/libgupnp*.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/girepository-1.0/GUPnP-1.0.typelib
%{_libdir}/libgupnp-1.0.so.*

%files devel
%{_bindir}/gupnp-binding-tool
%{_includedir}/gupnp-1.0
%{_libdir}/libgupnp-1.0.so
%{_libdir}/pkgconfig/gupnp-1.0.pc
%{_datadir}/gir-1.0/GUPnP-1.0.gir
%{_datadir}/gtk-doc/html/gupnp
%{_datadir}/vala/vapi/gupnp-1.0.deps
%{_datadir}/vala/vapi/gupnp-1.0.vapi


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 0.20.14-2
- Rebuild for 4.0 release


