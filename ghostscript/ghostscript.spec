%define version 9.14
%{expand: %%define build_with_freetype %{?_with_freetype:1}%{!?_with_freetype:0}}

Summary: A PostScript interpreter and renderer
Name: ghostscript
Version: 9.14 
Release: 2 
License: AGPLv3+
URL: http://www.ghostscript.com/
Source0: %{name}-%{version}.tar.gz

Source2: CIDFnmap
Source4: cidfmap

Patch2: ghostscript-scripts.patch
Patch3: ghostscript-noopt.patch
Patch4: ghostscript-runlibfileifexists.patch
Patch5: ghostscript-icc-missing-check.patch
Patch6: ghostscript-Fontmap.local.patch
Patch7: ghostscript-iccprofiles-initdir.patch
Patch8: ghostscript-gdevcups-debug-uninit.patch
Patch9: ghostscript-wrf-snprintf.patch
Patch10: ghostscript-gs694154.patch
Patch11: ghostscript-sys-zlib.patch
Patch12: ghostscript-crash.patch


Requires: poppler
BuildRequires: xz
BuildRequires: libjpeg-devel
BuildRequires: zlib-devel, libpng-devel, unzip
BuildRequires: glib2-devel
# Omni requires libxml
BuildRequires: libxml2-devel
BuildRequires: libtiff-devel
BuildRequires: cups-devel >= 1.1.13
BuildRequires: libtool
BuildRequires: jasper-devel
BuildRequires: dbus-devel
BuildRequires: poppler-devel
BuildRequires: openjpeg-devel
BuildRequires: freetype-devel

%description
Ghostscript is a set of software that provides a PostScript
interpreter, a set of C procedures (the Ghostscript library, which
implements the graphics capabilities in the PostScript language) and
an interpreter for Portable Document Format (PDF) files. Ghostscript
translates PostScript code into many common, bitmapped formats, like
those understood by your printer or screen. Ghostscript is normally
used to display PostScript files and to print PostScript files to
non-PostScript printers.

If you need to display PostScript files or print them to
non-PostScript printers, you should install ghostscript.

%package devel
Summary: Files for developing applications that use ghostscript
Requires: %{name} = %{version}-%{release}

%description devel
The header files for developing applications that use ghostscript.

%package doc
Summary: Documentation for ghostscript
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
The documentation files that come with ghostscript.

%package gsx
Summary: A PostScript interpreter and renderer
Requires: %{name} = %{version}-%{release}

%description gsx 
A PostScript interpreter and renderer

%prep
%setup -q -n %{name}-%{version}
rm -rf expat tiff freetype jasper jpeg libpng zlib cups/libs

%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
EXTRACFLAGS="-fno-strict-aliasing"

FONTPATH=
for path in \
        %{_datadir}/fonts/default/%{name} \
        %{_datadir}/fonts/default/Type1 \
        %{_datadir}/fonts/default/amspsfnt/pfb \
        %{_datadir}/fonts/default/cmpsfont/pfb \
        %{_datadir}/fonts \
        %{_datadir}/%{name}/conf.d \
        %{_sysconfdir}/%{name} \
        %{_sysconfdir}/%{name}/%{version} \
        %{_datadir}/poppler/cMap/*
do
  FONTPATH="$FONTPATH${FONTPATH:+:}$path"
done

autoconf --force
%configure \
    CFLAGS="$CFLAGS $EXTRACFLAGS" \
    --with-ijs \
    --enable-dynamic \
    --with-fontpath="$FONTPATH" \
    --with-drivers=ALL \
    --disable-compile-inits \
    --with-system-libtiff \
    --without-luratech \
    --without-omni \
    --with-install-cups \
    --disable-gtk \
    --enable-fontconfig \
    --enable-freetype

# Build IJS
cd ijs
./autogen.sh
%configure --enable-shared --disable-static
make
cd ..

make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT \
     CUPSSERVERROOT=$RPM_BUILD_ROOT`cups-config --serverroot` \
     CUPSSERVERBIN=$RPM_BUILD_ROOT`cups-config --serverbin` \
     CUPSDATA=$RPM_BUILD_ROOT`cups-config --datadir` \
     install install-so
    
mv -f $RPM_BUILD_ROOT%{_bindir}/gsc $RPM_BUILD_ROOT%{_bindir}/gs

cd ijs
%makeinstall
cd ..

echo ".so man1/gs.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/ghostscript.1
ln -sf gs $RPM_BUILD_ROOT%{_bindir}/ghostscript

# Rename an original cidfmap to cidfmap.GS
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/Resource/Init/cidfmap{,.GS}
# Install our own cidfmap to allow the separated
# cidfmap which the font packages own.
install -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/Resource/Init/CIDFnmap
install -m0644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/Resource/Init/cidfmap

# Don't ship ijs example client or server
rm -f $RPM_BUILD_ROOT%{_bindir}/ijs_{client,server}_example

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{version}
touch $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{version}/Fontmap.local
touch $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{version}/cidfmap.local
touch $RPM_BUILD_ROOT%{_sysconfdir}/ghostscript/%{version}/CIDFnmap.local

# remove unwanted localized man-pages
rm -rf $RPM_BUILD_ROOT%{_mandir}/[^man1]*

# Don't ship fixmswrd.pl as it pulls in perl (bug #463948).
rm -f $RPM_BUILD_ROOT%{_bindir}/fixmswrd.pl

# Don't ship CMaps (instead poppler-data paths are in search path).
rm -f $RPM_BUILD_ROOT%{_datadir}/ghostscript/%{version}/Resource/CMap/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/ghostscript
%dir %{_sysconfdir}/ghostscript/%{version}
%config(noreplace) %{_sysconfdir}/ghostscript/%{version}/*
%dir %{_datadir}/ghostscript
%{_datadir}/ghostscript/*
%{_libdir}/libgs.so.*
%{_libdir}/libijs-*.so*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/%{version}/X11.so
%{_mandir}/man*/*
%{_bindir}/*
%exclude %{_bindir}/gsx
%exclude %{_bindir}/ijs-config
%exclude %{_datadir}/ghostscript/%{version}/examples
%exclude %{_datadir}/ghostscript/%{version}/doc

%files doc
%defattr(-,root,root)
%doc %{_datadir}/ghostscript/%{version}/examples
%doc %{_datadir}/ghostscript/%{version}/doc

%files gsx
%defattr(-,root,root)
%{_bindir}/gsx

%files devel
%defattr(-,root,root)
%dir %{_includedir}/ghostscript
%{_includedir}/ghostscript/*.h
%dir %{_includedir}/ijs
%{_includedir}/ijs/*
%{_bindir}/ijs-config
%{_libdir}/pkgconfig/ijs.pc
%{_libdir}/libijs.so
%{_libdir}/libgs.so

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 9.14-2
- Rebuild for new 4.0 release.

