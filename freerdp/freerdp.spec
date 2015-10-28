# https://fedoraproject.org/wiki/Packaging:SourceURL#Github
%global commit 24a752a70840f3e4b027ba7c020af71f2bcfd94a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           freerdp
Version:        1.2.0
Release:        0.10%{?shortcommit:.git.%{shortcommit}}%{?dist}
Epoch:          2
Summary:        Free implementation of the Remote Desktop Protocol (RDP)

License:        ASL 2.0
URL:            http://www.freerdp.com/
# VCS: git:https://github.com/FreeRDP/Remmina.git
Source0:        https://github.com/FreeRDP/FreeRDP/archive/%{commit}/FreeRDP-%{commit}.tar.gz
Patch0:         freerdp-aarch64.patch
# https://github.com/FreeRDP/FreeRDP/commit/1b663ceffe51008af7ae9749e5b7999b2f7d6698
Patch1:         freerdp-cmake-list.patch
# https://github.com/FreeRDP/FreeRDP/pull/2310
Patch2:         freerdp-args.patch
# We have to stick at commit 24a752a for now to stop breaking guacamole etc.,
# and these are assorted shadow fixes from later.
Patch3:         freerdp-fixes-since-24a752a.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  cmake >= 2.8
BuildRequires:  cups-devel
BuildRequires:  gsm-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  openssl-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  pcsc-lite-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  xmlto
BuildRequires:  zlib-devel

Provides:       xfreerdp = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}

%description
The xfreerdp Remote Desktop Protocol (RDP) client from the FreeRDP project.

xfreerdp can connect to RDP servers such as Microsoft Windows machines, xrdp and
VirtualBox.

%package        libs
Summary:        Core libraries implementing the RDP protocol
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-plugins < 1:1.1.0
Provides:       %{name}-plugins = %{?epoch}:%{version}-%{release}
%description    libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 2.8

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}-libs.

%package        server
Summary:        Server support for %{name}

%description    server
The %{name}-server package contains servers which can export a desktop via
the RDP protocol.

%package -n     libwinpr
Summary:        Windows Portable Runtime
Provides:       %{name}-libwinpr = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-libwinpr < %{?epoch}:%{version}-%{release}

%description -n libwinpr
WinPR provides API compatibility for applications targeting non-Windows
environments. When on Windows, the original native API is being used instead of
the equivalent WinPR implementation, without having to modify the code using it.

%package -n     libwinpr-devel
Summary:        Windows Portable Runtime development files
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 2.8

%description -n libwinpr-devel
The %{name}-libwinpr-devel package contains libraries and header files for
developing applications that use %{name}-libwinpr.

%prep
%setup -qn FreeRDP-%{commit}
%patch0 -p1 -b .aarch64
%patch1 -p1 -b .cmake-list
%patch2 -p1 -b .args
%patch3 -p1 -b .fixes

# Rpmlint fixes
find . -name "*.h" -exec chmod 664 {} \;

%build
%cmake %{?_cmake_skip_rpath} \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
    -DWITH_ALSA=ON \
    -DWITH_CUPS=ON \
    -DWITH_CHANNELS=ON -DSTATIC_CHANNELS=OFF \
    -DWITH_DIRECTFB=OFF \
    -DWITH_FFMPEG=OFF \
    -DWITH_GSM=ON \
    -DWITH_GSTREAMER_1_0=ON \
    -DWITH_IPP=OFF \
    -DWITH_JPEG=ON \
    -DWITH_OPENSSL=ON \
    -DWITH_PCSC=ON \
    -DWITH_PULSE=ON \
    -DWITH_SERVER=ON \
    -DWITH_WAYLAND=OFF \
    -DWITH_X11=ON \
    -DWITH_XCURSOR=ON \
    -DWITH_XEXT=ON \
    -DWITH_XKBFILE=ON \
    -DWITH_XI=ON \
    -DWITH_XINERAMA=ON \
    -DWITH_XRENDER=ON \
    -DWITH_XV=ON \
    -DWITH_ZLIB=ON \
%ifarch x86_64
    -DWITH_SSE2=ON \
%else
    -DWITH_SSE2=OFF \
%endif
%ifarch armv7hl
    -DARM_FP_ABI=hard \
    -DWITH_NEON=OFF \
%endif
%ifarch armv7hnl
    -DARM_FP_ABI=hard \
    -DWITH_NEON=ON \
%endif
%ifarch armv5tel armv6l armv7l
    -DARM_FP_ABI=soft \
    -DWITH_NEON=OFF \
%endif
%ifarch aarch64
    -DWITH_SSE2=OFF \
%endif
    .

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

find %{buildroot} -name "*.a" -delete

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post -n libwinpr -p /sbin/ldconfig

%postun -n libwinpr -p /sbin/ldconfig

%files
%{_bindir}/xfreerdp
%{_mandir}/man1/xfreerdp.*

%files libs
%doc LICENSE README ChangeLog
%{_libdir}/%{name}/
%{_libdir}/lib%{name}*.so.*
%{_libdir}/libx%{name}*.so.*
%{_libdir}/librdtk.so.*

%files devel
%{_libdir}/cmake/FreeRDP
%{_libdir}/cmake/RdTk
%{_includedir}/%{name}
%{_includedir}/rdtk
%{_libdir}/lib%{name}*.so
%{_libdir}/libx%{name}*.so
%{_libdir}/librdtk.so
%{_libdir}/pkgconfig/%{name}.pc

%files server
%{_bindir}/freerdp-shadow

%files -n libwinpr
%doc LICENSE README ChangeLog
%{_libdir}/libwinpr*.so.*

%files -n libwinpr-devel
%{_libdir}/cmake/WinPR
%{_includedir}/winpr
%{_libdir}/libwinpr*.so
%{_libdir}/pkgconfig/winpr.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2:1.2.0-0.10.git.24a752a
- Rebuild for new 4.0 release.

