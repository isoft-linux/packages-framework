Name:    librsvg2
Summary: An SVG library based on cairo
Version: 2.40.11
Release: 2

License:        LGPLv2+
Source:         http://download.gnome.org/sources/librsvg/2.32/librsvg-%{version}.tar.xz

Requires(post):   gdk-pixbuf2
Requires(postun): gdk-pixbuf2

BuildRequires:  libpng-devel
BuildRequires:  glib2-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  pango-devel
BuildRequires:  libxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  cairo-devel
BuildRequires:  libcroco-devel
BuildRequires:  gobject-introspection
Provides:       librsvg3 = %{name}.%{version}-%{release}
Obsoletes:      librsvg3 <= 2.26.3-3.fc14

%description
An SVG library based on cairo.


%package devel
Summary:        Libraries and include files for developing with librsvg
Requires:       %{name} = %{version}-%{release}
Requires:       gdk-pixbuf2-devel
Requires:       cairo-devel
Requires:       pango-devel
Requires:       libxml2-devel
Requires:       freetype-devel
Requires:       pkgconfig

Provides:       librsvg3-devel = %{name}.%{version}-%{release}
Obsoletes:      librsvg3-devel <= 2.26.3-3.fc14

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

%prep
%setup -q -n librsvg-%{version}

%build
GDK_PIXBUF_QUERYLOADERS=/usr/bin/gdk-pixbuf-query-loaders
export GDK_PIXBUF_QUERYLOADERS
# work around an ordering problem in configure
enable_pixbuf_loader=yes
export enable_pixbuf_loader

%configure --with-svgz \
        --disable-gtk-doc \
        --disable-gtk-theme
make %{?_smp_mflags} CC=cc

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/svg-viewer.svg

%post
/sbin/ldconfig
gdk-pixbuf-query-loaders --update-cache || :

%postun
/sbin/ldconfig
gdk-pixbuf-query-loaders --update-cache || :


%files
%defattr(-, root, root)
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_libdir}/librsvg-2.so.*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-svg.so
#%{_bindir}/rsvg
#%{_bindir}/rsvg-view*
%{_bindir}/rsvg-convert
%{_mandir}/man1/*
%{_libdir}/girepository-?.?/Rsvg-2.0.typelib

%files devel
%defattr(-, root, root)
%{_libdir}/librsvg-2.so
%{_includedir}/librsvg-2.0
%{_libdir}/pkgconfig/librsvg-2.0.pc
%{_datadir}/gir-?.?/Rsvg-2.0.gir
%doc %{_datadir}/gtk-doc/html/rsvg-2.0


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.40.11-2
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 2.40.11 

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

