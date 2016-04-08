Name: qt5-qtwebkit
Version: 5.6.0
Release: 1
Summary: QtWebKit component

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtwebkit-opensource-src-%{version}.tar.xz 

# Search /usr/lib{,64}/mozilla/plugins-wrapped for browser plugins too
Patch1: qtwebkit-opensource-src-5.2.0-pluginpath.patch

# smaller debuginfo s/-g/-g1/ (debian uses -gstabs) to avoid 4gb size limit
Patch3: qtwebkit-opensource-src-5.0.1-debuginfo.patch

# tweak linker flags to minimize memory usage on "small" platforms
Patch4: qtwebkit-opensource-src-5.2.0-save_memory.patch

# Add AArch64 support
Patch7: 0001-Add-ARM-64-support.patch

# truly madly deeply no rpath please, kthxbye
Patch8: qtwebkit-opensource-src-5.2.1-no_rpath.patch

Patch9: qt5-webkit-pthread.patch

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
BuildRequires: qt5-qtlocation-devel >= %{version}
BuildRequires: qt5-qtsensors-devel >= %{version}
BuildRequires: qt5-qtwebchannel-devel >= %{version}

BuildRequires: bison
BuildRequires: flex
BuildRequires: gperf
BuildRequires: libicu-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: pkgconfig(gio-2.0) pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gl)

BuildRequires: pkgconfig(gstreamer-1.0) 
BuildRequires: pkgconfig(gstreamer-app-1.0)
BuildRequires: pkgconfig(gstreamer-audio-1.0)
BuildRequires: pkgconfig(gstreamer-base-1.0)
BuildRequires: pkgconfig(gstreamer-pbutils-1.0)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(xcomposite) pkgconfig(xrender)
BuildRequires: perl perl(version)
BuildRequires: perl(Digest::MD5) perl(Text::ParseWords) perl(Getopt::Long)
BuildRequires: ruby
BuildRequires: zlib-devel

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools-devel
#for absolute path qdoc
BuildRequires: qt5-qtbase-devel


%description
QtWebKit component

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt5-qtbase-devel >= %{version}
Requires: qt5-qtdeclarative-devel >= %{version}
Requires: qt5-qtlocation-devel >= %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtwebkit-opensource-src-%{version}

%patch1 -p1 -b .pluginpath
%patch3 -p1 -b .debuginfo
%patch4 -p1 -b .save_memory
%patch7 -p1 -b .aarch64
%patch8 -p1 -b .no_rpath
%patch9 -p1 -b .pthread

%build
# WTF... http://lists.qt-project.org/pipermail/development/2016-March/025362.html
mkdir %{buildroot}/.git
qmake-qt5

make %{?_smp_mflags}
make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}

#fake debug library
pushd %{buildroot}%{_qt5_libdir}
for lib in libQt*.so ; do
 ln -s $lib $(basename $lib .so)_debug.so
done
popd

#fix pkgconfig files
sed -i -e 's:-L/home[^ ]\+::g' $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*.pc


%files
%{_libdir}/*.so.*
%{_libdir}/qt5/libexec/QtWebPluginProcess
%{_libdir}/qt5/libexec/QtWebProcess
%{_libdir}/qt5/qml/QtWebKit/experimental/libqmlwebkitexperimentalplugin.so
%{_libdir}/qt5/qml/QtWebKit/experimental/qmldir
%{_libdir}/qt5/qml/QtWebKit/libqmlwebkitplugin.so
%{_libdir}/qt5/qml/QtWebKit/plugins.qmltypes
%{_libdir}/qt5/qml/QtWebKit/qmldir

%files devel
%{_libdir}/cmake/*
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/qt5/include/*
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_docdir}/qt5/*

%changelog
* Fri Apr 08 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-1
- Release 5.6.0

* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-4
- Rebuild with icu 56.1

* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

