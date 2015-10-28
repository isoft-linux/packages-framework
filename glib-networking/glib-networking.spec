%define glib2_version 2.42

Name:           glib-networking
Version:        2.46.1
Release:        2
Summary:        Networking support for GLib

License:        LGPLv2+
URL:            http://www.gnome.org
Source:         http://download.gnome.org/sources/glib-networking/2.36/%{name}-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gnutls-devel
BuildRequires:  intltool
BuildRequires:  ca-certificates
BuildRequires:  libproxy-devel
BuildRequires:  gsettings-desktop-schemas-devel

Requires:       ca-certificates
Requires:       glib2%{?_isa} >= %{glib2_version}

%description
This package contains modules that extend the networking support in
GIO. In particular, it contains libproxy- and GSettings-based
GProxyResolver implementations and a gnutls-based GTlsConnection
implementation.

%prep
%setup -q


%build
#the ca-certificates is important.
#some implementations who using libsoup will depend on this key to handle https protocol.
#for example, geoclue2/webkitgtk and so on.
#By Cjacker!

%configure --disable-static --with-libproxy --with-gnome-proxy --with-ca-certificates=/etc/pki/tls/certs/ca-bundle.crt

make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la

%find_lang %{name}

%post
gio-querymodules %{_libdir}/gio/modules

%postun
gio-querymodules %{_libdir}/gio/modules

%files -f %{name}.lang
%{_libdir}/gio/modules/libgiognutls.so
%{_libdir}/gio/modules/libgiognomeproxy.so
%{_libdir}/gio/modules/libgiolibproxy.so
%{_libexecdir}/glib-pacrunner
%{_datadir}/dbus-1/services/org.gtk.GLib.PACRunner.service

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.46.1-2
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 2.46.1

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

