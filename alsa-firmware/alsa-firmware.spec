# This is a firmware package, so binaries (which are not run on the host)
# in the end package are expected.
%define _binaries_in_noarch_packages_terminate_build   0

Summary:        Firmware for several ALSA-supported sound cards
Name:           alsa-firmware
Version:        1.0.29
Release:        2%{?dist}
# See later in the spec for a breakdown of licensing
License:        GPL+ and BSD and GPLv2+ and GPLv2 and LGPLv2+
Group:          Applications/Multimedia
URL:            http://www.alsa-project.org/
Source:         ftp://ftp.alsa-project.org/pub/firmware/%{name}-%{version}.tar.bz2

Requires:       alsa-tools-firmware >= %{version}
Requires:       systemd
BuildRequires:  libtool autoconf automake

# noarch, since the package is firmware
BuildArch:      noarch

%description
This package contains the firmware binaries for a number of sound cards.
Some (but not all of these) require firmware loaders which are included in
the alsa-tools-firmware package.


%prep
%setup -q


%build

# Leaving this directory in place ends up with the following crazy, broken
# symlinks in the output RPM, with no sign of the actual firmware (*.bin) files
# themselves:
#
# /lib/firmware/turtlebeach:
# msndinit.bin -> /etc/sound/msndinit.bin
# msndperm.bin -> /etc/sound/msndperm.bin
# pndsperm.bin -> /etc/sound/pndsperm.bin
# pndspini.bin -> /etc/sound/pndspini.bin
#
# Probably an upstream package bug.
sed -i s#'multisound/Makefile \\'## configure.ac
sed -i s#multisound## Makefile.am

autoreconf -vif
%configure --disable-loader
make %{?_smp_mflags}

# Rename README files from firmware subdirs that have them
for i in hdsploader mixartloader pcxhrloader usx2yloader vxloader ca0132
do
  mv ${i}/README README.${i}
done
mv aica/license.txt LICENSE.aica_firmware
mv aica/Dreamcast_sound.txt aica_dreamcast_sound.txt
mv ca0132/creative.txt LICENSE.creative_txt

%install
make install DESTDIR=%{buildroot}


rm -rf %{buildroot}/lib/firmware/ess/maestro3_assp_kernel.fw
rm -rf %{buildroot}/lib/firmware/ess/maestro3_assp_minisrc.fw
rm -rf %{buildroot}/lib/firmware/korg/k1212.dsp
rm -rf %{buildroot}/lib/firmware/yamaha/ds1_ctrl.fw
rm -rf %{buildroot}/lib/firmware/yamaha/ds1_dsp.fw
rm -rf %{buildroot}/lib/firmware/yamaha/ds1e_ctrl.fw

%files
%doc COPYING README* LICENSE*
%doc aica_dreamcast_sound.txt

# License: KOS (BSD-alike)
/lib/firmware/aica_firmware.bin

# License: No explicit license; default package license is GPLv2+
/lib/firmware/asihpi

# License: GPL (undefined version)
/lib/firmware/digiface_firmware*

%dir /lib/firmware/ea
# The licenses for the Echo Audio firmware vary slightly so each is enumerated
# separately, to be really sure.
# LGPLv2.1+
/lib/firmware/ea/3g_asic.fw
# GPL (undefined version)
/lib/firmware/ea/darla20_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/darla24_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/echo3g_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina20_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_301_asic.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_301_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_361_asic.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_361_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_dj_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_djx_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_io_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_iox_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/layla20_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla20_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_1_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_2A_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_2S_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/loader_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/mia_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/mona_2_asic.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_1_asic_48.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_1_asic_96.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_1_asic_48.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_1_asic_96.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_dsp.fw

%dir /lib/firmware/emu
# Licenses vary so are enumerated separately
# GPLv2
/lib/firmware/emu/audio_dock.fw
# GPLv2
/lib/firmware/emu/emu0404.fw
# GPLv2
/lib/firmware/emu/emu1010_notebook.fw
# GPLv2
/lib/firmware/emu/emu1010b.fw
# GPLv2
/lib/firmware/emu/hana.fw
# GPLv2+
/lib/firmware/emu/micro_dock.fw

# License: GPL (undefined version)
/lib/firmware/ess

# License: No explicit license; default package license is GPLv2+
/lib/firmware/korg

# License: GPL (undefined version)
/lib/firmware/mixart

# License: GPL (undefined version)
/lib/firmware/multiface_firmware*

# License: GPL (undefined version)
/lib/firmware/pcxhr

# License: GPL (undefined version)
/lib/firmware/rpm_firmware.bin

# License: GPLv2+
/lib/firmware/sb16

# License: GPL (undefined version)
/lib/firmware/vx

# License: No explicit license; default package license is GPLv2+
# See ALSA bug #3412
/lib/firmware/yamaha

# Licence: Redistribution allowed, see ca0132/creative.txt
/lib/firmware/ctefx.bin
/lib/firmware/ctspeq.bin

# Licence: No explicit license; says it's copied from kernel where the cs46xx
# driver is labelled as GPLv2+
/lib/firmware/cs46xx

# Even with --disable-loader, we still get usxxx firmware here; looking at the
# alsa-tools-firmware package, it seems like these devices probably use an old- 
# style hotplug loading method
# License: GPL (undefined version)
%{_datadir}/alsa/firmware


%changelog
