Name:          geoclue
Version:       0.12.99
Release:       9%{?dist}
Summary:       A modular geoinformation service

License:       LGPLv2
URL:           http://geoclue.freedesktop.org/
Source0:       http://people.freedesktop.org/~hadess/%{name}-%{version}.tar.gz

BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: glib2-devel
BuildRequires: libxml2-devel
BuildRequires: libsoup-devel
BuildRequires: gtk3-devel
BuildRequires: NetworkManager-devel >= 1:0.8.997
BuildRequires: NetworkManager-glib-devel >= 1:0.8.997
BuildRequires: gypsy-devel
BuildRequires: gtk-doc

Obsoletes: geoclue-gpsd
Requires: dbus

%description
Geoclue is a modular geoinformation service built on top of the D-Bus 
messaging system. The goal of the Geoclue project is to make creating 
location-aware applications as simple as possible. 

%package devel
Summary: Development package for geoclue
Requires: %{name} = %{version}-%{release}
Requires: dbus-devel
Requires: libxml2-devel
Requires: pkgconfig

%description devel
Files for development with geoclue.

%package doc
Summary: Developer documentation for geoclue
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Developer documentation for geoclue

%package gui
Summary: Testing gui for geoclue
Requires: %{name} = %{version}-%{release}

%description gui
Testing gui for geoclue

%package gypsy
Summary: gypsy provider for geoclue
Requires: %{name} = %{version}-%{release}

%description gypsy
A gypsy provider for geoclue

%package gsmloc
Summary: gsmloc provider for geoclue
Requires: %{name} = %{version}-%{release}

%description gsmloc
A gsmloc provider for geoclue

%prep
%setup -q
sed -i -e "s/gtk+-2.0/gtk+-3.0/" configure

%build
%configure --disable-static --enable-gtk-doc --enable-networkmanager=yes --enable-gypsy=yes --enable-skyhook=yes --enable-gsmloc=yes --enable-gpsd=no
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Install the test gui as it seems the test isn't installed any more
mkdir $RPM_BUILD_ROOT%{_bindir}
cp test/.libs/geoclue-test-gui $RPM_BUILD_ROOT%{_bindir}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{_datadir}/geoclue-providers
%{_libdir}/libgeoclue.so.0
%{_libdir}/libgeoclue.so.0.0.0
%{_datadir}/GConf/gsettings/geoclue
%{_datadir}/glib-2.0/schemas/org.freedesktop.Geoclue.gschema.xml
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Master.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Example.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Geonames.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Hostip.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Localnet.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Manual.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Nominatim.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Plazes.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Skyhook.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Yahoo.service
%{_datadir}/geoclue-providers/geoclue-example.provider
%{_datadir}/geoclue-providers/geoclue-geonames.provider
%{_datadir}/geoclue-providers/geoclue-hostip.provider
%{_datadir}/geoclue-providers/geoclue-localnet.provider
%{_datadir}/geoclue-providers/geoclue-manual.provider
%{_datadir}/geoclue-providers/geoclue-nominatim.provider
%{_datadir}/geoclue-providers/geoclue-plazes.provider
%{_datadir}/geoclue-providers/geoclue-skyhook.provider
%{_datadir}/geoclue-providers/geoclue-yahoo.provider
%{_libexecdir}/geoclue-example
%{_libexecdir}/geoclue-geonames
%{_libexecdir}/geoclue-hostip
%{_libexecdir}/geoclue-localnet
%{_libexecdir}/geoclue-manual
%{_libexecdir}/geoclue-nominatim
%{_libexecdir}/geoclue-master
%{_libexecdir}/geoclue-plazes
%{_libexecdir}/geoclue-skyhook
%{_libexecdir}/geoclue-yahoo

%files devel
%defattr(-,root,root,-)
%{_includedir}/geoclue
%{_libdir}/pkgconfig/geoclue.pc
%{_libdir}/libgeoclue.so

%files doc
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/geoclue/

%files gui
%defattr(-,root,root,-)
%{_bindir}/geoclue-test-gui

%files gypsy
%defattr(-,root,root,-)
%{_libexecdir}/geoclue-gypsy
%{_datadir}/geoclue-providers/geoclue-gypsy.provider
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Gypsy.service

%files gsmloc
%defattr(-,root,root,-)
%{_libexecdir}/geoclue-gsmloc
%{_datadir}/geoclue-providers/geoclue-gsmloc.provider
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Gsmloc.service

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.12.99-9
- Rebuild for new 4.0 release.

