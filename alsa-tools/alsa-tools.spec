# If you want to skip building the firmware subpackage, define the macro
# _without_firmware to 1. This is not the actual firmware itself 
# (see alsa-firmware), it is some complementary tools.
# Do *NOT* set it to zero or have a commented out define here, or it will not
# work. (RPM spec file voodoo)
%global _without_tools 1 	

%ifarch ppc ppc64
# sb16_csp doesn't build on PPC; see bug #219010
%{?!_without_tools:     %global builddirstools as10k1 echomixer envy24control hdspconf hdspmixer hwmixvolume rmedigicontrol sbiload sscape_ctl us428control hda-verb hdajackretask }
%else
%{?!_without_tools:     %global builddirstools as10k1 echomixer envy24control hdspconf hdspmixer hwmixvolume rmedigicontrol sbiload sb16_csp sscape_ctl us428control hda-verb hdajackretask }
%endif

%{?!_without_firmware:  %global builddirsfirmw hdsploader mixartloader usx2yloader vxloader }

%{?!_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# Note that the Version is intended to coincide with the version of ALSA
# included with the Fedora kernel, rather than necessarily the very latest
# upstream version of alsa-tools

Summary:        Specialist tools for ALSA
Name:           alsa-tools
Version:        1.1.0
Release:        2%{?dist}

# Checked at least one source file from all the sub-projects contained in
# the source tarball and they are consistent GPLv2+ - TJ 2007-11-15
License:        GPLv2+
URL:            http://www.alsa-project.org/
Source:		ftp://ftp.alsa-project.org/pub/tools/%{name}-%{version}.tar.bz2

# The icons below were created by Tim Jackson from screenshots of the
# apps in question. They suck, a lot. Better alternatives welcome!
Source1:        envy24control.desktop
Source2:        envy24control.png
Source3:        echomixer.desktop
Source4:        echomixer.png
Source5:        90-alsa-tools-firmware.rules
# Resized version of public domain clipart found here:
# http://www.openclipart.org/detail/17428
Source6:        hwmixvolume.png
Source7:        hwmixvolume.desktop
Source9:        hdajackretask.desktop

BuildRequires:  alsa-lib-devel >= %{version}
%if 0%{!?_without_tools:1}
BuildRequires:  gtk+-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  fltk-devel
Buildrequires:  desktop-file-utils
Requires:       xorg-x11-fonts-misc
# Needed for hwmixvolume
Requires:       python-alsa
%endif

%description
This package contains several specialist tools for use with ALSA, including
a number of programs that provide access to special hardware facilities on
certain sound cards.

* as10k1 - AS10k1 Assembler
%ifnarch ppc ppc64
* cspctl - Sound Blaster 16 ASP/CSP control program
%endif
* echomixer - Mixer for Echo Audio (indigo) devices
* envy24control - Control tool for Envy24 (ice1712) based soundcards
* hdspmixer - Mixer for the RME Hammerfall DSP cards
* hwmixvolume - Control the volume of individual streams on sound cards that
  use hardware mixing
* rmedigicontrol - Control panel for RME Hammerfall cards
* sbiload - An OPL2/3 FM instrument loader for ALSA sequencer
* sscape_ctl - ALSA SoundScape control utility
* us428control - Control tool for Tascam 428
* hda-verb - Direct HDA codec access
* hdajackretask - Reassign the I/O jacks on the HDA hardware


%package firmware
Summary:        ALSA tools for uploading firmware to some soundcards
Requires:       udev
Requires:       alsa-firmware
Requires:       fxload


%description firmware
This package contains tools for flashing firmware into certain sound cards.
The following tools are available:

* hdsploader   - for RME Hammerfall DSP cards
* mixartloader - for Digigram miXart soundcards
* vxloader     - for Digigram VX soundcards
* usx2yloader  - second phase firmware loader for Tascam USX2Y USB soundcards


%prep
%setup -q -n %{name}-%{version}

%build
mv seq/sbiload . ; rm -rf seq
for i in %{?builddirstools:%builddirstools} %{?builddirsfirmw:%builddirsfirmw}
do
  cd $i ; %configure
  make %{?_smp_mflags} || exit 1
  cd ..
done


%install
mkdir -p %{buildroot}%{_datadir}/{pixmaps,applications}

for i in %{?builddirstools:%builddirstools} %{?builddirsfirmw:%builddirsfirmw}
do
  case $i in
    echomixer)
      (cd $i ; %make_install ; install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/pixmaps/ ; install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/applications/ ) || exit 1
      ;;
    envy24control)
      (cd $i ; %make_install ; install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/ ; install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/ ) || exit 1
      ;;
    hdspconf)
      (cd $i ; %make_install ) || exit 1
      ;;
    hdspmixer)
      (cd $i ; %make_install ) || exit 1
      ;;
    hwmixvolume)
      (cd $i ; %make_install ; install -m 644 %{SOURCE6} %{buildroot}%{_datadir}/pixmaps/ ; install -m 644 %{SOURCE7} %{buildroot}%{_datadir}/applications/ ) || exit 1
      ;;
    usx2yloader)
      (cd $i ; %make_install hotplugdir=/lib/udev) || exit 1
      ;;
    hdajackretask)
      (cd $i ; %make_install ; install -m 644 %{SOURCE9} %{buildroot}%{_datadir}/applications/ ) || exit 1
      ;;
    *) (cd $i ; %make_install) || exit 1
   esac
   if [[ -s "${i}"/README ]]
   then
      if [[ ! -d "%{buildroot}%{_pkgdocdir}/${i}" ]]
      then
         mkdir -p "%{buildroot}%{_pkgdocdir}/${i}"
      fi
      cp "${i}"/README "%{buildroot}%{_pkgdocdir}/${i}"
   fi
   if [[ -s "${i}"/COPYING ]]
   then
      if [[ ! -d "%{buildroot}%{_pkgdocdir}/${i}" ]]
      then
         mkdir -p "%{buildroot}%{_pkgdocdir}/${i}"
      fi
      cp "${i}"/COPYING "%{buildroot}%{_pkgdocdir}/${i}"
   fi
   if [[ -s %{buildroot}%{_datadir}/applications/${i}.desktop ]] ; then
      desktop-file-install --dir %{buildroot}%{_datadir}/applications \
        %{buildroot}%{_datadir}/applications/${i}.desktop
   fi
done

# Merge applications into one software center item
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/echomixer.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<component type="desktop">
  <metadata_license>CC0-1.0</metadata_license>
  <id>echomixer.desktop</id>
  <metadata>
    <value key="X-Merge-With-Parent">hwmixvolume.desktop</value>
  </metadata>
</component>
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/envy24control.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<component type="desktop">
  <metadata_license>CC0-1.0</metadata_license>
  <id>envy24control.desktop</id>
  <metadata>
    <value key="X-Merge-With-Parent">hwmixvolume.desktop</value>
  </metadata>
</component>
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/hdspconf.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<component type="desktop">
  <metadata_license>CC0-1.0</metadata_license>
  <id>hdspconf.desktop</id>
  <metadata>
    <value key="X-Merge-With-Parent">hwmixvolume.desktop</value>
  </metadata>
</component>
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/hdspmixer.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<component type="desktop">
  <metadata_license>CC0-1.0</metadata_license>
  <id>hdspmixer.desktop</id>
  <metadata>
    <value key="X-Merge-With-Parent">hwmixvolume.desktop</value>
  </metadata>
</component>
EOF

# convert hotplug stuff to udev
rm -f %{buildroot}/lib/udev/tascam_fw.usermap
mkdir -p %{buildroot}/lib/udev/rules.d
install -m 644 %{SOURCE5} %{buildroot}/lib/udev/rules.d

%if 0%{!?_without_tools:1}
%files
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/as10k1
%doc %{_pkgdocdir}/echomixer
%doc %{_pkgdocdir}/envy24control
%doc %{_pkgdocdir}/hdspconf
%doc %{_pkgdocdir}/hdspmixer
%doc %{_pkgdocdir}/hwmixvolume
%doc %{_pkgdocdir}/rmedigicontrol
%doc %{_pkgdocdir}/sbiload
%doc %{_pkgdocdir}/hda-verb
%doc %{_pkgdocdir}/hdajackretask
%{_bindir}/as10k1
%{_bindir}/echomixer
%{_bindir}/envy24control
%{_bindir}/hdspconf
%{_bindir}/hdspmixer
%{_bindir}/hwmixvolume
%{_bindir}/rmedigicontrol
%{_bindir}/sbiload
%{_bindir}/sscape_ctl
%{_bindir}/us428control
%{_bindir}/hda-verb
%{_bindir}/hdajackretask
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/echomixer.desktop
%{_datadir}/applications/envy24control.desktop
%{_datadir}/applications/hdspconf.desktop
%{_datadir}/applications/hdspmixer.desktop
%{_datadir}/applications/hwmixvolume.desktop
%{_datadir}/applications/hdajackretask.desktop
%{_datadir}/man/man1/envy24control.1.gz
%{_datadir}/pixmaps/echomixer.png
%{_datadir}/pixmaps/envy24control.png
%{_datadir}/pixmaps/hdspconf.png
%{_datadir}/pixmaps/hdspmixer.png
%{_datadir}/pixmaps/hwmixvolume.png
%{_datadir}/sounds/*

# sb16_csp stuff which is excluded for PPCx
%ifnarch ppc ppc64
%doc %{_pkgdocdir}/sb16_csp
%{_bindir}/cspctl
%{_datadir}/man/man1/cspctl.1.gz
%endif

%endif

%if 0%{!?_without_firmware:1}
%files firmware
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/hdsploader
%doc %{_pkgdocdir}/mixartloader
%doc %{_pkgdocdir}/usx2yloader
%doc %{_pkgdocdir}/vxloader
/lib/udev/rules.d/*.rules
/lib/udev/tascam_fpga
/lib/udev/tascam_fw
%{_bindir}/hdsploader
%{_bindir}/mixartloader
%{_bindir}/usx2yloader
%{_bindir}/vxloader
%endif

%changelog
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 1.1.0-2
- Update to 1.1.0

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.29-5
- Rebuild for new 4.0 release.

