Name:	    gssdp	
Version:	0.14.11
Release:	2
Summary:    Resource discovery and announcement over SSDP	

License:	GPL
URL:		http://www.gnome.org
Source0:	%{name}-%{version}.tar.xz

%description
The Gssdp package provides a GObject based API for handling resource discovery and announcement over SSDP (Simple Service Discovery Protocol).

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
%description devel
%{summary}.

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/gssdp-device-sniffer
%{_datadir}/gssdp/gssdp-device-sniffer.ui
%{_libdir}/libgssdp-1.0.so.*
%{_libdir}/girepository-1.0/GSSDP-1.0.typelib

%files devel
%{_includedir}/gssdp-1.0
%{_libdir}/libgssdp-1.0.so
%{_libdir}/pkgconfig/gssdp-1.0.pc
%{_datadir}/gir-1.0/GSSDP-1.0.gir
%{_datadir}/gtk-doc/html/gssdp
%{_datadir}/vala/vapi/gssdp-1.0.deps
%{_datadir}/vala/vapi/gssdp-1.0.vapi


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 0.14.11-2
- Rebuild for 4.0 release


