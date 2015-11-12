Summary:   Library for AppStream metadata
Name:      appstream-glib
Version:   0.5.3
Release:   2 
License:   LGPLv2+
URL:       http://people.freedesktop.org/~hughsient/appstream-glib/
Source0:   http://people.freedesktop.org/~hughsient/appstream-glib/releases/%{name}-%{version}.tar.xz

BuildRequires: glib2-devel >= 2.45.8
BuildRequires: libtool
BuildRequires: docbook-utils
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel
BuildRequires: gperf
BuildRequires: libarchive-devel
BuildRequires: libsoup-devel >= 2.51.92
BuildRequires: gdk-pixbuf2-devel >= 2.31.5
BuildRequires: gtk3-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libgcab-devel

# for the builder component
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: pango-devel
BuildRequires: rpm-devel
BuildRequires: sqlite-devel
BuildRequires: gcab

# for the manpages
BuildRequires: libxslt
BuildRequires: docbook-style-xsl

Requires: gcab

Provides: libappstream-glib = %{version}-%{release}
%description
This library provides GObjects and helper methods to make it easy to read and
write AppStream metadata. It also provides a simple DOM implementation that
makes it easy to edit nodes and convert to and from the standardized XML
representation.


%package devel
Summary: GLib Libraries and headers for appstream-glib
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: libappstream-glib-devel = %{version}-%{release}

%description devel
GLib headers and libraries for appstream-glib.

%prep
%setup -q

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure \
        --enable-gtk-doc \
        --disable-static \
        --disable-silent-rules \
        --disable-dependency-tracking

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang appstream-glib

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f appstream-glib.lang
%doc README.md AUTHORS NEWS COPYING
%{_bindir}/appstream-util
%{_bindir}/appdata-validate
%{_bindir}/appstream-builder
%{_libdir}/libappstream-glib.so.*
%{_libdir}/libappstream-builder.so.*
%{_libdir}/girepository-1.0/*.typelib
%dir %{_libdir}/asb-plugins-2
%{_libdir}/asb-plugins-2/*.so
%{_datadir}/bash-completion/completions/appstream-builder
%{_datadir}/bash-completion/completions/appstream-util
%{_datadir}/installed-tests/appstream-glib/appdata-validate.test
%{_datadir}/installed-tests/appstream-glib/destdir-check.test
%{_mandir}/man1/appstream-builder.1.gz
%{_mandir}/man1/appstream-util.1.gz

%files devel
%{_libdir}/libappstream-glib.so
%{_libdir}/libappstream-builder.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libappstream-glib
%{_includedir}/libappstream-glib/*.h
%{_includedir}/libappstream-builder/*.h
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/*.gir

%{_datadir}/aclocal/appdata-xml.m4
%{_datadir}/aclocal/appstream-xml.m4

%changelog
* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 0.5.3-2
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.4.1-2
- Rebuild for new 4.0 release.

