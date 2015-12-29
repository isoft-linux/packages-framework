Name:           pulseaudio
Summary:        Improved Linux Sound Server
Version:        7.1
Release:        4 
License:        LGPLv2+

Source0: http://freedesktop.org/software/pulseaudio/releases/pulseaudio-%{version}.tar.xz
# revert upstream commit to rely solely on autospawn for autostart, instead
# include a fallback to manual launch when autospawn fails, like when
# user disables autospawn, or logging in as root
Patch1: pulseaudio-autostart.patch
Patch2: fix-locale-dir.patch

URL:            http://pulseaudio.org/
BuildRequires:  json-c
BuildRequires:  m4
BuildRequires:  libtool
BuildRequires:  libltdl-devel
BuildRequires:  intltool
BuildRequires:  pkgconfig
BuildRequires:  alsa-lib-devel
BuildRequires:  glib2-devel
BuildRequires:  libXt-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXi-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libICE-devel
BuildRequires:  openssl-devel
BuildRequires:  libudev-devel >= 143
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  xcb-util-devel 
BuildRequires:  sbc-devel 
BuildRequires:  bluez-libs-devel
BuildRequires:  libcap-devel
BuildRequires:  avahi-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libspeex-devel

Obsoletes:      pulseaudio-devel
Obsoletes:      pulseaudio-core-libs
Provides:       pulseaudio-core-libs
Requires:       udev >= 145-3
Requires:	kernel >= 2.6.30
%description
PulseAudio is a sound server for Linux and other Unix like operating
systems. It is intended to be an improved drop-in replacement for the
Enlightened Sound Daemon (ESOUND).

%package esound-compat
Summary:        PulseAudio EsounD daemon compatibility script
Requires:       %{name} = %{version}-%{release}
Provides:       esound
Obsoletes:      esound

%description esound-compat
A compatibility script that allows applications to call /usr/bin/esd
and start PulseAudio with EsounD protocol modules.

%package module-x11
Summary:        X11 support for the PulseAudio sound server
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-utils = %{version}-%{release}

%description module-x11
X11 bell and security modules for the PulseAudio sound server.

%package module-zeroconf
Summary:        Zeroconf support for the PulseAudio sound server
Requires:       %{name} = %{version}-%{release}
Requires:       pulseaudio-utils

%description module-zeroconf
Zeroconf publishing module for the PulseAudio sound server.

%ifnarch s390 s390x
%package module-bluetooth
Summary:        Bluetooth support for the PulseAudio sound server
Requires:       %{name} = %{version}-%{release}
Requires:       bluez >= 5.0 

%description module-bluetooth
Contains Bluetooth audio (A2DP/HSP/HFP) support for the PulseAudio sound server.

Also contains a module that can be used to automatically turn down the volume if
a bluetooth mobile phone leaves the proximity or turn it up again if it enters the
proximity again
%endif


%package libs
Summary:        Libraries for PulseAudio clients
License:        LGPLv2+
Provides:       pulseaudio-lib
Obsoletes:      pulseaudio-lib

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PulseAudio sound server.

%package core-libs
Summary:        Core libraries for the PulseAudio sound server.
License:        LGPLv2+

%description core-libs
This package contains runtime libraries that are used internally in the
PulseAudio sound server.

%package libs-glib2
Summary:        GLIB 2.x bindings for PulseAudio clients
License:        LGPLv2+
Provides:       pulseaudio-lib-glib2
Obsoletes:      pulseaudio-lib-glib2

%description libs-glib2
This package contains bindings to integrate the PulseAudio client library with
a GLIB 2.x based application.

%package libs-zeroconf
Summary:    Zeroconf support for PulseAudio clients
License:        LGPLv2+
Provides:       pulseaudio-lib-zeroconf
Obsoletes:      pulseaudio-lib-zeroconf

%description libs-zeroconf
This package contains the runtime libraries and tools that allow PulseAudio
clients to automatically detect PulseAudio servers using Zeroconf.

%package libs-devel
Summary:        Headers and libraries for PulseAudio client development
License:        LGPLv2+
Requires:       %{name}-libs = %{version}-%{release}
Requires:       %{name}-libs-glib2 = %{version}-%{release}
#Requires:       %{name}-libs-zeroconf = %{version}-%{release}
Requires:   	pkgconfig
Requires:	glib2-devel
#Requires:	vala
Provides:       pulseaudio-lib-devel
Obsoletes:      pulseaudio-lib-devel

%description libs-devel
Headers and libraries for developing applications that can communicate with
a PulseAudio sound server.

%package utils
Summary:        PulseAudio sound server utilities
License:        LGPLv2+
Requires:       %{name}-libs = %{version}-%{release}

%description utils
This package contains command line utilities for the PulseAudio sound server.

%prep
%setup -q

%patch1 -p1 -b .autostart
%patch2 -p1

sed -i.no_consolekit -e \
  's/^load-module module-console-kit/#load-module module-console-kit/' \
  src/daemon/default.pa.in


%build
autoreconf

%configure \
    --disable-static \
    --disable-rpath \
    --with-system-user=pulse \
    --with-system-group=pulse \
    --with-access-group=pulse-access \
    --enable-bluez5 \
    --enable-systemd-daemon \
    --enable-systemd-logind \
    --enable-systemd-journal \
    --enable-samplerate \
    --enable-avahi \
    --enable-orc \
    --enable-openssl \
    --enable-ipv6 \
    --with-speex \
    --disable-hal-compat \
    --disable-tcpwrap \
    --disable-gconf \
    --disable-bluez4 \
    --disable-waveout \
    --disable-gtk3 \
    --disable-jack \
    --disable-asyncns \
    --disable-lirc \
    --disable-hal-compat \
    --without-fftw \
    --with-caps 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Disable cork-request module, can result in e.g. media players unpausing
# when there's a Skype call incoming
sed -e 's|/usr/bin/pactl load-module module-x11-cork-request|#&|' -i %{buildroot}%{_bindir}/start-pulseaudio-x11

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{_libdir}/pulse-%{version}/modules/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a $RPM_BUILD_ROOT%{_libdir}/pulse-%{version}/modules/*.a
rm $RPM_BUILD_ROOT%{_libdir}/pulse-%{version}/modules/module-detect.so

touch -r src/daemon/daemon.conf.in $RPM_BUILD_ROOT%{_sysconfdir}/pulse/daemon.conf
touch -r src/daemon/default.pa.in $RPM_BUILD_ROOT%{_sysconfdir}/pulse/default.pa
touch -r man/pulseaudio.1.xml.in $RPM_BUILD_ROOT%{_mandir}/man1/pulseaudio.1
touch -r man/default.pa.5.xml.in $RPM_BUILD_ROOT%{_mandir}/man5/default.pa.5
touch -r man/pulse-client.conf.5.xml.in $RPM_BUILD_ROOT%{_mandir}/man5/pulse-client.conf.5
touch -r man/pulse-daemon.conf.5.xml.in $RPM_BUILD_ROOT%{_mandir}/man5/pulse-daemon.conf.5
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/pulse

rm -rf $RPM_BUILD_ROOT/%{_libdir}/pulseaudio/*.a
rm -rf $RPM_BUILD_ROOT/%{_libdir}/pulseaudio/*.la

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group pulse-access >/dev/null || groupadd -r pulse-access
getent group pulse-rt >/dev/null || groupadd -r pulse-rt
getent group pulse >/dev/null || groupadd -f -g 171 -r pulse
if ! getent passwd pulse >/dev/null ; then
    if ! getent passwd 171 >/dev/null ; then
      useradd -r -u 171 -g pulse -d /var/run/pulse -s /sbin/nologin -c "PulseAudio System Daemon" pulse
    else
      useradd -r -g pulse -d /var/run/pulse -s /sbin/nologin -c "PulseAudio System Daemon" pulse
    fi
fi
exit 0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post libs-glib2 -p /sbin/ldconfig
%postun libs-glib2 -p /sbin/ldconfig

%post libs-zeroconf -p /sbin/ldconfig
%postun libs-zeroconf -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README LICENSE GPL LGPL
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/pulseaudio-system.conf
%{_bindir}/pulseaudio
%{_libdir}/libpulsecore-%{version}.so
%dir %{_libdir}/pulse-%{version}/
%dir %{_libdir}/pulse-%{version}/modules/
%{_libdir}/pulse-%{version}/modules/libalsa-util.so
%{_libdir}/pulse-%{version}/modules/libcli.so
%{_libdir}/pulse-%{version}/modules/libprotocol-cli.so
%{_libdir}/pulse-%{version}/modules/libprotocol-esound.so
%{_libdir}/pulse-%{version}/modules/libprotocol-http.so
%{_libdir}/pulse-%{version}/modules/libprotocol-native.so
%{_libdir}/pulse-%{version}/modules/libprotocol-simple.so
%{_libdir}/pulse-%{version}/modules/librtp.so
%{_libdir}/pulse-%{version}/modules/module-alsa-sink.so
%{_libdir}/pulse-%{version}/modules/module-alsa-source.so
%{_libdir}/pulse-%{version}/modules/module-alsa-card.so
%{_libdir}/pulse-%{version}/modules/module-cli-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-cli-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-cli.so
%{_libdir}/pulse-%{version}/modules/module-combine.so
%{_libdir}/pulse-%{version}/modules/module-device-manager.so
%{_libdir}/pulse-%{version}/modules/module-loopback.so
%{_libdir}/pulse-%{version}/modules/module-esound-compat-spawnfd.so
%{_libdir}/pulse-%{version}/modules/module-esound-compat-spawnpid.so
%{_libdir}/pulse-%{version}/modules/module-esound-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-esound-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-esound-sink.so
%{_libdir}/pulse-%{version}/modules/module-udev-detect.so
%{_libdir}/pulse-%{version}/modules/module-http-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-http-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-match.so
%{_libdir}/pulse-%{version}/modules/module-mmkbd-evdev.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-fd.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-null-sink.so
%{_libdir}/pulse-%{version}/modules/module-rescue-streams.so
%{_libdir}/pulse-%{version}/modules/module-rtp-recv.so
%{_libdir}/pulse-%{version}/modules/module-rtp-send.so
%{_libdir}/pulse-%{version}/modules/module-simple-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-simple-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-sine.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-sink.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-source.so
%{_libdir}/pulse-%{version}/modules/module-volume-restore.so
%{_libdir}/pulse-%{version}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{version}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{version}/modules/module-device-restore.so
%{_libdir}/pulse-%{version}/modules/module-stream-restore.so
%{_libdir}/pulse-%{version}/modules/module-card-restore.so
%{_libdir}/pulse-%{version}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{version}/modules/module-remap-sink.so
%{_libdir}/pulse-%{version}/modules/module-always-sink.so
%{_libdir}/pulse-%{version}/modules/module-console-kit.so
%{_libdir}/pulse-%{version}/modules/module-position-event-sounds.so
%{_libdir}/pulse-%{version}/modules/module-augment-properties.so
%{_libdir}/pulse-%{version}/modules/module-systemd-login.so
#%{_libdir}/pulse-%{version}/modules/module-cork-music-on-phone.so
%{_libdir}/pulse-%{version}/modules/module-sine-source.so
%{_libdir}/pulse-%{version}/modules/module-intended-roles.so
%{_libdir}/pulse-%{version}/modules/module-rygel-media-server.so
%{_libdir}/pulse-%{version}/modules/module-echo-cancel.so
%{_libdir}/pulse-%{version}/modules/libraop.so
%{_libdir}/pulse-%{version}/modules/module-combine-sink.so
%{_libdir}/pulse-%{version}/modules/module-dbus-protocol.so
%{_libdir}/pulse-%{version}/modules/module-filter-apply.so
%{_libdir}/pulse-%{version}/modules/module-filter-heuristics.so
%{_libdir}/pulse-%{version}/modules/module-null-source.so
%{_libdir}/pulse-%{version}/modules/module-raop-sink.so
%{_libdir}/pulse-%{version}/modules/module-switch-on-connect.so
%{_libdir}/pulse-%{version}/modules/module-virtual-sink.so
%{_libdir}/pulse-%{version}/modules/module-virtual-source.so
%{_libdir}/pulse-%{version}/modules/module-role-cork.so
%{_libdir}/pulse-%{version}/modules/module-switch-on-port-available.so
%{_libdir}/pulse-%{version}/modules/module-virtual-surround-sink.so
#%{_libdir}/pulse-%{version}/modules/module-lirc.so
%{_libdir}/pulse-%{version}/modules/module-remap-source.so
%{_libdir}/pulse-%{version}/modules/module-role-ducking.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-sink-new.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-source-new.so
%{_libdir}/pulse-%{version}/modules/liboss-util.so
%{_libdir}/pulse-%{version}/modules/module-oss.so
%{_libdir}/pulse-%{version}/modules/module-pipe-sink.so
%{_libdir}/pulse-%{version}/modules/module-pipe-source.so

%{_datadir}/pulseaudio/alsa-mixer/paths/*
%{_datadir}/pulseaudio/alsa-mixer/profile-sets/*
%{_mandir}/man1/pulseaudio.1.gz
%{_mandir}/man5/default.pa.5.gz
%{_mandir}/man5/pulse-client.conf.5.gz
%{_mandir}/man5/pulse-daemon.conf.5.gz
/lib/udev/rules.d/90-pulseaudio.rules
#%dir %{_libexecdir}/pulse
%attr(0700, pulse, pulse) %dir %{_localstatedir}/lib/pulse

%{_mandir}/man5/pulse-cli-syntax.5.gz


%{_datadir}/bash-completion/completions/*
%{_libdir}/systemd/user/pulseaudio.service
%{_libdir}/systemd/user/pulseaudio.socket
%{_datadir}/zsh/site-functions/_pulseaudio


%files esound-compat
%defattr(-,root,root)
%{_bindir}/esdcompat
%{_mandir}/man1/esdcompat.1.gz

%files module-x11
%defattr(-,root,root)
%{_sysconfdir}/xdg/autostart/pulseaudio.desktop
%{_bindir}/start-pulseaudio-x11
%{_libdir}/pulse-%{version}/modules/module-x11-bell.so
%{_libdir}/pulse-%{version}/modules/module-x11-publish.so
%{_libdir}/pulse-%{version}/modules/module-x11-xsmp.so
%{_libdir}/pulse-%{version}/modules/module-x11-cork-request.so
%{_mandir}/man1/start-pulseaudio-x11.1.gz

%files module-zeroconf
%defattr(-,root,root)
%{_libdir}/pulse-%{version}/modules/libavahi-wrap.so
%{_libdir}/pulse-%{version}/modules/module-raop-discover.so
%{_libdir}/pulse-%{version}/modules/module-zeroconf-discover.so
%{_libdir}/pulse-%{version}/modules/module-zeroconf-publish.so

%ifnarch s390 s390x
%files module-bluetooth
%defattr(-,root,root)
%{_libdir}/pulse-%{version}/modules/module-bluez5-discover.so
%{_libdir}/pulse-%{version}/modules/module-bluez5-device.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-policy.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-discover.so
%{_libdir}/pulse-%{version}/modules/libbluez5-util.so
#%{_libexecdir}/pulse/proximity-helper
%endif

%files libs -f %{name}.lang
%defattr(-,root,root)
%doc README LICENSE GPL LGPL
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%{_libdir}/libpulse.so.*
#%{_libdir}/libpulsecommon-%{version}.so
%{_libdir}/libpulse-simple.so.*

%{_libdir}/pulseaudio/libpulsecommon-%{version}.so
%{_libdir}/pulseaudio/libpulsedsp.so

%files libs-glib2
%defattr(-,root,root)
%{_libdir}/libpulse-mainloop-glib.so.*

#%files libs-zeroconf
#%defattr(-,root,root)
#%{_bindir}/pabrowse
#%{_libdir}/libpulse-browse.so.*
#%{_mandir}/man1/pabrowse.1.gz

%files libs-devel
%defattr(-,root,root)
%{_includedir}/pulse/
%{_libdir}/libpulse.so
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/libpulse-simple.so
#%{_libdir}/libpulse-browse.so
%{_libdir}/pkgconfig/libpulse*.pc
%{_libdir}/cmake/PulseAudio/*.cmake
%{_datadir}/vala/vapi/*

%files utils
%defattr(-,root,root)
%{_bindir}/pacat
%{_bindir}/pacmd
%{_bindir}/pactl
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/pamon
%{_bindir}/parecord
%{_bindir}/pax11publish
%{_bindir}/padsp
%{_bindir}/pasuspender
#%{_bindir}/qpaeq
#%{_libdir}/libpulsedsp.so
%{_mandir}/man1/pacat.1.gz
%{_mandir}/man1/pacmd.1.gz
%{_mandir}/man1/pactl.1.gz
%{_mandir}/man1/paplay.1.gz
%{_mandir}/man1/pasuspender.1.gz
%{_mandir}/man1/padsp.1.gz
%{_mandir}/man1/pax11publish.1.gz
%{_mandir}/man1/pamon.1.gz
%{_mandir}/man1/parec.1.gz
%{_mandir}/man1/parecord.1.gz


%changelog
* Tue Dec 29 2015 xiaotian.wu@i-soft.com.cn - 7.1-4
- fix path error of locale message mo file.

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 7.0-3
- Rebuild for new 4.0 release.

* Mon Oct 19 2015 Cjacker <cjacker@foxmail.com>
- rebuild.
