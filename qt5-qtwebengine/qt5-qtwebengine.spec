Name: qt5-qtwebengine 
Version: 5.5.1
Release: 2 
Summary: QtWebengine Component of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtwebengine-opensource-src-%{version}.tar.xz 

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
BuildRequires: qt5-qtxmlpatterns-devel >= %{version}
BuildRequires: qt5-qtlocation-devel >= %{version}
BuildRequires: qt5-qtsensors-devel >= %{version}
BuildRequires: qt5-qtwebchannel-devel >= %{version}
BuildRequires: qt5-qttools-devel >= %{version}

BuildRequires: bison
BuildRequires: flex
BuildRequires: gperf
BuildRequires: libicu-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libgcrypt-devel
BuildRequires: bzip2-devel
BuildRequires: snappy-devel
BuildRequires: yasm
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gobject-2.0) 
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(jsoncpp)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(libmtp)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libexif)
BuildRequires: pkgconfig(flac++)
BuildRequires: pkgconfig(minizip)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libxslt)
#####BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xcomposite) 
BuildRequires: pkgconfig(xrandr) 
BuildRequires: pkgconfig(xcursor) 
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(libpci)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(libusb)
BuildRequires: pkgconfig(speex)
BuildRequires: perl perl(version) perl(Digest::MD5) perl(Text::ParseWords)
BuildRequires: ruby
BuildRequires: python-devel


#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools-devel
#for absolute path qdoc
BuildRequires: qt5-qtbase-devel


%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtwebengine-opensource-src-%{version}

%build
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


if [ -d "examples/" ]; then
 mkdir -p %{buildroot}%{_libdir}/qt5/examples
 cp -r examples/* %{buildroot}%{_libdir}/qt5/examples/
 rm -rf %{buildroot}%{_libdir}/qt5/examples/*.pro
fi


%files
%{_libdir}/*.so.*
%{_libdir}/qt5/libexec/*
%{_libdir}/qt5/qml/*
%{_libdir}/qt5/plugins/qtwebengine/libffmpegsumo.so
%{_datadir}/qt5/icudtl.dat
%{_datadir}/qt5/qtwebengine_resources*.pak
%{_datadir}/qt5/translations/qtwebengine_locales/

%files devel
%{_libdir}/cmake/*
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/qt5/examples/*
%{_libdir}/qt5/include/*
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_docdir}/qt5/*

%changelog
* Sat Oct 24 2015 builder - 5.5.1-2
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

