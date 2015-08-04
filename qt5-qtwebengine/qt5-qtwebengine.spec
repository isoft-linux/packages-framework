Name:	    qt5-qtwebengine	
Version:	5.5.0
Release:	1
Summary:    QtWebengine Component of Qt

Group:	    Extra/Runtime/Utility
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qtwebengine-opensource-src-%{version}.tar.xz	

BuildRequires:  qt5-qtbase-devel
BuildRequires:  libX11-devel libXrandr-devel libXtst-devel libXcursor-devel
BuildRequires:  alsa-lib-devel at-spi2-core-devel cups-devel bluez-libs-devel
BuildRequires:  fontconfig-devel geoclue-devel gstreamer-plugins-base-devel
BuildRequires:  gtk2-devel harfbuzz-devel 
BuildRequires:  mesa-libGL-devel
BuildRequires:  ruby 
BuildRequires:  nss-devel
BuildRequires:  mtdev-devel
BuildRequires:  libxcb-devel
BuildRequires:  libmng-devel

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires:  qt5-qttools
#for absolute path qdoc
BuildRequires:  qt5-qtbase


%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Extra/Development/Library
Requires:       %{name} = %{version}-%{release}

%description    devel
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
%{_datadir}/qt5/qtwebengine_resources.pak
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
