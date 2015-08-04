Name: libcanberra
Version: 0.30
Release: 3
Summary: Portable Sound Event Library
Group: System Environment/Libraries
Source0: http://0pointer.de/lennart/projects/libcanberra/libcanberra-%{version}.tar.xz

License: LGPLv2+
Url: http://git.0pointer.de/?p=libcanberra.git;a=summary
BuildRequires: gtk2-devel
BuildRequires: gtk3-devel
BuildRequires: alsa-lib-devel
BuildRequires: libvorbis-devel
BuildRequires: gtk-doc
BuildRequires: pulseaudio-libs-devel >= 0.9.15
BuildRequires: gstreamer-devel
BuildRequires: gettext-devel
BuildRequires: systemd-devel
Requires: sound-theme-freedesktop
Requires: pulseaudio-libs >= 0.9.15
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package gtk2
Summary: Gtk+ 2.x Bindings for libcanberra
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description gtk2
Gtk+ 2.x bindings for libcanberra

%package gtk2-devel
Summary: Gtk+ 2.x Bindings for libcanberra
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description gtk2-devel
Gtk+ 2.x bindings for libcanberra


%package gtk3
Summary: Gtk+ 3.x Bindings for libcanberra
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description gtk3
Gtk+ 3.x bindings for libcanberra

%package gtk3-devel
Summary: Gtk+ 3.x Bindings for libcanberra
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description gtk3-devel
Gtk+ 3.x bindings for libcanberra

%package devel
Summary: Development Files for libcanberra Client Development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtk2-devel

%description devel
Development Files for libcanberra Client Development

%post
/sbin/ldconfig
%systemd_post canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service

%preun
%systemd_preun canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service

%postun
/sbin/ldconfig
%systemd_postun

%post gtk2 -p /sbin/ldconfig
%postun gtk2 -p /sbin/ldconfig

%post gtk3 -p /sbin/ldconfig
%postun gtk3 -p /sbin/ldconfig

%prep
%setup -q

%build
%configure \
    --disable-static \
    --enable-pulse \
    --enable-alsa \
    --enable-null \
    --disable-oss \
    --with-builtin=dso \
    --with-systemdsystemunitdir=/usr/lib/systemd/system
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT \( -name *.a -o -name *.la \) -exec rm {} \;
rm $RPM_BUILD_ROOT%{_docdir}/libcanberra/README
rpmclean

%files
%defattr(-,root,root)
%doc README LGPL
%{_libdir}/libcanberra.so.*
%dir %{_libdir}/libcanberra-%{version}
%{_libdir}/libcanberra-%{version}/libcanberra-alsa.so
%{_libdir}/libcanberra-%{version}/libcanberra-pulse.so
%{_libdir}/libcanberra-%{version}/libcanberra-null.so
%{_libdir}/libcanberra-%{version}/libcanberra-multi.so
%{_libdir}/libcanberra-%{version}/libcanberra-gstreamer.so
%{_prefix}/lib/systemd/system/canberra-system-bootup.service
%{_prefix}/lib/systemd/system/canberra-system-shutdown-reboot.service
%{_prefix}/lib/systemd/system/canberra-system-shutdown.service
%{_bindir}/canberra-boot

%files gtk2
%defattr(-,root,root)
%{_libdir}/libcanberra-gtk.so.*
%{_libdir}/gtk-2.0/modules/libcanberra-gtk-module.so

%files gtk3
%defattr(-,root,root)
%{_libdir}/libcanberra-gtk3.so.*
%{_libdir}/gtk-3.0/modules/libcanberra-gtk3-module.so
%{_libdir}/gtk-3.0/modules/libcanberra-gtk-module.so
%{_bindir}/canberra-gtk-play
%{_datadir}/gnome/autostart/libcanberra-login-sound.desktop
%{_datadir}/gnome/shutdown/libcanberra-logout-sound.sh
%{_datadir}/gdm/autostart/LoginWindow/libcanberra-ready-sound.desktop
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/canberra-gtk-module.desktop

%files gtk2-devel
%{_libdir}/libcanberra-gtk.so
%{_libdir}/pkgconfig/libcanberra-gtk.pc

%files gtk3-devel
%{_libdir}/libcanberra-gtk3.so
%{_libdir}/pkgconfig/libcanberra-gtk3.pc

#some files is shared between gtk2/gtk3, put them all in devel package
#let gtk2-devel/gtk3-devel require it.
%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc
%{_includedir}/canberra.h
%{_includedir}/canberra-gtk.h
%{_libdir}/libcanberra.so
%{_libdir}/pkgconfig/libcanberra.pc
%{_datadir}/vala/vapi/libcanberra.vapi
%{_datadir}/vala/vapi/libcanberra-gtk.vapi

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

