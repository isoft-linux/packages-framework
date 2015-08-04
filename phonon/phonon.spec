%define zeitgeist 0

Summary: Multimedia framework api
Name:    phonon
Version: 4.8.3
Release: 4%{?dist}
License: LGPLv2+
URL:     http://phonon.kde.org/
%if 0%{?snap}
Source0: phonon-%{version}-%{snap}.tar.xz
%else
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/phonon/%{version}/src/phonon-%{version}.tar.xz
%endif

Patch0: phonon-4.7.0-rpath_use_link_path.patch 

## upstream patches

BuildRequires: automoc4 >= 0.9.86
BuildRequires: cmake >= 2.6.9
BuildRequires: pkgconfig
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libpulse-mainloop-glib) > 0.9.15
BuildRequires: pkgconfig(libxml-2.0)
# Qt4
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtDesigner) pkgconfig(QtOpenGL) pkgconfig(QtDeclarative) 
# Qt5
BuildRequires: pkgconfig(Qt5DBus) pkgconfig(Qt5Designer) pkgconfig(Qt5OpenGL) pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Declarative)
%if 0%{?zeitgeist}
BuildRequires: pkgconfig(QZeitgeist)
%endif
BuildRequires: pkgconfig(xcb)

%global pulseaudio_version %((pkg-config --modversion libpulse 2>/dev/null || echo 0.9.15) | cut -d- -f1)

%if 0%{?bootstrap}
Provides: phonon-backend%{?_isa} = 4.7
%else
Requires: phonon-backend%{?_isa} => 4.7
%endif
Requires: pulseaudio-libs%{?_isa} >= %{pulseaudio_version}
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

Provides:  phonon-experimental = %{version}-%{release}

%description
%{summary}.

%package devel
Summary: Developer files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides:  phonon-experimental-devel = %{version}-%{release}
%description devel
%{summary}.

%package qt5 
Summary: phonon for Qt5
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}
%if 0%{?bootstrap}
Provides: %{name}-qt5-backend%{?_isa} = 4.7
%else
Requires: %{name}-qt5-backend%{?_isa} => 4.7
%endif
%description qt5 
%{summary}.

%package qt5-devel
Summary: Developer files for %{name}-qt5 
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
%description qt5-devel
%{summary}.


%prep
%setup -q 

%patch0 -p1 -b .rpath_use_link_path

sed -i "s:BSD_SOURCE:DEFAULT_SOURCE:g" cmake/FindPhononInternal.cmake


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} .. \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DPHONON_INSTALL_QT_COMPAT_HEADERS:BOOL=ON \
  -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT:BOOL=ON
popd

make %{?_smp_mflags} -C %{_target_platform}

mkdir %{_target_platform}-Qt5
pushd %{_target_platform}-Qt5
%{cmake} .. \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DPHONON_BUILD_PHONON4QT5:BOOL=ON \
  -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT:BOOL=ON \
  -D__KDE_HAVE_GCC_VISIBILITY=NO 
popd

make %{?_smp_mflags} -C %{_target_platform}-Qt5


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-Qt5
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# own these dirs
mkdir -p %{buildroot}%{_libdir}/kde4/plugins/phonon_backend/
mkdir -p %{buildroot}%{_datadir}/kde4/services/phononbackends/
mkdir -p %{buildroot}%{_qt5_plugindir}/phonon4qt5_backend

#for qt4, dirty hack
#install headers into the Qt4 dir, for example, PyQt4 will need it.
install -d %{buildroot}%{_qt4_headerdir}/phonon
cp -r %{buildroot}%{_includedir}/phonon/* %{buildroot}%{_qt4_headerdir}/phonon/
#sed -i 's#includedir=/usr/include#includedir=/usr/lib/qt4/include#' %{buildroot}%{_libdir}/pkgconfig/phonon.pc

%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion phonon)" = "%{version}"
test "$(pkg-config --modversion phonon4qt5)" = "%{version}"


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LIB
%{_libdir}/libphonon.so.4*
%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
%{_qt4_plugindir}/designer/libphononwidgets.so
%dir %{_datadir}/phonon/
%dir %{_libdir}/kde4/plugins/phonon_backend/
%dir %{_datadir}/kde4/services/phononbackends/

%if 0%{?experimental}
%post experimental -p /sbin/ldconfig
%postun experimental -p /sbin/ldconfig

%files experimental
%endif
%{_libdir}/libphononexperimental.so.4*

%files devel
%{_datadir}/phonon/buildsystem/
%dir %{_libdir}/cmake/
%{_libdir}/cmake/phonon/
%dir %{_includedir}/KDE
%{_includedir}/KDE/Phonon/
%{_includedir}/phonon/
%{_qt4_headerdir}/phonon/*

%{_libdir}/pkgconfig/phonon.pc
%{_libdir}/libphonon.so
%{_qt4_datadir}/mkspecs/modules/qt_phonon.pri

%if 0%{?experimental}
%exclude %{_includedir}/KDE/Phonon/Experimental/
%exclude %{_includedir}/phonon/experimental/
%files experimental-devel
%{_includedir}/KDE/Phonon/Experimental/
%{_includedir}/phonon/experimental/
%endif
%{_libdir}/libphononexperimental.so

%post qt5 -p /sbin/ldconfig
%postun qt5 -p /sbin/ldconfig

%files qt5 
%doc COPYING.LIB
%dir %{_datadir}/phonon4qt5
%{_libdir}/libphonon4qt5.so.4*
%{_libdir}/libphonon4qt5experimental.so.4*
%{_qt5_plugindir}/designer/libphononwidgets.so
%dir %{_qt5_plugindir}/phonon4qt5_backend/
%{_datadir}/dbus-1/interfaces/org.kde.Phonon4Qt5.AudioOutput.xml

%files qt5-devel
%{_datadir}/phonon4qt5/buildsystem/
%dir %{_libdir}/cmake/
%{_libdir}/cmake/phonon4qt5/
%{_includedir}/phonon4qt5/
%{_libdir}/libphonon4qt5.so
%{_libdir}/libphonon4qt5experimental.so
%{_libdir}/pkgconfig/phonon4qt5.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_phonon4qt5.pri


%changelog
