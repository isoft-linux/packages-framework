Name:	    qt5-qtbase	
Version:	5.5.0
Release:	1
Summary:    Base components of Qt


Group:	    Extra/Runtime/Library	
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qtbase-opensource-src-%{version}.tar.xz	

# xinitrc script to check for OpenGL 1 only drivers and automatically set
# QT_XCB_FORCE_SOFTWARE_OPENGL for them
Source6: 10-qt5-check-opengl2.sh

#macros for rpm system.
Source10:   qt5.macros

#setup PATH to find qt5 utility
Source20:   qt5-path.sh

# fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
Patch4: qtbase-opensource-src-5.3.2-QTBUG-35459.patch

# unconditionally enable freetype lcdfilter support
Patch12: qtbase-opensource-src-5.2.0-enable_ft_lcdfilter.patch


# fix issue on big endian platform
Patch13: qtbase-opensource-src-5.5.x-big-endian.patch

# hack out largely useless (to users) warnings about qdbusconnection
# (often in kde apps), keep an eye on https://git.reviewboard.kde.org/r/103699/
Patch25: qtbase-opensource-src-5.5.1-qdbusconnection_no_debug.patch

# Qt5 application crashes when connecting/disconnecting displays
# https://bugzilla.redhat.com/show_bug.cgi?id=1083664
Patch51: qtbase-opensource-src-5.5-disconnect_displays.patch

# https://bugreports.qt.io/browse/QTBUG-33093
# https://codereview.qt-project.org/#/c/95219/
Patch52:  qtbase-opensource-src-5.4.1-QTBUG-33093.patch

# https://bugreports.qt.io/browse/QTBUG-45484
# QWidget::setWindowRole does nothing
# adapted to apply on top of patch51
Patch53: qtbase-opensource-src-5.4.1-QTBUG-45484.patch

# https://bugreports.qt.io/browse/QTBUG-46310
#SM_CLIENT_ID property is not set
Patch54: qtbase-opensource-src-5.4.1-QTBUG-46310.patch

Patch55: socket-readyread-stop-firing-BUG46552.patch

# All these macros should match contents of SOURCE10: 
%define qtdir %{_libdir}/qt5
%define qt5_prefix  %{_libdir}/qt5
%define qt5_bindir  %{_libdir}/qt5/bin
%define qt5_datadir     %{_datadir}/qt5
%define qt5_docdir  %{_docdir}/qt5
%define qt5_headerdir   %{_libdir}/qt5/include
%define qt5_libdir  %{_libdir}
%define qt5_plugindir   %{qt5_prefix}/plugins
%define qt5_sysconfdir  %{_sysconfdir}
%define qt5_translationdir %{qt5_datadir}/translations


BuildRequires:  mesa-libGL-devel libICE-devel libSM-devel libX11-devel libXext-devel
BuildRequires:  libxkbcommon-devel libXi-devel libXrandr-devel libXrender-devel
BuildRequires:  openssl-devel cups-devel
BuildRequires:  fontconfig-devel freetype-devel
BuildRequires:  glib2-devel zlib-devel libpng-devel libjpeg-turbo-devel
BuildRequires:  sqlite-devel dbus-devel libicu-devel libxslt-devel pcre-devel
BuildRequires:  bison, flex, gawk, gperf

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build without doc and install it, then buld qttools without doc and install it, 
#we can generate docs.
#then rebuild these two rpm package.

#for qhelpgenerator
BuildRequires:  qt5-qttools
#for absolute path qdoc
BuildRequires:  qt5-qtbase

%description
Base components of Qt

%package        devel
Summary:        Development files for %{name}
Group:          Extra/Development/Library
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtbase-opensource-src-%{version}

%patch4 -p1 -b .QTBUG-35459
%patch12 -p1 -b .enable_ft_lcdfilter
#%patch13 -p1
%patch25 -p1 -b .qdbusconnection_no_debug

%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1

%build
%define platform linux-g++

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
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt5
      ln -sv ${i} ${i}-qt5
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
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
* Mon Jul 20 2015 Cjacker <cjacker@foxmail.com>
- drop '-reduce-relocations'
