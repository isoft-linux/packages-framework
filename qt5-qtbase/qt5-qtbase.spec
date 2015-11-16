Name: qt5-qtbase 
Version: 5.5.1
Release: 13
Summary: Base components of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtbase-opensource-src-%{version}.tar.xz 

# xinitrc script to check for OpenGL 1 only drivers and automatically set
# QT_XCB_FORCE_SOFTWARE_OPENGL for them
Source6: 10-qt5-check-opengl2.sh

#macros for rpm system.
Source10: qt5.macros

#setup PATH to find qt5 utility
Source20: qt5-path.sh

# fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
Patch1: qtbase-opensource-src-5.3.2-QTBUG-35459.patch

# unconditionally enable freetype lcdfilter support
Patch2: qtbase-opensource-src-5.2.0-enable_ft_lcdfilter.patch

# hack out largely useless (to users) warnings about qdbusconnection
# (often in kde apps), keep an eye on https://git.reviewboard.kde.org/r/103699/
Patch3: qtbase-opensource-src-5.5.1-qdbusconnection_no_debug.patch

# Qt5 application crashes when connecting/disconnecting displays
# https://bugzilla.redhat.com/show_bug.cgi?id=1083664
Patch10: qtbase-opensource-src-5.5-disconnect_displays.patch

# Followup https://codereview.qt-project.org/#/c/138201/ adapted for 5.5
# XCB screen connection and disconnection bug fix
Patch11: 138201.patch

#Already upstream, will be in 5.5.2
#https://bugreports.qt.io/browse/QTBUG-48350
Patch13: qtbase-fix-comparison-qbytearray-and-qstring.patch
Patch14: qtbase-fix-qlinedit-visibility-handling-of-side-widgets.patch
Patch15: qtbase-fix_reuse_address_problem_qtbug-47011.patch
Patch16: qtbase-report-correct-networkaccessibility-qtbug-46323.patch
Patch17: qtbase-fix-qimage-DPM-value-with-some-orientations.patch

#Already reported, https://bugreports.qt.io/browse/QTBUG-45812
Patch30: qt5-qtbase-fix-chromium-and-other-application-dnd.patch

#Wrong, but we do that!!
Patch60: qtbase-do-not-exit-when-error-happened.patch

#revert: https://codereview.qt-project.org/#/c/89777/
#This is partial fix of "kcmshell5 kwineffects popup menu wrong position" issue.
#another two revert happened in qtquickcontrols
Patch61: qtbase-revert-89777.patch

#https://bugreports.qt.io/browse/QTBUG-49061
#it also should fix kmozillahelper segfault issue
Patch62: qtbase-unload-plugin-QTBUG-49061.patch

# All these macros should match contents of SOURCE10: 
%define qtdir %{_libdir}/qt5
%define qt5_prefix %{_libdir}/qt5
%define qt5_bindir %{_libdir}/qt5/bin
%define qt5_datadir %{_datadir}/qt5
%define qt5_docdir %{_docdir}/qt5
%define qt5_headerdir %{_libdir}/qt5/include
%define qt5_libdir %{_libdir}
%define qt5_plugindir %{qt5_prefix}/plugins
%define qt5_sysconfdir %{_sysconfdir}
%define qt5_translationdir %{_qt5_datadir}/translations


BuildRequires: cmake
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: libjpeg-turbo-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel

BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-2.0)
# xcb-sm
BuildRequires: pkgconfig(ice) pkgconfig(sm)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(NetworkManager)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(dbus-1)

BuildRequires: pkgconfig(libinput)
BuildRequires: pkgconfig(xcb-xkb) >= 1.10
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1
BuildRequires: pkgconfig(xkbcommon-x11) >= 0.4.1
BuildRequires: pkgconfig(atspi-2)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gbm)
#It's ok, even we requires gles, it's still link to GL by default.
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(sqlite3) >= 3.7
BuildRequires: pkgconfig(xkeyboard-config)

BuildRequires: pkgconfig(harfbuzz) >= 0.9.31
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libpcre) >= 8.30

BuildRequires: pkgconfig(xcb) pkgconfig(xcb-glx) pkgconfig(xcb-icccm) pkgconfig(xcb-image) pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil)
BuildRequires: pkgconfig(zlib)

BuildRequires: libproxy-devel

BuildRequires: mtdev-devel
BuildRequires: tslib-devel

#wired but needed, if we want to build docs, we need qdoc in qt5-qtbase-devel
#by Cjacker.

#for absolute path qdoc
BuildRequires: qt5-qtbase-devel

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build without doc and install it, then buld qttools without doc and install it, 
#we can generate docs.
#then rebuild these two rpm package.

#for qhelpgenerator
BuildRequires: qt5-qttools-devel

%description
Base components of Qt

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig(gl)
Requires: pkgconfig(egl)
#Requires: pkgconfig(glesv2)

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtbase-opensource-src-%{version}

%patch1 -p1 
%patch2 -p1
%patch3 -p1

%patch10 -p1
%patch11 -p1

%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

%patch30 -p1

%patch60 -p1
%patch61 -p1

%patch62 -p1

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

%define platform linux-g++

sed -i -e "s|-O2|$RPM_OPT_FLAGS|g" \
  mkspecs/%{platform}/qmake.conf

sed -i -e "s|^\(QMAKE_LFLAGS_RELEASE.*\)|\1 $RPM_LD_FLAGS|" \
  mkspecs/common/g++-unix.conf

# undefine QMAKE_STRIP (and friends), so we get useful -debuginfo pkgs
sed -i -e 's|^\(QMAKE_STRIP.*=\).*$|\1|g' mkspecs/common/linux.conf

%build
./configure -v \
 -confirm-license \
 -opensource \
 -optimized-qmake \
 -prefix %{qt5_prefix} \
 -bindir %{qt5_bindir} \
 -datadir %{qt5_datadir} \
 -docdir %{qt5_docdir} \
 -headerdir %{qt5_headerdir} \
 -libdir %{qt5_libdir} \
 -plugindir %{qt5_plugindir} \
 -sysconfdir %{qt5_sysconfdir} \
 -translationdir %{qt5_translationdir} \
 -platform %{platform} \
 -release \
 -shared \
 -cups \
 -fontconfig \
 -largefile \
 -openssl-linked \
 -nomake examples \
 -no-rpath \
 -no-separate-debug-info \
 -no-reduce-relocations \
 -sm \
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
 -xinput2 \
 -glib \
 -dbus \
 -libproxy \
 -no-sql-mysql \
 -no-sql-psql \
 -no-sql-ibase \
 -no-sql-oci \
 -no-sql-odbc \
 -no-sql-sqlite2 \
 -no-sql-db2 \
 -no-sql-tds \
 -plugin-sql-sqlite \
 -system-sqlite \
 -c++11 \
 -xcb \
 -system-xcb \
 -system-freetype \
 -system-harfbuzz



make %{?_smp_mflags}
make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}

#fake debug library
pushd %{buildroot}%{qt5_libdir}
for lib in libQt*.so ; do
 ln -s $lib $(basename $lib .so)_debug.so
done
for lib in libQt*.a ; do
 ln -s $lib $(basename $lib .a)_debug.a
done
popd

# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
 case "${i}" in
 moc|qdbuscpp2xml|qdbusxml2cpp|qmake|rcc|syncqt|uic)
 ln -v ${i} %{buildroot}%{_bindir}/${i}-qt5
 ln -sv ${i} ${i}-qt5
 ;;
 *)
 ln -v ${i} %{buildroot}%{_bindir}/${i}
 ;;
 esac
done
popd


# rpm macros
install -p -m644 -D %{SOURCE10} \
 %{buildroot}%{_libdir}/rpm/macros.d/macros.qt5

# path setup
install -p -m755 -D %{SOURCE20} %{buildroot}%{_sysconfdir}/profile.d/qt5-path.sh

mkdir -p %{buildroot}%{_libdir}/qt5/examples
if [ -d "examples/" ]; then
 cp -r examples/* %{buildroot}%{_libdir}/qt5/examples/
 rm -rf %{buildroot}%{_libdir}/qt5/examples/*.pro
fi

install -p -m755 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh

%files
#own this dir
%dir %{_libdir}/qt5
%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh
%{_sysconfdir}/profile.d/qt5-path.sh
%{_libdir}/lib*.so.*
%{_libdir}/qt5/plugins/*

%files devel
%{_libdir}/rpm/macros.d/macros.qt5
%{_bindir}/*
%{_libdir}/qt5/bin/*
%{_libdir}/cmake/*
%{_libdir}/*.a
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/qt5/examples
%{_libdir}/qt5/include
%{_libdir}/qt5/mkspecs
%{_docdir}/qt5

%changelog
* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-13
- Should fix kmozillahelper segfault issue

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-13
- Revert Ensure transient parents are top level widgets
- this is partial fix of "kcmshell5 kwineffects popup menu wrong position" issue.
- another two revert happened in qtquickcontrols

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-11
- Fix QTBUG-49220

* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-10
- add patches, fix QTBUG-48350, QTBUG-48806, QTBUG-48899, QTBUG-39660, QTBUG-47011, QTBUG-46323

* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-9
- Add patch to fix 'https://code.google.com/p/chromium/issues/detail?id=543940'
- Now support Xdnd Text/URL from Qt5 to chromium/chrome/emacs etc. 

* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-8
- Bump version

* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-7
- Add more requires for devel package

* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-6
- Rebuild with icu 56.1

* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-5
- Fix Requires to pkgconfig(gl) of devel package

* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-4
- Add patch to fix xcb screen connect/disconnect issue

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

* Thu Aug 13 2015 Cjacker <cjacker@foxmail.com>
- add patch100, fix jpg file reader.

* Mon Jul 20 2015 Cjacker <cjacker@foxmail.com>
- drop '-reduce-relocations'
