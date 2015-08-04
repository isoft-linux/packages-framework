%define with_jack 0

Name:           alsa-plugins
Version:        1.0.29
Release:        2
Summary:        The Advanced Linux Sound Architecture (ALSA) Plugins
# All packages are LGPLv2+ with the exception of samplerate which is GPLv2+
# pph plugin is BSD-like licensed
License:        GPLv2+ and LGPLv2+ and BSD
Group:          System Environment/Libraries
URL:            http://www.alsa-project.org/
Source0:        ftp://ftp.alsa-project.org/pub/plugins/%{name}-%{version}.tar.bz2
Source1:        50-jack.conf
Source2:        50-pcm-oss.conf
Source3:        10-speex.conf
Source4:        10-samplerate.conf
Source5:        50-upmix.conf
Source6:        97-vdownmix.conf
Source8:        50-arcamav.conf
Source9:        98-maemo.conf

BuildRequires:  alsa-lib-devel

%description
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.

This package includes plugins for ALSA.

%if 0%{?with_jack}
%package jack
Requires:       alsa-utils
Requires:       jack-audio-connection-kit
BuildRequires:  jack-audio-connection-kit-devel
Summary:        Jack PCM output plugin for ALSA
Group:          System Environment/Libraries
License:        LGPLv2+
%description jack
This plugin converts the ALSA API over JACK (Jack Audio Connection
Kit, http://jackit.sf.net) API.  ALSA native applications can work
transparently together with jackd for both playback and capture.
This plugin provides the PCM type "jack"
%endif

%package oss
Requires:       alsa-utils
BuildRequires:  alsa-lib-devel
Summary:        Oss PCM output plugin for ALSA
Group:          System Environment/Libraries
License:        LGPLv2+ 
%description oss
This plugin converts the ALSA API over OSS API.  With this plugin,
ALSA native apps can run on OSS drivers.

This plugin provides the PCM type "oss".

%package pulseaudio
Requires:       alsa-utils
Requires:       pulseaudio
BuildRequires:  pulseaudio-libs-devel
Summary:        Alsa to PulseAudio backend
Group:          System Environment/Libraries
License:        LGPLv2+
%description pulseaudio
This plugin allows any program that uses the ALSA API to access a PulseAudio
sound daemon. In other words, native ALSA applications can play and record
sound across a network. There are two plugins in the suite, one for PCM and
one for mixer control.

%package samplerate
Requires:       alsa-utils
BuildRequires:  libsamplerate-devel
Summary:        External rate converter plugin for ALSA
Group:          System Environment/Libraries
License:        GPLv2+
%description samplerate
This plugin is an external rate converter using libsamplerate by Erik de
Castro Lopo.

%package upmix
Requires:       alsa-utils
BuildRequires:  libsamplerate-devel
Summary:        Upmixer channel expander plugin for ALSA
Group:          System Environment/Libraries
License:        LGPLv2+
%description upmix
The upmix plugin is an easy-to-use plugin for upmixing to 4 or
6-channel stream.  The number of channels to be expanded is determined
by the slave PCM or explicitly via channel option.

%package vdownmix
Requires:       alsa-utils
BuildRequires:  libsamplerate-devel
Summary:        Downmixer to stereo plugin for ALSA
Group:          System Environment/Libraries
License:        LGPLv2+
%description vdownmix
The vdownmix plugin is a downmixer from 4-6 channels to 2-channel
stereo headphone output.  This plugin processes the input signals with
a simple spacialization, so the output sounds like a kind of "virtual
surround".

%package usbstream
Summary:        USB stream plugin for ALSA
Group:          System Environment/Libraries
License:        LGPLv2+
%description usbstream
The usbstream plugin is for snd-usb-us122l driver. It converts PCM
stream to USB specific stream.

%package arcamav
Summary:        Arcam AV amplifier plugin for ALSA
Group:          System Environment/Libraries
License:        LGPLv2+
%description arcamav
This plugin exposes the controls for an Arcam AV amplifier
(see: http://www.arcam.co.uk/) as an ALSA mixer device.

%package speex
Requires:       libspeex libspeexdsp
BuildRequires:  libspeex-devel libspeexdsp-devel
Summary:        Rate Converter Plugin Using Speex Resampler
Group:          System Environment/Libraries
License:        LGPLv2+
%description speex
The rate plugin is an external rate converter using the Speex resampler
(aka Public Parrot Hack) by Jean-Marc Valin. The pcm plugin provides
pre-processing of a mono stream like denoise using libspeex DSP API.

%package maemo
#BuildRequires:  alsa-lib-devel = %{version}
BuildRequires:  dbus-devel
Summary:        Maemo plugin for ALSA
Group:          System Environment/Libraries
License:        LGPLv2+
%description maemo
This plugin converts the ALSA API over PCM task nodes protocol. In this way,
ALSA native applications can run over DSP Gateway and use DSP PCM task nodes.

%prep
%setup -q -n %{name}-%{version}%{?prever}

%build
%configure --disable-static \
           --with-speex=lib \
           --enable-maemo-plugin \
           --enable-maemo-resource-manager
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

install -d ${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d
%if 0%{?with_jack}
install -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d
%endif
install -m 644 %SOURCE2 \
               %SOURCE3 \
               %SOURCE4 \
               %SOURCE5 \
               %SOURCE6 \
               %SOURCE8 \
               %SOURCE9 \
               ${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d
mv ${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d/99-pulseaudio-default.conf.example \
	${RPM_BUILD_ROOT}%{_datadir}/alsa/alsa.conf.d/99-pulseaudio-default.conf

find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if 0%{?with_jack}
%files jack
%doc COPYING COPYING.GPL doc/README-jack
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-jack.conf
%{_libdir}/alsa-lib/libasound_module_pcm_jack.so
%endif

%files oss
%doc COPYING COPYING.GPL doc/README-pcm-oss
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-pcm-oss.conf
%{_libdir}/alsa-lib/libasound_module_ctl_oss.so
%{_libdir}/alsa-lib/libasound_module_pcm_oss.so

%files pulseaudio
%doc COPYING COPYING.GPL doc/README-pulse
%{_libdir}/alsa-lib/libasound_module_pcm_pulse.so
%{_libdir}/alsa-lib/libasound_module_ctl_pulse.so
%{_libdir}/alsa-lib/libasound_module_conf_pulse.so
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-pulseaudio.conf
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/99-pulseaudio-default.conf

%files samplerate
%doc COPYING COPYING.GPL doc/samplerate.txt
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/10-samplerate.conf
%{_libdir}/alsa-lib/libasound_module_rate_samplerate.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_best.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_linear.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_medium.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_order.so

%files upmix
%doc COPYING COPYING.GPL doc/upmix.txt
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-upmix.conf
%{_libdir}/alsa-lib/libasound_module_pcm_upmix.so

%files vdownmix
%doc COPYING COPYING.GPL doc/vdownmix.txt
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/97-vdownmix.conf
%{_libdir}/alsa-lib/libasound_module_pcm_vdownmix.so

%files usbstream
%doc COPYING COPYING.GPL
%{_libdir}/alsa-lib/libasound_module_pcm_usb_stream.so

%files arcamav
%doc COPYING COPYING.GPL doc/README-arcam-av
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/50-arcamav.conf
%{_libdir}/alsa-lib/libasound_module_ctl_arcam_av.so

%files speex
%doc COPYING COPYING.GPL doc/speexdsp.txt doc/speexrate.txt
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/10-speex.conf
%{_libdir}/alsa-lib/libasound_module_pcm_speex.so
%{_libdir}/alsa-lib/libasound_module_rate_speexrate.so
%{_libdir}/alsa-lib/libasound_module_rate_speexrate_best.so
%{_libdir}/alsa-lib/libasound_module_rate_speexrate_medium.so

%files maemo
%doc COPYING COPYING.GPL doc/README-maemo
%dir %{_datadir}/alsa/alsa.conf.d
%config(noreplace) %{_datadir}/alsa/alsa.conf.d/98-maemo.conf
%{_libdir}/alsa-lib/libasound_module_ctl_dsp_ctl.so
%{_libdir}/alsa-lib/libasound_module_pcm_alsa_dsp.so


%changelog
