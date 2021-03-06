Name:           at-spi2-core
Version:        2.18.3
Release:        2
Summary:        Protocol definitions and daemon for D-Bus at-spi

License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:        http://download.gnome.org/sources/at-spi2-core/2.4/%{name}-%{version}.tar.xz

BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXevie-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  autoconf automake libtool
BuildRequires:  intltool
#for _userunitdir macro
BuildRequires:  systemd

Requires:       dbus

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

%package devel
Summary: Development files and headers for at-spi2-core
Requires: %{name} = %{version}-%{release}

%description devel
The at-spi2-core-devel package includes the header files and
API documentation for libatspi.

%prep
%setup -q

%build
%configure --with-dbus-daemondir=/bin

sed -i -e 's+sys_lib_dlsearch_path_spec="/lib /usr/lib+sys_lib_dlsearch_path_spec="/lib /usr/lib /lib64 /usr/lib64+' configure

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT DATADIRNAME=share

rm $RPM_BUILD_ROOT%{_libdir}/libatspi.la

%{find_lang} %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%{_libexecdir}/at-spi2-registryd
%{_sysconfdir}/at-spi2
%{_sysconfdir}/xdg/autostart/at-spi-dbus-bus.desktop
%{_libdir}/libatspi.so.*
%{_libdir}/girepository-1.0/Atspi-2.0.typelib
%{_libexecdir}/at-spi-bus-launcher
%{_datadir}/dbus-1/services/org.a11y.Bus.service
%{_datadir}/dbus-1/accessibility-services/org.a11y.atspi.Registry.service
#%{_userunitdir}/at-spi-dbus-bus.service

%files devel
%{_libdir}/libatspi.so
%{_datadir}/gtk-doc/html/libatspi
%{_datadir}/gir-1.0/Atspi-2.0.gir
%{_includedir}/at-spi-2.0
%{_libdir}/pkgconfig/atspi-2.pc

%changelog
* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 2.18.3-2
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.18.1-2
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 2.18.1

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

