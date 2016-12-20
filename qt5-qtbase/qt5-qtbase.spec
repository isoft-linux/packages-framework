Name: qt5-qtbase 
Version: 5.7.1
Release: 4
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

# QTBUG-54926
Patch104: standardkey-delete.patch

# All these macros should match contents of SOURCE10: 
%define bootstrap   0
%define qtdir %{_libdir}/qt5
%define qt5_prefix %{_libdir}/qt5
%define qt5_bindir %{_libdir}/qt5/bin
%define qt5_datadir %{_datadir}/qt5
%if !%{bootstrap}
%define qt5_docdir %{_docdir}/qt5
%endif
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
%if !%{bootstrap}
BuildRequires: qt5-qttools-devel
%endif

%description
Base components of Qt

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig(gl)
Requires: pkgconfig(egl)
Requires: libicu
#Requires: pkgconfig(glesv2)

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtbase-opensource-src-%{version}
%patch104 -p1

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
%if !%{bootstrap}
 -docdir %{qt5_docdir} \
%endif
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
 -c++std c++11 \
 -xcb \
 -system-xcb \
 -system-freetype \
 -system-harfbuzz

make %{?_smp_mflags}
%if !%{bootstrap}
make docs
%endif

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
%if !%{bootstrap}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

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
%if !%{bootstrap}
%{_docdir}/qt5
%endif

%changelog
* Tue Dec 20 2016 sulit - 5.7.1-4
- rebuild qt5-qtbase in koji

* Mon Dec 19 2016 sulit - 5.7.1-3
- rebuild qt5-qtbase

* Fri Dec 16 2016 sulit - 5.7.1-2
- add requires libicu

* Thu Dec 15 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.1-1
- 5.7.1-1

* Thu Nov 24 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-8
- 5.7.0-8

* Mon Nov 21 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-7
- Drop dbus related patches.

* Mon Jul 25 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-6
- Fix QTBUG-54926.

* Fri Jul 08 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-5
- Fix QTBUG-49061.
- Merge the QDBusMetaType's custom information to QDBusConnectionManager.

* Wed Jul 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-3
- Fix QTBUG-52988.

* Thu Jun 30 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-2
- Rebuild with gcc-6.1.0

* Tue Jun 21 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-1
- 5.7.0

* Tue May 10 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-beta-1
- 5.7.0-beta-1

* Thu Apr 14 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-7
- Add combo popup wrong position REVERT patch.
- Add disconnect displays hang patch.

* Wed Apr 6 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-5
- qdoc

* Thu Mar 24 2016 sulit <sulitsrc@gmail.com> - 5.6.0-3
- second build

* Thu Mar 24 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-2
- Release 5.6.0
- first build

* Mon Dec 21 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-20
- Add poll support, hope to fix trash hang issue

* Fri Dec 18 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-19
- Fix QTBUG-47812/49395

* Thu Dec 17 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.5.1-18
- Drop close windows when requested to save application state patch.

* Tue Dec 15 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.5.1-17
- Don't close windows when requested to save application state. QTBUG-49667, KDEBUG-354724

* Wed Dec 09 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.5.1-16
- Fix QWidget::setWindowRole() QTBUG-45484

* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-15
- Fix QTBUG-18722,QTBUG-46887,QTBUG-48393

* Thu Dec 03 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-14
- Fix QTBUG-47272, QTBUG-49363, 49399

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
