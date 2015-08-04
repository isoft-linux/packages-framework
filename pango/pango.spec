%global with_x11 1 

%define glib2_base_version 2.10.0
%define glib2_version %{glib2_base_version}-1
%define pkgconfig_version 0.12
%define freetype_version 2.1.3-3
%define fontconfig_version 2.0
%define cairo_version 1.1.2

Summary: System for layout and rendering of internationalized text
Name: pango
Version: 1.36.8
Release: 3
License: LGPL
Group: System Environment/Libraries
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

%if %with_x11
BuildRequires: libXft-devel
%endif

%description
Pango is a system for layout and rendering of internationalized text.


%package devel
Summary: System for layout and rendering of internationalized text.
Group: Development/Libraries
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

%prep
%setup -q -n pango-%{version}

%build
%configure \
    %if %with_x11
    --with-xft
    %else
    --without-xft
    %endif

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

# Deriving /etc/pango/$host location
# NOTE: Duplicated below
#
# autoconf changes linux to linux-gnu
case "%{_host}" in
  *linux) host="%{_host}-gnu"
  ;;
  *) host="%{_host}"
  ;;
esac

# autoconf uses powerpc not ppc
host=`echo $host | sed "s/^ppc/powerpc/"`

# Make sure that the host value that is passed to the compile 
# is the same as the host that we're using in the spec file
#
compile_host=`grep 'host_triplet =' pango/Makefile | sed "s/.* = //"`

if test "x$compile_host" != "x$host" ; then
  echo 1>&2 "Host mismatch: compile='$compile_host', spec file='$host'" && exit 1
fi

%makeinstall

# Remove files that should not be packaged
rm $RPM_BUILD_ROOT%{_libdir}/pango/*/modules/*.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la

# We need to have separate 32-bit and 64-bit pango-querymodules binaries
# for places where we have two copies of the Pango libraries installed.
# (we might have x86_64 and i686 packages on the same system, for example.)
case "$host" in
  alpha*|ia64*|powerpc64*|s390x*|x86_64*)
   mv $RPM_BUILD_ROOT%{_bindir}/pango-querymodules $RPM_BUILD_ROOT%{_bindir}/pango-querymodules-64
   ;;
  *)
   mv $RPM_BUILD_ROOT%{_bindir}/pango-querymodules $RPM_BUILD_ROOT%{_bindir}/pango-querymodules-32
   ;;
esac

rm $RPM_BUILD_ROOT%{_sysconfdir}/pango/pango.modules
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pango/$host
touch $RPM_BUILD_ROOT%{_sysconfdir}/pango/$host/pango.modules

#
# We need the substitution of $host so we use an external
# file list
#
echo %dir %{_sysconfdir}/pango/$host > modules.files
echo %ghost %{_sysconfdir}/pango/$host/pango.modules >> modules.files
rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

# Deriving /etc/pango/$host location
#
# autoconf changes linux to linux-gnu
case "%{_host}" in
  *linux) host="%{_host}-gnu"
  ;;
  *) host="%{_host}"
  ;;
esac

# autoconf uses powerpc not ppc
host=`echo $host | sed "s/^ppc/powerpc/"`

case "$host" in
  alpha*|ia64*|powerpc64*|s390x*|x86_64*)
   %{_bindir}/pango-querymodules-64 > %{_sysconfdir}/pango/pango.modules
   ;;
  *)
   %{_bindir}/pango-querymodules-32 > %{_sysconfdir}/pango/pango.modules
   ;;
esac

%postun -p /sbin/ldconfig

%files -f modules.files
%defattr(-, root, root)
%{_libdir}/libpango-1.0.so.*
%{_libdir}/libpangocairo-1.0.so.*
%{_libdir}/libpangoft2-1.0.so.*
%{_bindir}/pango-querymodules*
%{_libdir}/pango
%{_mandir}/man1/*
%{_sysconfdir}/pango
%{_libdir}/girepository-1.0/Pango-1.0.typelib
%{_libdir}/girepository-1.0/PangoCairo-1.0.typelib
%{_libdir}/girepository-1.0/PangoFT2-1.0.typelib

%if %with_x11
%{_libdir}/libpangoxft-1.0.so.*
%{_libdir}/girepository-1.0/PangoXft-1.0.typelib
%endif



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

%if %with_x11
%{_includedir}/pango-1.0/pango/pangoxft-render.h
%{_includedir}/pango-1.0/pango/pangoxft.h
%{_libdir}/libpangoxft-1.0.so
%{_libdir}/pkgconfig/pangoxft.pc
%{_datadir}/gir-1.0/PangoXft-1.0.gir
%endif

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

