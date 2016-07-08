%global _changelog_trimtime %(date +%s -d "1 year ago")
%global with_wayland 1 

Name:          clutter
Version:       1.26.0
Release:       1
Summary:       Open Source software library for creating rich graphical user interfaces

License:       LGPLv2+
URL:           http://www.clutter-project.org/
Source0:       http://download.gnome.org/sources/clutter/1.18/clutter-%{version}.tar.xz

BuildRequires: glib2-devel mesa-libGL-devel pkgconfig pango-devel
BuildRequires: cairo-gobject-devel gdk-pixbuf2-devel atk-devel
BuildRequires: cogl-devel >= 1.15.1
BuildRequires: gobject-introspection-devel >= 0.9.6
BuildRequires: gtk3-devel
BuildRequires: json-glib-devel >= 0.12.0
BuildRequires: libinput-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: libXi-devel
BuildRequires: libevdev-devel
BuildRequires: gettext-devel
%if %{with_wayland}
BuildRequires: libgudev-devel
BuildRequires: libwayland-client-devel
BuildRequires: libwayland-cursor-devel
BuildRequires: libwayland-server-devel
BuildRequires: libxkbcommon-devel
%endif

Requires:      gobject-introspection

# F18
Obsoletes:     clutter-gtk010 < 0.11.4-9
Obsoletes:     clutter-gtk010-devel < 0.11.4-9
Obsoletes:     clutter-sharp < 0-0.17
Obsoletes:     clutter-sharp-devel < 0-0.17
Obsoletes:     pyclutter < 1.3.2-13
Obsoletes:     pyclutter-devel < 1.3.2-13
Obsoletes:     pyclutter-gst < 1.0.0-10
Obsoletes:     pyclutter-gst-devel < 1.0.0-10
Obsoletes:     pyclutter-gtk < 0.10.0-14
Obsoletes:     pyclutter-gtk-devel < 0.10.0-14

%description
Clutter is an open source software library for creating fast,
visually rich graphical user interfaces. The most obvious example
of potential usage is in media center type applications.
We hope however it can be used for a lot more.

%package devel
Summary:       Clutter development environment
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
clutter

%package       doc
Summary:       Documentation for %{name}
Requires:      %{name} = %{version}-%{release}

%description   doc
Clutter is an open source software library for creating fast,
visually rich graphical user interfaces. The most obvious example
of potential usage is in media center type applications.
We hope however it can be used for a lot more.

This package contains documentation for clutter.

%prep
%setup -q
%build
%configure \
    --enable-xinput \
    --enable-gdk-backend \
%if %{with_wayland}
    --enable-egl-backend \
    --enable-evdev-input \
    --enable-wayland-backend \
    --enable-wayland-compositor \
%endif

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang clutter-1.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f clutter-1.0.lang
%doc COPYING NEWS README
%{_libdir}/*.so.0
%{_libdir}/*.so.0.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir

%files doc
%{_datadir}/gtk-doc/html/clutter

%changelog
* Fri Jul 08 2016 zhouyang <yang.zhou@i-soft.com.cn> - 1.26.0-1
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.24.2-2
- Rebuild for new 4.0 release.


* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 1.24.2
