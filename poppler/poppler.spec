%define dataversion 0.4.7

Summary: PDF rendering library
Name: poppler
Version: 0.37.0
Release: 2 
License: GPLv2 and Redistributable, no modification permitted
# the code is GPLv2
# the charmap data in /usr/share/poppler is redistributable
Group: Development/Libraries
URL:     http://poppler.freedesktop.org/
Source0: http://poppler.freedesktop.org/poppler-%{version}.tar.xz
Source1: http://poppler.freedesktop.org/poppler-data-%{dataversion}.tar.gz
Patch0: poppler-ObjStream.patch
Patch1: poppler-0.10.0-macros.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#!!!!important to support cups-filter
BuildRequires: openjpeg-devel
BuildRequires: cairo-devel
BuildRequires: gobject-introspection
BuildRequires: qt4-devel
BuildRequires: qt5-qtbase-devel

Obsoletes:poppler-data
%description
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

%package devel
Summary: Libraries and headers for poppler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

You should install the poppler-devel package if you would like to
compile applications based on poppler.

%package glib
Summary: Glib wrapper for poppler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description glib
%{summary}.

%package cpp
Summary: cpp STL library for poppler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description cpp 
%{summary}.

%package glib-devel
Summary: Development files for glib wrapper
Group: Development/Libraries
Requires: %{name}-glib = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: pkgconfig

%description glib-devel
%{summary}.

%package cpp-devel
Summary: CPP Development files for cpp stl library 
Group: Development/Libraries
Requires: %{name}-cpp = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: pkgconfig

%description cpp-devel
%{summary}.

%package qt4
Summary: Qt4 wrapper for poppler
Group:   System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%description qt4
%{summary}.

%package qt4-devel
Summary: Development files for Qt4 wrapper
Group:   Development/Libraries
Requires: %{name}-qt4 = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
%description qt4-devel
%{summary}.

%package qt5
Summary: Qt5 wrapper for poppler
Group:   System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%description qt5
%{summary}.

%package qt5-devel
Summary: Development files for Qt5 wrapper
Group:   Development/Libraries
Requires: %{name}-qt5 = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
%description qt5-devel 
%{summary}.

%package utils
Summary: Command line utilities for converting PDF files.
Group: Applications/Text
Requires: %{name} = %{version}-%{release}
Conflicts: xpdf <= 1:3.01-8
# There's an extras package that provides pdftohtml

Provides: pdftohtml
Obsoletes: pdftohtml

Provides: xpdf-utils = 1:3.01-27.fc7
Obsoletes: xpdf-utils <= 1:3.01-26.fc7

%description utils
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

This utils package installs a number of command line tools for
converting PDF files to a number of other formats.

%prep
%setup -c -q -a1

%build

pushd %{name}-%{version}
sed -i "s@-fno-check-new@@g" configure.ac
autoreconf -ivf
# despair
%configure \
  --disable-static \
  --enable-cairo-output \
  --enable-poppler-qt4 \
  --enable-poppler-qt5 \
  --enable-xpdf-headers \
  --disable-gtk-test
make %{?_smp_mflags}
popd

pushd poppler-data-%{dataversion}
cp COPYING COPYING-poppler-data
cp README README-poppler-data
popd

%install
rm -rf $RPM_BUILD_ROOT
make -C %{name}-%{version} DESTDIR=$RPM_BUILD_ROOT install
make -C %{name}-data-%{dataversion} \
	DESTDIR=$RPM_BUILD_ROOT datadir=%{_datadir} install

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.la

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc %{name}-%{version}/README
%doc %{name}-%{version}/COPYING
%doc poppler-data-%{dataversion}/README-poppler-data
%doc poppler-data-%{dataversion}/COPYING-poppler-data
%{_libdir}/libpoppler.so.*
%{_datadir}/poppler/

%files devel
%defattr(-,root,root,-)
#%exclude %{_libdir}/pkgconfig/poppler-qt.pc
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/pkgconfig/poppler-splash.pc
%{_datadir}/pkgconfig/poppler-data.pc
%{_libdir}/libpoppler.so
%{_includedir}/poppler/
%{_datadir}/gtk-doc/html/poppler

%files glib
%defattr(-,root,root,-)
%{_libdir}/libpoppler-glib.so.*
%{_libdir}/girepository-?.?/Poppler-*.typelib

%files glib-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/poppler-glib.pc
%{_libdir}/pkgconfig/poppler-cairo.pc
%{_libdir}/libpoppler-glib.so
%{_datadir}/gtk-doc/html/poppler
%{_datadir}/gir-?.?/Poppler-*.gir

%files qt4
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt4.so.*

%files qt4-devel
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt4.so
%{_libdir}/pkgconfig/poppler-qt4.pc
%{_includedir}/poppler/qt4/

%files qt5
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt5.so.*

%files qt5-devel
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt5.so
%{_libdir}/pkgconfig/poppler-qt5.pc
%{_includedir}/poppler/qt5/

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files cpp
%defattr(-,root,root,-)
%{_libdir}/libpoppler-cpp.so.*

%files cpp-devel
%defattr(-,root,root,-)
%{_libdir}/libpoppler-cpp.so
%{_libdir}/pkgconfig/poppler-cpp.pc


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

