# Note that this is NOT a relocatable package

%define glib2_base_version 2.13.7
%define glib2_version %{glib2_base_version}-1
%define pango_base_version 1.15.3
%define pango_version %{pango_base_version}-1
%define atk_base_version 1.9.0
%define atk_version %{atk_base_version}-1
%define cairo_base_version 1.2.0
%define cairo_version %{cairo_base_version}-1
%define libpng_version 2:1.2.2-16

%define base_version 2.24.30
%define bin_version 2.10.0

Summary: The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name: gtk2
Version: %{base_version}
Release: 2
License: LGPLv2+
Source: http://download.gnome.org/sources/gtk+/2.11/gtk+-%{version}.tar.xz
Source1: gtk+2.0_2.24.24-0ubuntu1.debian.tar.xz
Source2: gtkrc

# Biarch changes
Patch0: gtk-fix-gcc-warning.patch

BuildRequires: atk-devel >= %{atk_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libtiff-devel
BuildRequires: libjpeg-devel
BuildRequires: libXi-devel
BuildRequires: libpng-devel >= %{libpng_version}
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: cups-devel
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXcursor-devel
BuildRequires: libXfixes-devel
BuildRequires: libXinerama-devel
BuildRequires: gdk-pixbuf2-devel 
BuildRequires: pkgconfig(gobject-introspection-1.0)
# for patch 2
#BuildRequires: gamin-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes: gtk+-gtkbeta
Obsoletes: Inti

# Conflicts with packages containing theme engines
# built against the 2.4.0 ABI
Conflicts: gtk2-engines < 2.7.4-7
Conflicts: libgnomeui < 2.15.1cvs20060505-2

URL: http://www.gtk.org

# required for icon themes apis to work

# We need to prereq these so we can run gtk-query-immodules-2.0
Requires(post): glib2 >= %{glib2_version}
Requires(post): atk >= %{atk_version}
Requires(post): pango >= %{pango_version}
# and these for gdk-pixbuf-query-loaders
Requires(post): libtiff >= 3.6.1
Requires: gail

%define _unpackaged_files_terminate_build      1
%define _missing_doc_files_terminate_build     1


%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

%package devel
Summary: Development tools for GTK+ applications
Requires: gtk2 = %{version}-%{release}
Requires: pango-devel >= %{pango_version}
Requires: atk-devel >= %{atk_version}
Requires: glib2-devel >= %{glib2_version}
Requires: cairo-devel >= %{cairo_version}
Requires: libX11-devel, libXcursor-devel, libXinerama-devel
Requires: libXext-devel, libXi-devel, libXrandr-devel
Requires: libXfixes-devel
Requires: libpng-devel
Requires: pkgconfig
Requires: gail-devel
Obsoletes: gtk+-gtkbeta-devel

%description devel
The gtk+-devel package contains the header files and developer
docs for the GTK+ widget toolkit.  


%package -n gail
Summary: Accessibility implementation for GTK+ and GNOME libraries
BuildRequires: libtool automake autoconf gettext
BuildRequires: atk-devel >= %{atk_version}

%description -n gail
GAIL implements the abstract interfaces found in ATK for GTK+ and
GNOME libraries, enabling accessibility technologies such as at-spi to
access those GUIs.

%package -n gail-devel
Summary: Files to compile applications that use GAIL
Requires: gail
Requires: gtk2-devel >= %{gtk2_version}
Requires: atk-devel >= %{atk_version}
Requires: pkgconfig
Requires: gtk2-devel
%description -n gail-devel
gail-devel contains the files required to compile applications against the GAIL libraries.


%prep
%setup -q -n gtk+-%{version} -a1

%patch0 -p1
cat debian/patches/015_default-fallback-icon-theme.patch|patch -p1
cat debian/patches/042_treeview_single-focus.patch |patch -p1
cat debian/patches/061_use_pdf_as_default_printing_standard.patch |patch -p1
cat debian/patches/060_ignore-random-icons.patch|patch -p1
cat debian/patches/062_dnd_menubar.patch|patch -p1
cat debian/patches/063_treeview_almost_fixed.patch|patch -p1
cat debian/patches/071_no_offscreen_widgets_grabbing.patch|patch -p1
cat debian/patches/093_gtk3_gtkimage_fallbacks_use.patch|patch -p1
cat debian/patches/096_git_gtkprintsettings.patch|patch -p1
cat debian/patches/097_statusicon_image_fallback.patch|patch -p1
cat debian/patches/099_printer_filename_fix.patch|patch -p1
cat debian/patches/100_overlay_scrollbar_loading.patch|patch -p1
cat debian/patches/backport_search_printer_location.patch|patch -p1
cat debian/patches/gtk-shell-shows-menubar.patch|patch -p1
cat debian/patches/print-dialog-show-options-of-remote-dnssd-printers.patch|patch -p1

%build
#autoreconf -i -f
if ! pkg-config --exists pangoxft ; then
        echo "No pangoxft.pc!"
        exit 1
fi

%configure \
  --with-xinput \
  --disable-gtk-doc \
  --disable-rebuilds \
  --with-included-loaders=png

## smp_mflags doesn't work for now due to gdk-pixbuf.loaders, may be fixed 
## past gtk 2.1.2
make %{?_smp_mflags}
# turn off for now, since floatingtest needs a display
#make check

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT        \
             RUN_QUERY_IMMODULES_TEST=false \
             RUN_QUERY_LOADER_TEST=false 
install -Dm 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/gtk-2.0/gtkrc

%find_lang gtk20
%find_lang gtk20-properties

cat gtk20.lang gtk20-properties.lang > all.lang

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0
#
# Make cleaned-up versions of tutorials, examples, and faq for installation
#
mkdir -p tmpdocs
cp -aR docs/tutorial/html tmpdocs/tutorial
cp -aR docs/faq/html tmpdocs/faq

for dir in examples/* ; do
  if [ -d $dir ] ; then
     mkdir -p tmpdocs/$dir
     for file in $dir/* ; do
       install -m 0644 $file tmpdocs/$dir
     done
  fi
done

#
# Install wrappers for the binaries
#
# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{bin_version}/*/*.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*/*/*.la

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/
touch $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gtk.immodules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules

#
# We need the substitution of $host so we use an external
# file list
#
echo %dir %{_sysconfdir}/gtk-2.0/ >> all.lang
echo %ghost %{_sysconfdir}/gtk-2.0//gtk.immodules >> all.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/usr/bin/gtk-query-immodules-2.0 >/etc/gtk-2.0/gtk.immodules || :
/usr/bin/gtk-query-immodules-2.0 --update-cache || :
%postun
/sbin/ldconfig

%files -f all.lang
%defattr(-, root, root)

%doc AUTHORS COPYING NEWS README
%{_bindir}/gtk-query-immodules-2.0*
%{_bindir}/gtk-update-icon-cache
%{_libdir}/libgtk-x11-2.0.so.*
%{_libdir}/libgdk-x11-2.0.so.*
%dir %{_libdir}/gtk-2.0
%{_libdir}/gtk-2.0/%{bin_version}
%dir %{_libdir}/gtk-2.0/modules
%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_datadir}/themes/Raleigh
%dir %{_sysconfdir}/gtk-2.0
%{_sysconfdir}/gtk-2.0/im-multipress.conf
%{_sysconfdir}/gtk-2.0/gtkrc
%{_libdir}/girepository-?.?/*.typelib

%files devel
%defattr(-, root, root)
%{_libdir}/lib*.so
%{_libdir}/gtk-2.0/include
%{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_datadir}/aclocal/*
%{_bindir}/gtk-builder-convert
%{_libdir}/pkgconfig/*
%doc tmpdocs/tutorial
%doc tmpdocs/faq
%doc tmpdocs/examples
%{_bindir}/gtk-demo
%{_datadir}/gtk-2.0
%{_datadir}/gir-?.?/*.gir

%exclude %{_libdir}/libgail*.so
%exclude %{_libdir}/pkgconfig/gail.pc
%exclude %{_datadir}/gtk-doc/html/gail-libgail-util
%exclude %{_includedir}/gail*


%files -n gail
%defattr(-, root, root)
%{_libdir}/libgail*.so.*
%{_libdir}/gtk-2.0/modules/*

%files -n gail-devel
%defattr(-, root, root)
%{_libdir}/libgail*.so
%{_libdir}/pkgconfig/gail.pc
%{_datadir}/gtk-doc/html/gail-libgail-util
%{_includedir}/gail*
%changelog
* Mon Apr 11 2016 sulit <sulitsrc@gmail.com> - 2.24.30-2
- update to release 2.24.30

* Thu Dec 03 2015 xiaotian.wu@i-soft.com.cn - 2.24.28-19
- Add gir build request to fix build on koji.

* Thu Dec 03 2015 xiaotian.wu@i-soft.com.cn - 2.24.28-18
- Add gtkrc for default gtk theme and icon theme.

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.24.28-17
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

