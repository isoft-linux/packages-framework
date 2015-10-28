Name:network-manager-applet
Summary: GNOME applications for use with NetworkManager
Version: 1.0.4
Release: 4 
License: GPLv2+
URL: http://www.gnome.org/projects/NetworkManager/
Source: %{name}-%{version}.tar.xz
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: glib2 >= %{glib2_version}
Requires: NetworkManager
#for password dialog
Requires: libnm-gtk = %{version}-%{release}
Requires(pre): gtk3

BuildRequires: NetworkManager-glib-devel
BuildRequires: NetworkManager-devel
BuildRequires: gtk3-devel
BuildRequires: iso-codes-devel
BuildRequires: gobject-introspection-devel
BuildRequires: libnotify-devel
BuildRequires: libsecret-devel

%description
This package contains GNOME utilities and applications for use with
NetworkManager, including a panel applet for wireless networks.


%package -n libnm-gtk 
Summary: Libraries of NetworkManager GTK+ binding
Requires: gtk3
Requires: NetworkManager-glib
%description -n libnm-gtk
%{summary}

%package -n libnm-gtk-devel 
Summary: Libraries and headers of NetworkManager GTK+ binding.
Requires: libnm-gtk = %{version}-%{release}
Requires: gtk3-devel
Requires: NetworkManager-glib-devel

%description -n libnm-gtk-devel
%{summary}

%prep
%setup -q
%build
%configure \
    --disable-static \
	--without-bluetooth \
	--enable-more-warnings=yes \
	--with-gtkver=3 \
    --disable-maintainer-mode \
    --enable-introspection \
    --disable-migration
	make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT

# install NM
make install DESTDIR=$RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

echo "NoDisplay=true" >>$RPM_BUILD_ROOT/%{_datadir}/applications/nm-connection-editor.desktop
%find_lang nm-applet

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk3-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk3-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%post -n libnm-gtk -p /sbin/ldconfig
%postun -n libnm-gtk -p /sbin/ldconfig

%files -f nm-applet.lang
%defattr(-,root,root,0755)
%{_bindir}/nm-applet
%{_bindir}/nm-connection-editor
%{_datadir}/applications/*.desktop
%dir %{_datadir}/nm-applet/
%{_datadir}/nm-applet/*
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%dir %{_datadir}/gnome-vpn-properties
%{_mandir}/man1/*
%{_datadir}/GConf/gsettings/nm-applet.convert
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml

%files -n libnm-gtk
%defattr(-,root,root,0755)
%{_libdir}/libnm-gtk.so.*
%{_libdir}/girepository-?.?/NMGtk-1.0.typelib
%dir %{_datadir}/libnm-gtk
%{_datadir}/libnm-gtk/*

%files -n libnm-gtk-devel
%defattr(-,root,root,0755)
%{_libdir}/libnm-gtk.so
%{_libdir}/pkgconfig/libnm-gtk.pc
%dir %{_includedir}/libnm-gtk
%{_includedir}/libnm-gtk/*
%{_datadir}/gir-?.?/NMGtk-1.0.gir


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.4-4
- Rebuild for new 4.0 release.

