%define snap %nil 
Summary:  Qt toolkit
Name:	  qt4
Version:  4.8.7
Release:  14
License:  GPL/QPL
Url:   	  http://www.trolltech.com/products/qt/

Source0:  qt-everywhere-opensource-src-%{version}%{snap}.tar.gz 
Source11: qt4.sh
Source13: qt4.macros

# these should match contents of SOURCE13: 
%define _qt4_prefix    %{_libdir}/qt4
%define _qt4_bindir    %{_qt4_prefix}/bin
%define _qt4_datadir   %{_qt4_prefix}/share
%define _qt4_docdir    %{_qt4_prefix}/doc
%define _qt4_headerdir %{_includedir}
%define _qt4_libdir    %{_libdir}
%define _qt4_plugindir %{_qt4_prefix}/plugins
%define _qt4_sysconfdir %{_sysconfdir}
%define _qt4_translationdir %{_qt4_prefix}/translations


# set default QMAKE_CFLAGS_RELEASE
Patch2: qt-everywhere-opensource-src-4.8.0-tp-multilib-optflags.patch
# get rid of timestamp which causes multilib problem
Patch4: qt-everywhere-opensource-src-4.8.5-uic_multilib.patch
# reduce debuginfo in qtwebkit (webcore)
Patch5: qt-everywhere-opensource-src-4.8.5-webcore_debuginfo.patch
# cups16 printer discovery
Patch6: qt-cupsEnumDests.patch
# enable ft lcdfilter
Patch15: qt-x11-opensource-src-4.5.1-enable_ft_lcdfilter.patch
# may be upstreamable, not sure yet
# workaround for gdal/grass crashers wrt glib_eventloop null deref's
Patch23: qt-everywhere-opensource-src-4.6.3-glib_eventloop_nullcheck.patch
# hack out largely useless (to users) warnings about qdbusconnection
# (often in kde apps), keep an eye on https://git.reviewboard.kde.org/r/103699/
Patch25: qt-everywhere-opensource-src-4.8.3-qdbusconnection_no_debug.patch
Patch26: qt-everywhere-opensource-src-4.8.5-qt_plugin_path.patch
Patch27: qt-everywhere-opensource-src-4.8.4-qmake_pkgconfig_requires_private.patch
Patch28: qt-x11-opensource-src-4.5.0-fix-qatomic-inline-asm.patch
Patch29: qt-everywhere-opensource-src-4.6.2-cups.patch
Patch30: qt-everywhere-opensource-src-4.8.0-tp-qtreeview-kpackagekit-crash.patch
Patch32: qt-everywhere-opensource-src-4.8.3-no_Werror.patch
Patch33: qt-everywhere-opensource-src-4.8.0-QTBUG-22037.patch
Patch34: qt-everywhere-opensource-src-4.8.5-QTBUG-21900.patch
Patch35: qt-everywhere-opensource-src-4.8.0-s390-atomic.patch
Patch36: qt-everywhere-opensource-src-4.8.2--assistant-crash.patch
Patch37: qt-everywhere-opensource-src-4.8.5-QTBUG-4862.patch
Patch38: qt-4.8-poll.patch
Patch39: qt-everywhere-opensource-src-4.8.1-qtgahandle.patch
Patch40: qt-everywhere-opensource-src-4.8.5-qgtkstyle_disable_gtk_theme_check.patch
Patch42: qt-everywhere-opensource-src-4.8.5-QTBUG-22829.patch

# fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
Patch84: qt-everywhere-opensource-src-4.8.5-QTBUG-35459.patch

# systemtrayicon plugin support (for appindicators)
Patch86: qt-everywhere-opensource-src-4.8.6-systemtrayicon.patch

# fixes for LibreOffice from the upstream Qt bug tracker (#1105422):
Patch87: qt-everywhere-opensource-src-4.8.6-QTBUG-37380.patch
Patch88: qt-everywhere-opensource-src-4.8.6-QTBUG-34614.patch
Patch89: qt-everywhere-opensource-src-4.8.6-QTBUG-38585.patch

ExclusiveArch: %{ix86} x86_64 ppc ppc64 sparc sparc64

BuildRequires: dbus-devel >= 0.62

Requires(pre):  /etc/ld.so.conf.d

BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: libpng-devel
BuildRequires: libungif-devel
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig
BuildRequires: libxml2-devel

BuildRequires: zlib-devel
BuildRequires: glib2-devel

BuildRequires: sqlite-devel

BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(NetworkManager)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(zlib)
BuildRequires: rsync

%define gl_deps pkgconfig(gl) pkgconfig(glu)
%define x_deps pkgconfig(ice) pkgconfig(sm) pkgconfig(xcursor) pkgconfig(xext) pkgconfig(xfixes) pkgconfig(xft) pkgconfig(xi) pkgconfig(xinerama) pkgconfig(xrandr) pkgconfig(xrender) pkgconfig(xt) pkgconfig(xv) pkgconfig(x11) pkgconfig(xproto)
BuildRequires: %{gl_deps}
BuildRequires: %{x_deps}
BuildRequires: pkgconfig(gstreamer-0.10)
BuildRequires: pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires: pkgconfig(gtk+-2.0)


Obsoletes: %{name}-config < %{version}-%{release}
Provides:  %{name}-config = %{version}-%{release}

%description 
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package devel
Summary: Development files for the Qt toolkit
Requires: %{name} = %{version}-%{release}
Requires: libpng-devel
Requires: libjpeg-devel
Requires: pkgconfig
Requires: pkgconfig(gl) pkgconfig(glu)
Requires: pkgconfig(ice) pkgconfig(sm) pkgconfig(xcursor) pkgconfig(xext) pkgconfig(xfixes) pkgconfig(xft) 
Requires: pkgconfig(xi) pkgconfig(xinerama) pkgconfig(xrandr) pkgconfig(xrender) pkgconfig(xt) pkgconfig(xv) pkgconfig(x11) pkgconfig(xproto)

Obsoletes: %{name}-designer < %{version}-%{release}
Provides:  %{name}-designer = %{version}-%{release}
%description devel
This package contains the files necessary to develop
applications using the Qt toolkit.  Includes:
Qt Linguist

%package doc
Summary: API documentation, demos and example programs for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt4-demos
Provides: %{name}-assistant = %{version}-%{release}
%description doc
%{summary}.  Includes:
Qt Assistant, Qt Demo

%package sqlite 
Summary: SQLite driver for Qt's SQL classes
Requires: %{name} = %{version}-%{release}
Requires: sqlite
%description sqlite 
%{summary}.

%package demos 
Summary: Demos for qt4 programing
Requires: %{name} = %{version}-%{release}
%description demos 
This package contains some demos for qt4 programing.

%prep
%setup -q -n qt-everywhere-opensource-src-%{version}%{snap}
%patch2 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch15 -p1
%patch23 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch42 -p1

%patch84 -p1
%patch86 -p1
%patch87 -p1
%patch88 -p0
%patch89 -p0

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

%define platform linux-g++

sed -i -e "s|-O2|$RPM_OPT_FLAGS|g" \
  mkspecs/%{platform}/qmake.conf

sed -i -e "s|^\(QMAKE_LFLAGS_RELEASE.*\)|\1 $RPM_LD_FLAGS|" \
  mkspecs/common/g++-unix.conf

# undefine QMAKE_STRIP (and friends), so we get useful -debuginfo pkgs (#193602)
sed -i -e 's|^\(QMAKE_STRIP.*=\).*$|\1|g' mkspecs/common/linux.conf

# let makefile create missing .qm files, the .qm files should be included in qt upstream
for f in translations/*.ts ; do
  touch ${f%.ts}.qm
done


%build
./configure -opensource -v \
  -confirm-license \
  -optimized-qmake \
  -prefix %{_qt4_prefix} \
  -bindir %{_qt4_bindir} \
  -datadir %{_qt4_datadir} \
  -docdir %{_qt4_docdir} \
  -headerdir %{_qt4_headerdir} \
  -libdir %{_qt4_libdir} \
  -plugindir %{_qt4_plugindir} \
  -sysconfdir %{_qt4_sysconfdir} \
  -translationdir %{_qt4_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -cups \
  -fontconfig \
  -largefile \
  -gtkstyle \
  -no-rpath \
  -no-separate-debug-info \
  -sm \
  -stl \
  -system-libpng \
  -system-libjpeg \
  -system-zlib \
  -xcursor \
  -xfixes \
  -xinerama \
  -xshape \
  -xrandr \
  -xrender \
  -xkb \
  -glib \
  -icu \
  -openssl-linked \
  -xmlpatterns \
  -webkit \
  -no-phonon \
  -plugin-sql-sqlite \
  -dbus \
  -no-nas-sound

make %{?_smp_mflags}


# recreate .qm files
LD_LIBRARY_PATH=`pwd`/lib bin/lrelease translations/*.ts


%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}


pushd %{buildroot}%{_qt4_libdir}
for lib in libQt*.so ; do
   libbase=`basename $lib .so | sed -e 's/^lib//'`
#  ln -s $lib lib${libbase}_debug.so
   echo "INPUT(-l${libbase})" > lib${libbase}_debug.so
done
for lib in libQt*.a ; do
   libbase=`basename $lib .a | sed -e 's/^lib//' `
#  ln -s $lib lib${libbase}_debug.a
   echo "INPUT(-l${libbase})" > lib${libbase}_debug.a
done
popd

# hardlink files to %{_bindir}, add -qt4 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt4_bindir}
for i in * ; do
  case "${i}" in
    # qt3 stuff
    assistant|designer|linguist|lrelease|lupdate|moc|qmake|qtconfig|qtdemo|uic)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt4
      ln -sv ${i} ${i}-qt4
      ;;
    *)
      ;;
  esac
done
popd

# rpm macros
install -p -m644 -D %{SOURCE13} %{buildroot}%{_libdir}/rpm/macros.d/macros.qt4

#install private headers
pushd include
for i in `find . -name private`
do
  dir=`dirname $i`
  mkdir -p $RPM_BUILD_ROOT/%{_qt4_headerdir}/$dir
  cp -r $dir/private $RPM_BUILD_ROOT/%{_qt4_headerdir}/$dir
done 
popd


#clean
pushd $RPM_BUILD_ROOT
find . -name .obj|xargs rm -rf
popd

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%dir %{_qt4_prefix}
%dir %{_qt4_bindir}
%dir %{_qt4_datadir}

#%config(noreplace) %{qt4_sysconfdir}/Trolltech.conf
%{_qt4_datadir}/phrasebooks/
%{_qt4_libdir}/libQtCore.so.*
%{_qt4_libdir}/libQtDBus.so.*
%{_qt4_libdir}/libQtNetwork.so.*
%{_qt4_libdir}/libQtSql.so.*
%{_qt4_libdir}/libQtTest.so.*
%{_qt4_libdir}/libQtXml.so.*
%{_qt4_libdir}/libQtXmlPatterns.so.*
%{_qt4_libdir}/libQtScript.so.*
%{_qt4_libdir}/libQtCLucene.so.*
%{_qt4_libdir}/libQtHelp.so.*
%{_qt4_libdir}/libQtMultimedia.so.*
%{_qt4_libdir}/libQtDeclarative.so.*
#%{qt4_libdir}/libphonon.so.*
%dir %{_qt4_plugindir}
%dir %{_qt4_plugindir}/sqldrivers/
%{_qt4_translationdir}/
%{_qt4_libdir}/libQtScriptTools.so.*
%{_qt4_libdir}/libQt3Support.so.*
%{_qt4_libdir}/libQtDesigner.so.*
%{_qt4_libdir}/libQtDesignerComponents.so.*
%{_qt4_libdir}/libQtGui.so.*
%{_qt4_libdir}/libQtOpenGL.so.*
%{_qt4_libdir}/libQtSvg.so.*
%{_qt4_libdir}/libQtWebKit.so.*
%{_qt4_plugindir}/*
%exclude %{_qt4_plugindir}/designer
%exclude %{_qt4_plugindir}/sqldrivers
%{_qt4_bindir}/qt*config*
%{_bindir}/qt*config*
%{_qt4_prefix}/imports/*

%files devel
%defattr(-,root,root,-)
%{_bindir}/*
%exclude %{_bindir}/qt*config*
%exclude %{_bindir}/assistant*
%exclude %{_bindir}/qt*demo*
%{_libdir}/rpm/macros.d/macros.qt4
%{_qt4_bindir}/qcollectiongenerator
%{_qt4_bindir}/qhelpconverter
%{_qt4_bindir}/qhelpgenerator
%{_qt4_bindir}/qmlplugindump
%{_qt4_bindir}/qmlviewer
%{_qt4_bindir}/qttracereplay
%{_qt4_bindir}/xmlpatternsvalidator

%{_qt4_bindir}/lrelease*
%{_qt4_bindir}/lupdate*
%{_qt4_bindir}/moc*
%{_qt4_bindir}/qdbus*
%{_qt4_bindir}/pixeltool*
%{_qt4_bindir}/qmake*
%{_qt4_bindir}/xmlpatterns
%{_qt4_bindir}/qt3to4
%{_qt4_bindir}/rcc*
%{_qt4_bindir}/uic*
%{_qt4_bindir}/lconvert
%{_qt4_headerdir}/*
%{_qt4_datadir}/mkspecs/
%{_qt4_datadir}/q3porting.xml
%{_qt4_libdir}/lib*.so
%{_qt4_libdir}/libQt*.a
%{_qt4_libdir}/lib*.prl
%{_libdir}/pkgconfig/*.pc
# Qt designer
%{_qt4_bindir}/designer*
%{_qt4_plugindir}/designer/
# Qt Linguist
%{_qt4_bindir}/linguist*
%{_qt4_prefix}/tests/qt4/*


%files doc
%defattr(-,root,root,-)
%dir %{_qt4_docdir}
%{_qt4_bindir}/qdoc3
%{_qt4_docdir}/html
%{_qt4_docdir}/src
%{_qt4_docdir}/qch
%exclude %{_qt4_prefix}/demos/
%{_qt4_prefix}/examples/
# Qt Assistant
%{_qt4_bindir}/assistant*
%{_bindir}/assistant*
# Qt Demo
%exclude %{_qt4_bindir}/qt*demo*


%files demos
%{_qt4_bindir}/qt*demo*
%{_bindir}/qt*demo*
%{_qt4_prefix}/demos

%files sqlite 
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlite.*


%changelog
* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 4.8.7-14
- Fix devel package requires

* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 4.8.7-13
- Rebuild

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.8.7-12
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

