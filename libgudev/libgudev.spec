Name:		libgudev
Version:    230	
Release:	2
Summary:    Libraries for adding libudev support to applications that use glib	

License:	GPL
URL:		http://wiki.gnome.org/Projects/libgudev
Source0:    %{name}-%{version}.tar.xz

BuildRequires:  systemd-devel, glib2-devel	
Requires:	systemd-libs, glib2

%description
Libraries for adding libudev support to applications that use glib

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%{_libdir}/libgudev-1.0.so.*
%{_libdir}/girepository-1.0/GUdev-1.0.typelib

%files devel
%{_libdir}/libgudev-1.0.so
%dir %{_includedir}/gudev-1.0
%dir %{_includedir}/gudev-1.0/gudev
%{_includedir}/gudev-1.0/gudev/*.h
%{_libdir}/pkgconfig/gudev-1.0*
%{_datadir}/gir-1.0/GUdev-1.0.gir

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 230-2
- Rebuild for new 4.0 release.


