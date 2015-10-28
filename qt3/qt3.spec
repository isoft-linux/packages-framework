Summary: The shared library for the Qt GUI toolkit.
Name: qt3
Version: 3.3.8
Release: 9 
Epoch: 1
License: GPL/QPL
Url: http://www.troll.no
Source0: ftp://ftp.troll.no/qt/source/qt-x11-free-%{version}.tar.bz2
Source2: qt3.sh
Source3: qt3.csh

Patch1: qt-3.3.4-print-CJK.patch
Patch2: qt-3.0.5-nodebug.patch
Patch3: qt-3.1.0-makefile.patch
Patch4: qt-x11-free-3.3.7-umask.patch
Patch5: qt-x11-free-3.3.6-strip.patch
Patch7: qt-x11-free-3.3.2-quiet.patch
Patch8: qt-x11-free-3.3.3-qembed.patch
Patch12: qt-uic-nostdlib.patch
Patch13: qt-x11-free-3.3.6-qfontdatabase_x11.patch
Patch14: qt-x11-free-3.3.3-gl.patch
Patch19: qt-3.3.3-gtkstyle.patch 
Patch20: qt-x11-free-3.3.5-gcc4-buildkey.patch
Patch24: qt-x11-free-3.3.5-uic.patch
Patch25: qt-x11-free-3.3.8-uic-multilib.patch
Patch26: qt-3.3.6-fontrendering-punjabi-209970.patch
Patch27: qt-3.3.6-fontrendering-ml_IN-209097.patch
Patch28: qt-3.3.6-fontrendering-or_IN-209098.patch
Patch29: qt-3.3.6-fontrendering-as_IN-209972.patch
Patch31: qt-3.3.6-fontrendering-te_IN-211259.patch
Patch32: qt-3.3.6-fontrendering-214371.patch
Patch33: qt-3.3.6-fontrendering-#214570.patch
Patch34: qt-3.3.6-fontrendering-ml_IN-209974.patch
Patch35: qt-3.3.6-fontrendering-ml_IN-217657.patch

# immodule patches
Patch50: qt-x11-immodule-unified-qt3.3.8-20071116.diff.bz2
Patch51: qt-x11-immodule-unified-qt3.3.5-20051012-quiet.patch
Patch52: qt-x11-free-3.3.8b-fix-key-release-event-with-imm.diff
Patch53: qt-x11-free-3.3.6-qt-x11-immodule-unified-qt3.3.5-20060318-resetinputcontext.patch
Patch54: qt-x11-free-fix-immodule-compile.patch 

# qt-copy patches
Patch100: 0038-dragobject-dont-prefer-unknown.patch
Patch101: 0047-fix-kmenu-width.diff
Patch102: 0048-qclipboard_hack_80072.patch
Patch103: 0056-khotkeys_input_84434.patch
Patch104: qt-font-default-subst.diff
patch105: 0073-xinerama-aware-qpopup.patch
Patch106: 0076-fix-qprocess.diff
Patch107: 0077-utf8-decoder-fixes.diff
Patch108: qt-3-fix-xim-create-destroy-crash.patch
# upstream patches
Patch200: qt-x11-free-3.3.4-fullscreen.patch

Patch201: qt-add-bold-style-for-missing-font.patch
Patch202: change-default-xim-style-to-overthespot.patch
Patch203: change-qtconfig-default-xim-style-to-overthespot.patch
Patch204: qt-special-char.patch
#for change all fonts name to sans/serif/monospace
Patch205: qt-dirty-hack-for-correct-non-antilias-profile-sans-fontsize.patch
Patch206: qt-drop-xftsubstitue-for-correct-sans-serif-mono.patch
Patch207: qt-x11-free-3.3.8-fix-han-script.patch

Patch300: qt-x11-free-fix-new-glibc.patch
Patch301: qt-rename-im-module-env-to-avoid-conflict.patch

Patch302: qt-glib-main-loop.patch

Patch350: qt-fix-compiler-warnings.patch

Patch402: fatal-X11-errors-when-both-external-display-and-commandline.patch

Patch403: qt-3.3.8-libpng15.patch

Patch404: qt-x11-free-add-linux-clang.patch

Patch500: qt-freetype2.patch


# security patches
# fix for CVE-2013-4549 backported from Qt 4
Patch600: qt-x11-free-3.3.8b-CVE-2013-4549.patch
# fix for CVE-2014-0190 (QTBUG-38367) backported from Qt 4
Patch601: qt-x11-free-3.3.8b-CVE-2014-0190.patch
# fix for CVE-2015-0295 backported from Qt 4
Patch602: qt-x11-free-3.3.8b-CVE-2015-0295.patch
# fix for CVE-2015-1860 backported from Qt 4
Patch603: qt-x11-free-3.3.8b-CVE-2015-1860.patch


%define qt_dirname qt-3.3
%define qtdir %{_libdir}/%{qt_dirname}
%define qt_docdir %{_docdir}/qt-devel-%{version}

%define smp 1
%define immodule 1 
%define debug 0

# MySQL plugins

# sqlite plugins
%define plugin_sqlite -plugin-sql-sqlite

%define plugins_style -qt-style-cde -qt-style-motifplus -qt-style-platinum -qt-style-sgi -qt-style-windows -qt-style-compact -qt-imgfmt-png -qt-imgfmt-jpeg -qt-imgfmt-mng
%define plugins %{plugin_sqlite} %{plugins_style}

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: fileutils
Requires: fontconfig >= 2.0
Requires: /etc/ld.so.conf.d

BuildRequires: glibc-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: giflib-devel
BuildRequires: perl
BuildRequires: sed
BuildRequires: findutils
BuildRequires: cups-devel
BuildRequires: tar
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: libXrender-devel
BuildRequires: libXrandr-devel
BuildRequires: libXcursor-devel
BuildRequires: libXinerama-devel
BuildRequires: libXft-devel
BuildRequires: libXext-devel
BuildRequires: libX11-devel
BuildRequires: libSM-devel
BuildRequires: libICE-devel
BuildRequires: libXt-devel
BuildRequires: libXmu-devel
BuildRequires: libXi-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: mesa-libGL-devel
BuildRequires: sqlite-devel

%package config
Summary: Grapical configuration tool for programs using Qt
Requires: %{name} = %{epoch}:%{version}-%{release}


%package devel
Summary: Development files for the Qt GUI toolkit.
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: freetype-devel
Requires: fontconfig-devel
Requires: libXrender-devel
Requires: libXrandr-devel
Requires: libXcursor-devel
Requires: libXinerama-devel
Requires: libXft-devel
Requires: libXext-devel
Requires: libX11-devel
Requires: libSM-devel
Requires: libICE-devel
Requires: libXt-devel
Requires: xorg-x11-proto-devel
Requires: libpng-devel
Requires: libjpeg-devel
Requires: pkgconfig
Requires: mesa-libGL-devel

%package devel-docs
Summary: Documentation for the Qt GUI toolkit.
Requires: %{name}-devel = %{epoch}:%{version}-%{release}


%package ODBC
Summary: ODBC drivers for Qt's SQL classes.
Requires: %{name} = %{epoch}:%{version}-%{release}


%package MySQL
Summary: MySQL drivers for Qt's SQL classes.
Requires: %{name} = %{epoch}:%{version}-%{release}


%package PostgreSQL
Summary: PostgreSQL drivers for Qt's SQL classes.
Requires: %{name} = %{epoch}:%{version}-%{release}


%package sqlite
Summary: sqlite drivers for Qt's SQL classes.
Requires: %{name} = %{epoch}:%{version}-%{release}


%package designer
Summary: Interface designer (IDE) for the Qt toolkit
Requires: %{name}-devel = %{epoch}:%{version}-%{release}


%description
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications
for the X Window System.

Qt is written in C++ and is fully object-oriented.

This package contains the shared library needed to run qt
applications, as well as the README files for qt.


%description config
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications
for the X Window System.

Qt is written in C++ and is fully object-oriented.

This package contains a grapical configuration tool for programs using Qt.


%description devel
The qt-devel package contains the files necessary to develop
applications using the Qt GUI toolkit: the header files, the Qt meta
object compiler.

Install qt-devel if you want to develop GUI applications using the Qt
toolkit.


%description devel-docs
The qt-devel-docs package contains the man pages, the HTML documentation and
example programs.


%description ODBC
ODBC driver for Qt's SQL classes (QSQL)


%description MySQL
MySQL driver for Qt's SQL classes (QSQL)


%description PostgreSQL
PostgreSQL driver for Qt's SQL classes (QSQL)


%description sqlite
sqlite driver for Qt's SQL classes (QSQL)


%description designer
The qt-designer package contains an User Interface designer tool
for the Qt toolkit.


%prep
%setup -q -n qt-x11-free-%{version}
%patch1 -p1 -b .cjk
%patch2 -p1 -b .ndebug
%patch3 -p1 -b .makefile
%patch4 -p1 -b .umask
%patch5 -p1
%patch7 -p1 -b .quiet
%patch8 -p1 -b .qembed
%patch12 -p1 -b .nostdlib
%patch13 -p1 -b .fonts
%patch14 -p1 -b .gl
%patch19 -p1 -b .gtk
%patch20 -p1 -b .gcc4-buildkey
%patch24 -p1 -b .uic
%patch25 -p1 -b .uic-multilib
%patch26 -p1 -b .fontrendering-punjabi-bz#209970
%patch27 -p1 -b .fontrendering-ml_IN-bz#209097
%patch28 -p1 -b .fontrendering-or_IN-bz#209098
%patch29 -p1 -b .fontrendering-as_IN-bz#209972
%patch31 -p1 -b .fontrendering-te_IN-bz#211259
%patch32 -p1 -b .fontrendering-bz#214371
%patch33 -p1 -b .fontrendering-#214570
%patch34 -p1 -b .fontrendering-#209974
%patch35 -p1 -b .fontrendering-ml_IN-217657

%if %{immodule}
%patch50 -p1
%patch51 -p1 -b .quiet
%patch52 -p1 -b .fix-key-release-event-with-imm
%patch53 -p1 -b .resetinputcontext
%patch54 -p1
%endif

%patch100 -p0 -b .0038-dragobject-dont-prefer-unknown
%patch101 -p0 -b .0047-fix-kmenu-width
%patch102 -p0 -b .0048-qclipboard_hack_80072
%patch103 -p0 -b .0056-khotkeys_input_84434
%patch104 -p0 -b .qt-font-default-subst
%patch105 -p0 -b .0073-xinerama-aware-qpopup
%patch106 -p0 -b .0076-fix-qprocess
%patch107 -p0 -b .0077-utf8-decoder-fixes
%patch108 -p1

%patch200 -p1 -b .fullscreen
%patch201 -p1 -b .add-bold-style-missing
%patch202 -p1
#############%patch203 -p1
%patch204 -p1
####%patch205 -p1
%patch206 -p1
%patch207 -p1
%patch300 -p1
%patch301 -p1

%patch302 -p1

%patch350 -p1

%patch402 -p1

%patch403 -p0
%patch404 -p1

%patch500 -p1


# security patches
%patch600 -p1 -b .CVE-2013-4549
%patch601 -p1 -b .CVE-2014-0190
%patch602 -p1 -b .CVE-2015-0295
%patch603 -p1 -b .CVE-2015-1860


# convert to UTF-8
iconv -f iso-8859-1 -t utf-8 < doc/man/man3/qdial.3qt > doc/man/man3/qdial.3qt_
mv doc/man/man3/qdial.3qt_ doc/man/man3/qdial.3qt

%build
export QTDIR=`/bin/pwd`
export LD_LIBRARY_PATH="$QTDIR/lib:$LD_LIBRARY_PATH"
export PATH="$QTDIR/bin:$PATH"
export QTDEST=%{qtdir}

%if %{smp}
   export SMP_MFLAGS="%{?_smp_mflags}"
%endif

%if %{immodule}
   sh ./make-symlinks.sh
%endif

# set correct X11 prefix
perl -pi -e "s,QMAKE_LIBDIR_X11.*,QMAKE_LIBDIR_X11\t=," mkspecs/*/qmake.conf
perl -pi -e "s,QMAKE_INCDIR_X11.*,QMAKE_INCDIR_X11\t=," mkspecs/*/qmake.conf
perl -pi -e "s,QMAKE_INCDIR_OPENGL.*,QMAKE_INCDIR_OPENGL\t=," mkspecs/*/qmake.conf
perl -pi -e "s,QMAKE_LIBDIR_OPENGL.*,QMAKE_LIBDIR_OPENGL\t=," mkspecs/*/qmake.conf

# don't use rpath
perl -pi -e "s|-Wl,-rpath,| |" mkspecs/*/qmake.conf

perl -pi -e "s|-O2|$INCLUDES %{optflags}|g" mkspecs/*/qmake.conf

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
  perl -pi -e "s,/usr/lib /lib,/usr/%{_lib} /%{_lib},g" config.tests/{unix,x11}/*.test
  perl -pi -e "s,/lib /usr/lib,/%{_lib} /usr/%{_lib},g" config.tests/{unix,x11}/*.test
fi

# build shared, threaded (default) libraries
echo yes | ./configure \
  -v \
  -prefix $QTDEST \
  -docdir %{qt_docdir} \
  -platform linux-g++ \
%if %{debug}
  -debug \
%else
  -release \
%endif
  -shared \
  -largefile \
  -qt-gif \
  -system-zlib \
  -system-libpng \
  -system-libjpeg \
  -no-exceptions \
  -enable-styles \
  -enable-tools \
  -enable-kernel \
  -enable-widgets \
  -enable-dialogs \
  -enable-iconview \
  -enable-workspace \
  -enable-network \
  -enable-canvas \
  -enable-table \
  -enable-xml \
  -enable-opengl \
  -enable-sql \
  -qt-style-motif \
  %{plugins} \
  -stl \
  -thread \
  -cups \
  -sm \
  -xinerama \
  -xrender \
  -xkb \
  -ipv6 \
  -dlopen-opengl \
  -xft \
  -tablet \
  -glibmainloop

make $SMP_MFLAGS src-qmake

# build sqlite plugin
pushd plugins/src/sqldrivers/sqlite
qmake -o Makefile sqlite.pro
popd

make $SMP_MFLAGS src-moc
make $SMP_MFLAGS sub-src
make $SMP_MFLAGS sub-tools UIC="$QTDIR/bin/uic -nostdlib -L $QTDIR/plugins"

%install
rm -rf %{buildroot}

export QTDIR=`/bin/pwd`
export LD_LIBRARY_PATH="$QTDIR/lib:$LD_LIBRARY_PATH"
export PATH="$QTDIR/bin:$PATH"
export QTDEST=%{qtdir}

make install INSTALL_ROOT=%{buildroot}

for i in findtr qt20fix qtrename140 lrelease lupdate ; do
   install bin/$i %{buildroot}%{qtdir}/bin/
done

mkdir -p %{buildroot}%{_libdir}/pkgconfig/
mv %{buildroot}%{qtdir}/lib/pkgconfig/*.pc %{buildroot}%{_libdir}/pkgconfig/

# install man pages
mkdir -p %{buildroot}%{_mandir}
cp -fR doc/man/* %{buildroot}%{_mandir}/

# clean up
make -C tutorial clean
make -C examples clean

# Make sure the examples can be built outside the source tree.
# Our binaries fulfill all requirements, so...
perl -pi -e "s,^DEPENDPATH.*,,g;s,^REQUIRES.*,,g" `find examples -name "*.pro"`

# don't include Makefiles of qt examples/tutorials
find examples -name "Makefile" | xargs rm -f
find examples -name "*.obj" | xargs rm -rf
find examples -name "*.moc" | xargs rm -rf
find tutorial -name "Makefile" | xargs rm -f

for a in */*/Makefile ; do
  sed 's|^SYSCONF_MOC.*|SYSCONF_MOC		= %{qtdir}/bin/moc|' < $a > ${a}.2
  mv -v ${a}.2 $a
done

mkdir -p %{buildroot}/etc/profile.d
install -m 755 %{SOURCE2} %{SOURCE3} %{buildroot}/etc/profile.d/

# Patch qmake to use qt-mt unconditionally
perl -pi -e "s,-lqt ,-lqt-mt ,g;s,-lqt$,-lqt-mt,g" %{buildroot}%{qtdir}/mkspecs/*/qmake.conf

# remove broken links
rm -f %{buildroot}%{qtdir}/mkspecs/default/linux-g++*

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{qtdir}/lib" > %{buildroot}/etc/ld.so.conf.d/qt-%{_arch}.conf


#build KDE apidox need this.
mkdir -p $RPM_BUILD_ROOT/%{qtdir}/doc
pushd $RPM_BUILD_ROOT/%{qtdir}/doc
ln -sf /usr/share/doc/qt-devel-%{version}/html html
popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc FAQ LICENSE.QPL README* changes*
%dir %{qtdir}
%dir %{qtdir}/bin
%dir %{qtdir}/lib
%dir %{qtdir}/plugins
%if %{immodule}
%{qtdir}/plugins/inputmethods
%endif
/etc/ld.so.conf.d/*
%{qtdir}/lib/libqui.so.*
%{qtdir}/lib/libqt*.so.*

%files config
%defattr(-,root,root,-)
%{qtdir}/bin/qtconfig

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %config /etc/profile.d/*
%{qtdir}/bin/moc
%{qtdir}/bin/uic
%{qtdir}/bin/findtr
%{qtdir}/bin/qt20fix
%{qtdir}/bin/qtrename140
%{qtdir}/bin/assistant
%{qtdir}/bin/qm2ts
%{qtdir}/bin/qmake
%{qtdir}/bin/qembed
%{qtdir}/bin/linguist
%{qtdir}/bin/lupdate
%{qtdir}/bin/lrelease
%{qtdir}/include
%{qtdir}/mkspecs
%{qtdir}/lib/libqt*.so
%{qtdir}/lib/libqui.so
%{qtdir}/lib/libeditor.a
%{qtdir}/lib/libdesigner*.a
%{qtdir}/lib/libqassistantclient.a
%{qtdir}/lib/*.prl
%{qtdir}/translations
%{qtdir}/phrasebooks
%{_libdir}/pkgconfig/*
%doc %{qt_docdir}/html
%{qtdir}/doc/html


%files devel-docs
%defattr(-,root,root,-)
%doc examples
%doc tutorial
%{_mandir}/*/*

%files sqlite
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlite.so


%files designer
%defattr(-,root,root,-)
%dir %{qtdir}/plugins/designer
%{qtdir}/templates
%{qtdir}/plugins/designer/*
%{qtdir}/bin/designer

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:3.3.8-9
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

