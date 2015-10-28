%define glib2_version 2.13.6
%define gtk2_version 2.12.0

%define po_package gtksourceview-2.0

Summary: A library for viewing source files
Name: gtksourceview2
Version: 2.10.5
Release: 21%{?dist}
License: LGPLv2+ and GPLv2+
# the library itself is LGPL, some .lang files are GPL
URL: http://gtksourceview.sourceforge.net/
#VCS: git:git://git.gnome.org/gtksourceview
Source0: http://download.gnome.org/sources/gtksourceview/2.11/gtksourceview-%{version}.tar.bz2
BuildRequires: libxml2-devel
BuildRequires: GConf2-devel
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: intltool >= 0.35
BuildRequires: gettext
BuildRequires: gobject-introspection-devel

%description
GtkSourceView is a text widget that extends the standard GTK+
GtkTextView widget. It improves GtkTextView by implementing
syntax highlighting and other features typical of a source code editor.

This package contains version 2 of GtkSourceView. The older version
1 is contains in the gtksourceview package.

%package devel
Summary: Files to compile applications that use gtksourceview2
Requires: %{name} = %{version}-%{release}
Requires: gtk2-devel >= %{gtk2_version}
Requires: libxml2-devel

%description devel
gtksourceview2-devel contains the files required to compile
applications which use GtkSourceView 2.x.

%prep
%setup -q -n gtksourceview-%{version}

%build
%configure --disable-gtk-doc --disable-static --disable-deprecations

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-2.0/language-specs/check.sh
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-2.0/language-specs/convert.py

%find_lang %{po_package}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS MAINTAINERS
%{_datadir}/gtksourceview-2.0
%{_libdir}/*.so.*
#%{_libdir}/girepository-1.0/GtkSource-2.0.typelib

%files devel
%defattr(-,root,root,-)
%{_includedir}/gtksourceview-2.0
%{_datadir}/gtk-doc/html/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
#%{_datadir}/gir-1.0/GtkSource-2.0.gir

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.10.5-21
- Rebuild for new 4.0 release.

