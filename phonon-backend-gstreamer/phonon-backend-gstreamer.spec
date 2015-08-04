# enable for snapshots
#global snap 20141025

Summary: Gstreamer phonon backend
Name:    phonon-backend-gstreamer
Epoch:   2
Version: 4.8.2
Release: 3%{?dist}

License: LGPLv2+
URL:     http://phonon.kde.org/
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/phonon/phonon-backend-gstreamer/%{version}/src/phonon-backend-gstreamer-%{version}.tar.xz

Patch0: phonon-gstreamer-add-include-patch.patch


BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-app-1.0) pkgconfig(gstreamer-audio-1.0) pkgconfig(gstreamer-video-1.0)

Requires: gstreamer-plugins-good

BuildRequires: automoc4
BuildRequires: cmake
BuildRequires: pkgconfig(phonon) >= 4.7.80
BuildRequires: pkgconfig(phonon4qt5) >= 4.7.80
BuildRequires: pkgconfig(QtOpenGL)
BuildRequires: pkgconfig(Qt5OpenGL)

%global phonon_version %(pkg-config --modversion phonon 2>/dev/null || echo 4.7.80)

Provides: phonon-backend%{?_isa} = %{phonon_version}

Obsoletes: phonon-backend-gst < 4.2.0-4
Provides:  phonon-backend-gst = %{version}-%{release}

Obsoletes: phonon-gstreamer < 4.4.4-0.2
Provides:  phonon-gstreamer = %{version}-%{release}

# provide upgrade path for deprecated/removed -xine backend
Obsoletes: phonon-backend-xine < 4.5.0

# not *strictly* required, but strongly recommended by upstream when built
# with USE_INSTALL_PLUGIN
#Requires: PackageKit-gstreamer-plugin
Requires: phonon%{?_isa} => %{phonon_version}
Requires: qt4%{?_isa} >= %{_qt4_version}

%description
%{summary}.

%package -n phonon-qt5-backend-gstreamer
Summary:  Gstreamer phonon-qt5 backend
Provides: phonon-qt5-backend%{?_isa} = %{phonon_version}
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}
Requires: gstreamer-plugins-good
%description -n phonon-qt5-backend-gstreamer
%{summary}.


%prep
%setup -q -n phonon-backend-gstreamer-%{version}
%patch0 -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} .. \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DUSE_INSTALL_PLUGIN:BOOL=ON
popd

make %{?_smp_mflags} -C %{_target_platform}

mkdir %{_target_platform}-Qt5
pushd %{_target_platform}-Qt5
%{cmake} .. \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DUSE_INSTALL_PLUGIN:BOOL=ON \
  -D__KDE_HAVE_GCC_VISIBILITY=NO \
  -DPHONON_BUILD_PHONON4QT5:BOOL=ON
popd

make %{?_smp_mflags} -C %{_target_platform}-Qt5


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-Qt5
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:

%files
%doc COPYING.LIB
%{_libdir}/kde4/plugins/phonon_backend/phonon_gstreamer.so
%{_datadir}/kde4/services/phononbackends/gstreamer.desktop
%{_datadir}/icons/hicolor/*/apps/phonon-gstreamer.*

%files -n phonon-qt5-backend-gstreamer
%doc COPYING.LIB
%{_qt5_plugindir}/phonon4qt5_backend/phonon_gstreamer.so


%changelog
