%define glib2_base_version 2.10.0
%define glib2_version %{glib2_base_version}-1
%define pkgconfig_version 0.12
%define freetype_version 2.1.3-3
%define fontconfig_version 2.0
%define cairo_version 1.1.2

Summary: System for layout and rendering of internationalized text
Name: pango
Version: 1.38.1
Release: 3
License: LGPL
Source: http://ftp.gnome.org/pub/gnome/sources/pango/1.8/pango-%{version}.tar.xz

URL: http://www.pango.org
BuildRoot: %{_tmppath}/pango-%{version}-root

# We need to prereq this so we can run pango-querymodules
Requires(pre): glib2 >= %{glib2_version}
Requires(pre): freetype >= %{freetype_version}
Requires: freetype >= %{freetype_version}
Requires: cairo >= %{cairo_version}
Requires: harfbuzz 
Requires: sed
BuildRequires: libtool >= 1.4.2-10
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: harfbuzz-devel
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: gobject-introspection

BuildRequires: libthai-devel

BuildRequires: libXft-devel

%description
Pango is a system for layout and rendering of internationalized text.


%package devel
Summary: System for layout and rendering of internationalized text.
Requires: pango = %{version}
Requires: glib2-devel >= %{glib2_version}
Requires: freetype-devel >= %{freetype_version}
Requires: fontconfig-devel >= %{fontconfig_version}
Requires: cairo-devel >= %{cairo_version}
Obsoletes: fribidi-gtkbeta-devel, pango-gtkbeta-devel

%description devel
The pango-devel package includes the static libraries, header files,
and developer docs for the pango package.

Install pango-devel if you want to develop programs which will use
pango.

%package tests
Summary: Tests for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%setup -q -n pango-%{version}

%build
# We try hard to not link to libstdc++
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
          --enable-doc-cross-references \
          --enable-installed-tests
)
make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT

%make_install

# Remove files that should not be packaged
rm $RPM_BUILD_ROOT%{_libdir}/*.la

PANGOXFT_SO=$RPM_BUILD_ROOT%{_libdir}/libpangoxft-1.0.so
if ! test -e $PANGOXFT_SO; then
        echo "$PANGOXFT_SO not found; did not build with Xft support?"
        ls $RPM_BUILD_ROOT%{_libdir}
        exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/libpango-1.0.so.*
%{_libdir}/libpangocairo-1.0.so.*
%{_libdir}/libpangoft2-1.0.so.*
%{_mandir}/man1/*
%{_libdir}/girepository-1.0/Pango-1.0.typelib
%{_libdir}/girepository-1.0/PangoCairo-1.0.typelib
%{_libdir}/girepository-1.0/PangoFT2-1.0.typelib

%{_libdir}/libpangoxft-1.0.so.*
%{_libdir}/girepository-1.0/PangoXft-1.0.typelib



%files devel
%defattr(-, root, root)
%{_libdir}/libpango-1.0.so
%{_libdir}/libpangocairo-1.0.so
%{_libdir}/libpangoft2-1.0.so
%dir %{_includedir}/pango-1.0
%{_includedir}/pango-1.0/pango/pango-attributes.h
%{_includedir}/pango-1.0/pango/pango-bidi-type.h
%{_includedir}/pango-1.0/pango/pango-break.h
%{_includedir}/pango-1.0/pango/pango-context.h
%{_includedir}/pango-1.0/pango/pango-coverage.h
%{_includedir}/pango-1.0/pango/pango-engine.h
%{_includedir}/pango-1.0/pango/pango-enum-types.h
%{_includedir}/pango-1.0/pango/pango-features.h
%{_includedir}/pango-1.0/pango/pango-font.h
%{_includedir}/pango-1.0/pango/pango-fontmap.h
%{_includedir}/pango-1.0/pango/pango-fontset.h
%{_includedir}/pango-1.0/pango/pango-glyph-item.h
%{_includedir}/pango-1.0/pango/pango-glyph.h
%{_includedir}/pango-1.0/pango/pango-gravity.h
%{_includedir}/pango-1.0/pango/pango-item.h
%{_includedir}/pango-1.0/pango/pango-language.h
%{_includedir}/pango-1.0/pango/pango-layout.h
%{_includedir}/pango-1.0/pango/pango-matrix.h
%{_includedir}/pango-1.0/pango/pango-modules.h
%{_includedir}/pango-1.0/pango/pango-ot.h
%{_includedir}/pango-1.0/pango/pango-renderer.h
%{_includedir}/pango-1.0/pango/pango-script.h
%{_includedir}/pango-1.0/pango/pango-tabs.h
%{_includedir}/pango-1.0/pango/pango-types.h
%{_includedir}/pango-1.0/pango/pango-utils.h
%{_includedir}/pango-1.0/pango/pango.h
%{_includedir}/pango-1.0/pango/pangocairo.h
%{_includedir}/pango-1.0/pango/pangofc-decoder.h
%{_includedir}/pango-1.0/pango/pangofc-font.h
%{_includedir}/pango-1.0/pango/pangofc-fontmap.h
%{_includedir}/pango-1.0/pango/pangoft2.h
%{_libdir}/pkgconfig/pango.pc
%{_libdir}/pkgconfig/pangocairo.pc
%{_libdir}/pkgconfig/pangoft2.pc
%{_bindir}/pango-view
%{_datadir}/gtk-doc/
%{_datadir}/gir-1.0/Pango-1.0.gir
%{_datadir}/gir-1.0/PangoCairo-1.0.gir
%{_datadir}/gir-1.0/PangoFT2-1.0.gir

%{_includedir}/pango-1.0/pango/pangoxft-render.h
%{_includedir}/pango-1.0/pango/pangoxft.h
%{_libdir}/libpangoxft-1.0.so
%{_libdir}/pkgconfig/pangoxft.pc
%{_datadir}/gir-1.0/PangoXft-1.0.gir

%files tests
%{_libexecdir}/installed-tests/%{name}
%{_datadir}/installed-tests

%changelog
* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 1.38.1

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

