%global with_x11 1

%define glib2_base_version 2.28.0
%define glib2_version %{glib2_base_version}-1
%define pango_base_version 1.28.3
%define pango_version %{pango_base_version}-1
%define atk_base_version 1.32.0
%define atk_version %{atk_base_version}-1
%define cairo_base_version 1.10.2
%define cairo_version %{cairo_base_version}-1

%define gobject_introspection_base_version 0.10.1 
%define gobject_introspection_version %{gobject_introspection_base_version}-1
%define libpng_version 2:1.2.2-16

%define base_version 3.18.2
%define bin_version 3.0.0

Summary: The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name: gtk3
Version: %{base_version}
Release: 18
License: LGPLv2+
Source: http://download.gnome.org/sources/gtk+/3.0/gtk+-%{version}.tar.xz
#By Cjacker
#gtk default to wayland backend now.
#It's bad since we still use "Xorg" as our default Display Server.
#here is a hack, if get WAYLAND_DISPLAY env, then prefer wayland backend,
#else prefer x11 backend.
#and GDK_BACKEND settings still works.
Patch0: gtk-temp-fix-backend-selection.patch

BuildRequires: atk-devel >= %{atk_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires: libtiff-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel >= %{libpng_version}
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: gettext
BuildRequires: cups-devel
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: wayland-devel
BuildRequires: colord-devel

%if %with_x11
BuildRequires: at-spi2-core-devel
BuildRequires: at-spi2-atk-devel
%endif

URL: http://www.gtk.org

# required for icon themes apis to work

# We need to prereq these so we can run gtk-query-immodules-2.0
Requires(post): glib2 >= %{glib2_version}
Requires(post): atk >= %{atk_version}
Requires(post): pango >= %{pango_version}
# and these for gdk-pixbuf-query-loaders
Requires(post): libtiff >= 3.6.1
Requires: gail3


%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

%package devel
Summary: Development tools for GTK+ applications
Requires: gtk3 = %{version}-%{release}
Requires: pango-devel >= %{pango_version}
Requires: atk-devel >= %{atk_version}
Requires: glib2-devel >= %{glib2_version}
Requires: cairo-devel >= %{cairo_version}
Requires: libpng-devel
Requires: pkgconfig
Requires: gail3-devel
Obsoletes: gtk+-gtkbeta-devel

%description devel
The gtk+-devel package contains the header files and developer
docs for the GTK+ widget toolkit.  


%package -n gail3
Summary: Accessibility implementation for GTK+ and GNOME libraries
BuildRequires: libtool automake autoconf gettext
BuildRequires: atk-devel >= %{atk_version}

%description -n gail3
GAIL implements the abstract interfaces found in ATK for GTK+ and
GNOME libraries, enabling accessibility technologies such as at-spi to
access those GUIs.

%package -n gail3-devel
Summary: Files to compile applications that use GAIL
Requires: gail3
Requires: gtk3-devel >= %{gtk3_version}
Requires: atk-devel >= %{atk_version}
Requires: pkgconfig
Requires: gtk3-devel
%description -n gail3-devel
gail-devel contains the files required to compile applications against the GAIL libraries.


%prep
%setup -q -n gtk+-%{version}
%patch0 -p1

%build
export CC=cc
export CXX=c++
%configure \
    --enable-introspection=auto \
    --enable-broadway-backend \
    --enable-wayland-backend \
%if %with_x11
    --enable-x11-backend \
    --with-xinput \
%else
    --disable-x11-backend \
    --without-xinput \
%endif
    --enable-colord=yes \
    --disable-cloudprint

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT        \
             RUN_QUERY_IMMODULES_TEST=false \
             RUN_QUERY_LOADER_TEST=false 

%find_lang gtk30
%find_lang gtk30-properties

cat gtk30.lang gtk30-properties.lang > all.lang

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0
#
# Make cleaned-up versions of tutorials, examples, and faq for installation
#
#mkdir -p tmpdocs
#cp -aR docs/tutorial/html tmpdocs/tutorial
#cp -aR docs/faq/html tmpdocs/faq
#
#for dir in examples/* ; do
#  if [ -d $dir ] ; then
#     mkdir -p tmpdocs/$dir
#     for file in $dir/* ; do
#       install -m 0644 $file tmpdocs/$dir
#     done
#  fi
#done

#
# Install wrappers for the binaries
#
# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/*/*.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*/*/*.la

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0/
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/modules

#
# We need the substitution of $host so we use an external
# file list
#
echo %dir %{_sysconfdir}/gtk-3.0/ >> all.lang

mv $RPM_BUILD_ROOT%{_bindir}/gtk-update-icon-cache $RPM_BUILD_ROOT%{_bindir}/gtk3-update-icon-cache
mv $RPM_BUILD_ROOT%{_mandir}/man1/gtk-update-icon-cache.1 $RPM_BUILD_ROOT%{_mandir}/man1/gtk3-update-icon-cache.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/usr/bin/gtk-query-immodules-3.0 >%{_libdir}/gtk-3.0/3.0.0/immodules.cache || :
glib-compile-schemas /usr/share/glib-2.0/schemas >/dev/null 2>&1 ||:
%postun
glib-compile-schemas /usr/share/glib-2.0/schemas >/dev/null 2>&1 ||:

%files -f all.lang
%defattr(-, root, root)

%doc AUTHORS COPYING NEWS README
%{_bindir}/gtk-query-immodules-3.0*
#%{_bindir}/gtk-update-icon-cache
%{_bindir}/gtk3-update-icon-cache
%{_bindir}/gtk3-icon-browser
%{_bindir}/gtk-encode-symbolic-svg
%{_bindir}/gtk-launch
%{_libdir}/libgtk-*.so.*
%{_libdir}/libgdk-*.so.*
%dir %{_libdir}/gtk-3.0
%{_libdir}/gtk-3.0/%{bin_version}
%dir %{_libdir}/gtk-3.0/modules
%{_datadir}/themes/*
%dir %{_sysconfdir}/gtk-3.0
%{_sysconfdir}/gtk-3.0/im-multipress.conf
%{_datadir}/glib-*/schemas/*.xml
%{_mandir}/*
%{_libdir}/girepository-?.?/*.typelib
%{_bindir}/broadwayd
%{_datadir}/applications/gtk3-icon-browser.desktop

%files devel
%defattr(-, root, root)
%{_bindir}/gtk-builder-tool
%{_libdir}/lib*.so
%{_datadir}/gtk-doc/html/gtk3
%{_datadir}/gtk-doc/html/gdk3
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/gdk*
%{_libdir}/pkgconfig/gtk*
%{_bindir}/gtk3-demo
%{_bindir}/gtk3-demo-application
%{_bindir}/gtk3-widget-factory
%{_datadir}/applications/gtk3-demo.desktop
%{_datadir}/applications/gtk3-widget-factory.desktop
%{_datadir}/icons/hicolor/*/apps/*

%{_datadir}/gtk-3.0
%{_datadir}/gir-?.?/*.gir

%exclude %{_libdir}/libgail*.so
%exclude %{_libdir}/pkgconfig/gail*.pc
%exclude %{_datadir}/gtk-doc/html/gail-libgail-util3
%exclude %{_includedir}/gail*


%files -n gail3
%defattr(-, root, root)
%{_libdir}/libgail*.so.*
#%{_libdir}/gtk-3.0/modules/*

%files -n gail3-devel
%defattr(-, root, root)
%{_libdir}/libgail*.so
%{_libdir}/pkgconfig/gail*.pc
%{_datadir}/gtk-doc/html/gail-libgail-util3
%{_includedir}/gail*

%changelog
* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 3.18.2

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Fri Aug 21 2015 Cjacker <cjacker@foxmail.com>
- update to 3.16.6
- add patch0 to fix backend selection, now gtk default to wayland, it's bad for us.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

