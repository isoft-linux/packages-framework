### Abstract ###

Name: pygobject2
Version: 2.28.6
Release: 9
License: LGPLv2+
Group: Development/Languages
Summary: Python 2 bindings for GObject 
URL: http://www.pygtk.org/
Source: http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-%{version}.tar.bz2

### Patches ###
# Fix this warning on startup:
#   ** WARNING **: Trying to register gtype 'GMountMountFlags' as enum when
#   in fact it is of type 'GFlags'
# using upstream patch (rhbz#790053)
Patch1: fix-gio-flags.patch
Patch2: 0001-Fix-set_qdata-warning-on-accessing-NULL-gobject-prop.patch

### Build Dependencies ###

BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(cairo-gobject)

# Bootstrap requirements
BuildRequires: automake autoconf libtool

%description
The %{name} package provides a convenient wrapper for the GObject library
for use in Python programs.

%package codegen
Summary: The code generation program for PyGObject
Group: Development/Languages

%description codegen
The package contains the C code generation program for PyGObject.

%package devel
Summary: Development files for building add-on libraries
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: %{name}-codegen = %{version}-%{release}
Requires: %{name}-doc = %{version}-%{release}
Requires: glib2-devel
Requires: python-devel
Requires: pkgconfig

%description devel
This package contains files required to build wrappers for %{name}-based
libraries such as pygtk2.

%package doc
Summary: Documentation files for %{name}
Group: Development/Languages

%description doc
This package contains documentation files for %{name}.

%prep
%setup -q -n pygobject-%{version}
%patch1 -p1
%patch2 -p1

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
PYTHON=/usr/bin/python
export PYTHON
export LDFLAGS="`python-config --ldflags`"
%configure --disable-introspection
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -delete
find $RPM_BUILD_ROOT -name '*.a' -delete

rm examples/Makefile*

rpmclean

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644, root, root, 755)
%doc AUTHORS NEWS README
%doc examples

%{_libdir}/libpyglib-2.0-python.so*
%dir %{python_sitearch}/gtk-2.0
%dir %{python_sitearch}/gobject
%dir %{python_sitearch}/glib

%{python_sitearch}/gtk-2.0/*
%{python_sitearch}/pygtk.*
%{python_sitearch}/gobject/*
%{python_sitearch}/glib/*

%files codegen
%defattr(755, root, root, 755)
%{_bindir}/pygobject-codegen-2.0
%defattr(644, root, root, 755)
%dir %{_datadir}/pygobject/2.0
%{_datadir}/pygobject/2.0/codegen

%files devel
%defattr(644, root, root, 755)
%dir %{_datadir}/pygobject
%dir %{_includedir}/pygtk-2.0
%{_datadir}/pygobject/2.0/defs
%{_includedir}/pygtk-2.0/pyglib.h
%{_includedir}/pygtk-2.0/pygobject.h
%{_libdir}/pkgconfig/pygobject-2.0.pc

%files doc
%defattr(644, root, root, 755)
%{_datadir}/gtk-doc/html/pygobject
%{_datadir}/pygobject/xsl

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

