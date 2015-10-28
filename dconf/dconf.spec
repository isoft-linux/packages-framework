%define glib2_version 2.42.0

Name:           dconf
Version:        0.24.0
Release:        3 
Summary:        A configuration system

License:        LGPLv2+
URL:            http://live.gnome.org/dconf
#VCS:		git:git://git.gnome.org/dconf
Source0:        http://download.gnome.org/sources/dconf/0.4/dconf-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
Requires:       dbus
Requires:		glib2
BuildRequires:  gtk3-devel
BuildRequires:  libxml2-devel
BuildRequires:  gobject-introspection-devel
# Bootstrap requirements
BuildRequires:  autoconf automake libtool
BuildRequires:  gobject-introspection-devel >= 0.9.3
BuildRoot:  /var/tmp/%{name}-%{version}


%description
dconf is a low-level configuration system. Its main purpose is to provide a
backend to the GSettings API in GLib.

%package devel
Summary: Header files and libraries for dconf development
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}

%description devel
dconf development package. Contains files needed for doing software
development using dconf.

%prep
%setup -q

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
	--disable-static \
    --disable-man \
)
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig
gio-querymodules %{_libdir}/gio/modules ||:

%postun
/sbin/ldconfig
gio-querymodules %{_libdir}/gio/modules ||:


%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/gio/modules/libdconfsettings.so
%{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_bindir}/dconf
%{_libdir}/libdconf*.so.*
%{_datadir}/bash-completion/completions/dconf
#%{_mandir}/man1/dconf-service.1.gz
#%{_mandir}/man1/dconf.1.gz
#%{_mandir}/man7/dconf.7.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libdconf*.so
%{_libdir}/pkgconfig/*
# temporarily disable introspection until we have a new-enough goi
#%{_libdir}/girepository-1.0/dconf-0.3.typelib
%{_datadir}/gtk-doc/html/dconf
%{_datadir}/vala/vapi/dconf.deps
%{_datadir}/vala/vapi/dconf.vapi

#%files editor
#%defattr(-,root,root,-)
#%{_bindir}/dconf-editor
#%{_datadir}/dbus-1/services/ca.desrt.dconf-editor.service
#%{_datadir}/applications/ca.desrt.dconf-editor.desktop
#%{_datadir}/appdata/*.xml
#%{_datadir}/glib-*/schemas/*
#%{_datadir}/icons/HighContrast/*/apps/dconf-editor.png
#%{_datadir}/icons/hicolor/*/apps/dconf-editor.png
##%{_mandir}/man1/dconf-editor.1.gz
##%{_datadir}/gir-1.0/dconf-0.3.gir

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.24.0-3
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

