# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python2_sitearch}/.*\.so$
%filter_provides_in %{python3_sitearch}/.*\.so$
%filter_setup
}

%{!?py2dir: %global py2dir python2-%{name}-%{version}-%{release}}

Summary: HP Linux Imaging and Printing Project
Name: hplip
Version: 3.15.6
Release: 4%{?dist}
License: GPLv2+ and MIT

Url: http://hplip.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/hplip/hplip-%{version}.tar.gz
Source1: hpcups-update-ppds.sh
Source2: copy-deviceids.py
Patch1: hplip-pstotiff-is-rubbish.patch
Patch2: hplip-strstr-const.patch
Patch3: hplip-ui-optional.patch
Patch4: hplip-no-asm.patch
Patch5: hplip-deviceIDs-drv.patch
Patch6: hplip-udev-rules.patch
Patch7: hplip-retry-open.patch
Patch8: hplip-snmp-quirks.patch
Patch9: hplip-hpijs-marker-supply.patch
Patch10: hplip-clear-old-state-reasons.patch
Patch11: hplip-hpcups-sigpipe.patch
Patch12: hplip-logdir.patch
Patch13: hplip-bad-low-ink-warning.patch
Patch14: hplip-deviceIDs-ppd.patch
Patch15: hplip-ppd-ImageableArea.patch
Patch16: hplip-scan-tmp.patch
Patch17: hplip-log-stderr.patch
Patch18: hplip-avahi-parsing.patch
Patch20: hplip-dj990c-margin.patch
Patch21: hplip-strncpy.patch
Patch22: hplip-no-write-bytecode.patch
Patch23: hplip-silence-ioerror.patch
Patch24: hp-systray-make-menu-title-visible-in-sni-qt-indicator.dpatch
Patch25: hp-systray-make-menu-appear-in-sni-qt-indicator-with-kde.dpatch
Patch26: process-events-for-systray.patch
 
%global hpijs_epoch 1
Requires: hpijs%{?_isa} = %{hpijs_epoch}:%{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
# due to hp-plugin (BZ#1196237)
Requires: %{name}-compat-libs%{?_isa} = %{version}-%{release}
Requires: python3-pillow
Requires: cups
Requires: wget
Requires: python3-dbus
Requires: gnupg

BuildRequires: net-snmp-devel
BuildRequires: cups-devel
BuildRequires: python3-devel
BuildRequires: libjpeg-devel
BuildRequires: desktop-file-utils
BuildRequires: libusb1-devel
BuildRequires: openssl-devel
BuildRequires: sane-backends-devel
BuildRequires: pkgconfig(dbus-1)

# Make sure we get postscriptdriver tags.
BuildRequires: python3-cups, cups

# macros: %%{_tmpfilesdir}, %%{_udevrulesdir}
BuildRequires: systemd

%description
The Hewlett-Packard Linux Imaging and Printing Project provides
drivers for HP printers and multi-function peripherals.

%package common
Summary: Files needed by the HPLIP printer and scanner drivers
License: GPLv2+
# /usr/lib/udev/rules.d
Requires: systemd

%description common
Files needed by the HPLIP printer and scanner drivers.

%package libs
Summary: HPLIP libraries
License: GPLv2+ and MIT
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Requires: python3

%description libs
Libraries needed by HPLIP.

%package compat-libs
Summary: HPLIP Python 2 modules
License: GPLv2+ and MIT
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Requires: python-pillow
Requires: dbus-python
Requires: python
BuildRequires: python2-devel

%description compat-libs
Python 2 modules needed by HP plugin.

%package gui
Summary: HPLIP graphical tools
License: BSD
Requires: python3-PyQt4
Requires: python3-reportlab
# hpssd.py
Requires: python3-gobject
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libsane-hpaio%{?_isa} = %{version}-%{release}

%description gui
HPLIP graphical tools.

%package -n hpijs
Summary: HP Printer Drivers
License: BSD
Epoch: %{hpijs_epoch}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: cups >= 1:1.4

%description -n hpijs
hpijs is a collection of optimized drivers for HP printers.
hpijs supports the DeskJet 350C, 600C, 600C Photo, 630C, Apollo 2000,
Apollo 2100, Apollo 2560, DeskJet 800C, DeskJet 825, DeskJet 900,
PhotoSmart, DeskJet 990C, and PhotoSmart 100 series.

%package -n libsane-hpaio
Summary: SANE driver for scanners in HP's multi-function devices
License: GPLv2+
Obsoletes: libsane-hpoj < 0.91
Provides: libsane-hpoj = 0.91
Requires: sane-backends
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description -n libsane-hpaio
SANE driver for scanners in HP's multi-function devices (from HPOJ).

%prep
%setup -q

# The pstotiff filter is rubbish so replace it (launchpad #528394).
%patch1 -p1 -b .pstotiff-is-rubbish

# Fix compilation.
%patch2 -p1 -b .strstr-const

# Make utils.checkPyQtImport() look for the gui sub-package (bug #243273).
%patch3 -p1 -b .ui-optional

# Make sure to avoid handwritten asm.
%patch4 -p1 -b .no-asm

# Corrected several IEEE 1284 Device IDs using foomatic data.
# Color LaserJet 2500 series (bug #659040)
# LaserJet 4100 Series/2100 Series (bug #659039)
%patch5 -p1 -b .deviceIDs-drv
chmod +x %{SOURCE2}
mv prnt/drv/hpijs.drv.in{,.deviceIDs-drv-hpijs}
%{SOURCE2} prnt/drv/hpcups.drv.in \
           prnt/drv/hpijs.drv.in.deviceIDs-drv-hpijs \
           > prnt/drv/hpijs.drv.in

# Don't add printer queue, just check plugin.
# Move udev rules from /etc/ to /usr/lib/ (bug #748208).
%patch6 -p1 -b .udev-rules

# Retry when connecting to device fails (bug #532112).
%patch7 -p1 -b .retry-open

# Mark SNMP quirks in PPD for HP OfficeJet Pro 8500 (bug #581825).
%patch8 -p1 -b .snmp-quirks

# Fixed bogus low ink warnings from hpijs driver (bug #643643).
%patch9 -p1 -b .hpijs-marker-supply

# Clear old printer-state-reasons we used to manage (bug #510926).
%patch10 -p1 -b .clear-old-state-reasons

# Avoid busy loop in hpcups when backend has exited (bug #525944).
%patch11 -p1 -b .hpcups-sigpipe

# CUPS filters should use TMPDIR when available (bug #865603).
%patch12 -p1 -b .logdir

# Fixed Device ID parsing code in hpijs's dj9xxvip.c (bug #510926).
%patch13 -p1 -b .bad-low-ink-warning

# Add Device ID for
# HP LaserJet Color M451dn (bug #1159380)
for ppd_file in $(grep '^diff' %{PATCH14} | cut -d " " -f 4);
do
  gunzip ${ppd_file#*/}.gz
done
%patch14 -p1 -b .deviceIDs-ppd
for ppd_file in $(grep '^diff' %{PATCH14} | cut -d " " -f 4);
do
  gzip -n ${ppd_file#*/}
done

# Fix ImageableArea for Laserjet 8150/9000 (bug #596298).
for ppd_file in $(grep '^diff' %{PATCH15} | cut -d " " -f 4);
do
  gunzip ${ppd_file#*/}.gz
done
%patch15 -p1 -b .ImageableArea
for ppd_file in $(grep '^diff' %{PATCH15} | cut -d " " -f 4);
do
  gzip -n ${ppd_file#*/}
done

# Scan to /var/tmp instead of /tmp (bug #1076954).
%patch16 -p1 -b .scan-tmp

# Treat logging before importing of logger module (bug #984699).
%patch17 -p1 -b .log-stderr

# Fix parsing of avahi-daemon output (bug #1096939).
%patch18 -p1 -b .parsing

# Fixed left/right margins for HP DeskJet 990C (LP #1405212).
%patch20 -p1 -b .dj990c-margin

# Fixed uses of strncpy throughout.
%patch21 -p1 -b .strncpy

# Don't try to write bytecode cache for hpfax backend (bug #1192761).
%patch22 -p1 -b .no-write-bytecode

# Ignore IOError when logging output (bug #712537).
%patch23 -p1 -b .silence-ioerror

%patch24 -p1
%patch25 -p1
%patch26 -p1

sed -i.duplex-constraints \
    -e 's,\(UIConstraints.* \*Duplex\),//\1,' \
    prnt/drv/hpcups.drv.in

# Change shebang /usr/bin/env python -> /usr/bin/python3 (bug #618351).
find -name '*.py' -print0 | xargs -0 \
    sed -i.env-python -e 's,^#!/usr/bin/env python,#!%{__python3},'
sed -i.env-python -e 's,^#!/usr/bin/env python,#!%{__python3},' \
    prnt/filters/hpps \
    fax/filters/pstotiff

# compat-libs
rm -rf ../%{py2dir}
cp -a . ../%{py2dir}


%build
# compat-libs
pushd ../%{py2dir}
%configure PYTHON=%{__python2}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make libhpmud.la hpmudext.la libhpipp.la cupsext.la pcardext.la scanext.la
popd

%configure \
        --enable-scan-build --enable-gui-build --enable-fax-build \
        --disable-foomatic-rip-hplip-install --enable-pp-build \
        --enable-qt4 --enable-hpcups-install --enable-cups-drv-install \
        --enable-foomatic-drv-install \
        --enable-hpijs-install \
        --disable-policykit --with-mimedir=%{_datadir}/cups/mime PYTHON=%{__python3}

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
# compat-libs
pushd ../%{py2dir}
make install-libLTLIBRARIES \
     install-hpmudextLTLIBRARIES \
     install-cupsextLTLIBRARIES \
     install-pcardextLTLIBRARIES \
     install-scanextLTLIBRARIES \
     DESTDIR=%{buildroot} PYTHON=%{__python2}
rm -f %{buildroot}%{python2_sitearch}/*.la
popd


mkdir -p %{buildroot}%{_bindir}
make install DESTDIR=%{buildroot} PYTHON=%{__python3}

# Create /run/hplip
mkdir -p %{buildroot}/run/hplip

# install /usr/lib/tmpfiles.d/hplip.conf (bug #1015831)
mkdir -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/hplip.conf <<EOF
# See tmpfiles.d(5) for details

d /run/hplip 0775 root lp -
EOF


# Remove unpackaged files
rm -rf  %{buildroot}%{_sysconfdir}/sane.d \
        %{buildroot}%{_docdir} \
        %{buildroot}%{_datadir}/hal/fdi \
        %{buildroot}%{_datadir}/hplip/pkservice.py \
        %{buildroot}%{_bindir}/hp-pkservice

rm -f   %{buildroot}%{_bindir}/hp-logcapture \
        %{buildroot}%{_bindir}/hp-doctor \
        %{buildroot}%{_datadir}/hplip/logcapture.py \
        %{buildroot}%{_datadir}/hplip/doctor.py

rm -f   %{buildroot}%{_bindir}/foomatic-rip \
        %{buildroot}%{_libdir}/cups/filter/foomatic-rip \
        %{buildroot}%{_libdir}/*.la \
        %{buildroot}%{python3_sitearch}/*.la \
        %{buildroot}%{_libdir}/libhpip.so \
        %{buildroot}%{_libdir}/libhpipp.so \
        %{buildroot}%{_libdir}/sane/*.la \
        %{buildroot}%{_datadir}/cups/model/foomatic-ppds \
        %{buildroot}%{_datadir}/applications/hplip.desktop \
        %{buildroot}%{_datadir}/ppd/HP/*.ppd

mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e '/^Categories=/d' hplip.desktop
# Encoding key is deprecated
sed -i -e '/^Encoding=/d' hplip.desktop

#Hide menu item by default. 
echo "NoDisplay=true" >> hplip.desktop

desktop-file-install --vendor HP                                \
        --dir %{buildroot}%{_datadir}/applications              \
        --add-category System                                   \
        --add-category Settings                                 \
        --add-category HardwareSettings                         \
        hplip.desktop

# Regenerate hpcups PPDs on upgrade if necessary (bug #579355).
install -p -m755 %{SOURCE1} %{buildroot}%{_bindir}/hpcups-update-ppds

%{__mkdir_p} %{buildroot}%{_sysconfdir}/sane.d/dll.d
echo hpaio > %{buildroot}%{_sysconfdir}/sane.d/dll.d/hpaio

# Images in docdir should not be executable (bug #440552).
find doc/images -type f -exec chmod 644 {} \;

# Create an empty plugins directory to make sure it gets the right
# SELinux file context (bug #564551).
%{__mkdir_p} %{buildroot}%{_datadir}/hplip/prnt/plugins

# Remove files we don't want to package.
rm -f %{buildroot}%{_datadir}/hplip/hpaio.desc
rm -f %{buildroot}%{_datadir}/hplip/hplip-install
rm -rf %{buildroot}%{_datadir}/hplip/install.*
rm -f %{buildroot}%{_datadir}/hplip/uninstall.*
rm -f %{buildroot}%{_bindir}/hp-uninstall
rm -f %{buildroot}%{_datadir}/hplip/upgrade.*
rm -f %{buildroot}%{_bindir}/hp-upgrade
rm -f %{buildroot}%{_bindir}/hp-config_usb_printer
rm -f %{buildroot}%{_unitdir}/hplip-printer@.service
rm -f %{buildroot}%{_datadir}/hplip/config_usb_printer.*
rm -f %{buildroot}%{_datadir}/hplip/hpijs.drv.in.template
rm -f %{buildroot}%{_datadir}/cups/mime/pstotiff.types
rm -f %{buildroot}%{_datadir}/hplip/fax/pstotiff*

# The systray applet doesn't work properly (displays icon as a
# window), so don't ship the launcher yet.
rm -f %{buildroot}%{_sysconfdir}/xdg/autostart/hplip-systray.desktop

# Sort out which PPDs go into which subpackage.
# The ones that use hpps have to go into the main package (bug #1194186).
find %{buildroot}%{_datadir}/ppd -type f | \
    (while read fname
     do
         if zgrep -q '^\*cupsFilter.* hpps' "$fname"
         then
	     which=0
         else
	     which=1
         fi
         printf "$which %s\n" "$fname"
     done) > ppds-all
sed -ne "s,^0 %{buildroot},,p" ppds-all > ppds-hpps
sed -ne "s,^1 %{buildroot},,p" ppds-all > ppds-nohpps
rm -f ppds-all

%files -f ppds-hpps
%doc COPYING doc/*
%{_bindir}/hp-align
%{_bindir}/hp-clean
%{_bindir}/hp-colorcal
%{_bindir}/hp-devicesettings
%{_bindir}/hp-diagnose_plugin
%{_bindir}/hp-diagnose_queues
%{_bindir}/hp-fab
%{_bindir}/hp-faxsetup
%{_bindir}/hp-firmware
%{_bindir}/hp-info
%{_bindir}/hp-levels
%{_bindir}/hp-linefeedcal
%{_bindir}/hp-makecopies
%{_bindir}/hp-makeuri
%{_bindir}/hp-plugin
%{_bindir}/hp-pqdiag
%{_bindir}/hp-printsettings
%{_bindir}/hp-probe
%{_bindir}/hp-query
%{_bindir}/hp-scan
%{_bindir}/hp-sendfax
%{_bindir}/hp-setup
%{_bindir}/hp-testpage
%{_bindir}/hp-timedate
%{_bindir}/hp-unload
%{_bindir}/hp-wificonfig
%{_cups_serverbin}/backend/hp
%{_cups_serverbin}/backend/hpfax
%{_cups_serverbin}/filter/hpps
%{_cups_serverbin}/filter/pstotiff
%{_datadir}/cups/mime/pstotiff.convs
# Files
%{_datadir}/hplip/align.py*
%{_datadir}/hplip/check-plugin.py*
%{_datadir}/hplip/clean.py*
%{_datadir}/hplip/colorcal.py*
%{_datadir}/hplip/devicesettings.py*
%{_datadir}/hplip/diagnose_plugin.py*
%{_datadir}/hplip/diagnose_queues.py*
%{_datadir}/hplip/fab.py*
%{_datadir}/hplip/fax
%{_datadir}/hplip/faxsetup.py*
%{_datadir}/hplip/firmware.py*
%{_datadir}/hplip/hpdio.py*
%{_datadir}/hplip/hplip_clean.sh
%{_datadir}/hplip/hpssd*
%{_datadir}/hplip/info.py*
%{_datadir}/hplip/__init__.py*
%{_datadir}/hplip/levels.py*
%{_datadir}/hplip/linefeedcal.py*
%{_datadir}/hplip/makecopies.py*
%{_datadir}/hplip/makeuri.py*
%{_datadir}/hplip/plugin.py*
%{_datadir}/hplip/pqdiag.py*
%{_datadir}/hplip/printsettings.py*
%{_datadir}/hplip/probe.py*
%{_datadir}/hplip/query.py*
%{_datadir}/hplip/scan.py*
%{_datadir}/hplip/sendfax.py*
%{_datadir}/hplip/setup.py*
%{_datadir}/hplip/testpage.py*
%{_datadir}/hplip/timedate.py*
%{_datadir}/hplip/unload.py*
%{_datadir}/hplip/wificonfig.py*
# Directories
%{_datadir}/hplip/base
%{_datadir}/hplip/copier
%{_datadir}/hplip/data/ldl
%{_datadir}/hplip/data/localization
%{_datadir}/hplip/data/pcl
%{_datadir}/hplip/data/ps
%{_datadir}/hplip/installer
%{_datadir}/hplip/pcard
%{_datadir}/hplip/prnt
%{_datadir}/hplip/scan
%{_localstatedir}/lib/hp
%dir %attr(0775,root,lp) /run/hplip
%{_tmpfilesdir}/hplip.conf

%files common
%doc COPYING
%{_udevrulesdir}/*.rules
%dir %{_sysconfdir}/hp
%config(noreplace) %{_sysconfdir}/hp/hplip.conf
%dir %{_datadir}/hplip
%dir %{_datadir}/hplip/data
%{_datadir}/hplip/data/models

%files libs
%{_libdir}/libhpip.so.*
%{_libdir}/libhpipp.so.*
# The so symlink is required here (see bug #489059).
%{_libdir}/libhpmud.so*
# Python extension
%{python3_sitearch}/*

%files compat-libs
# Python extensions
%{python2_sitearch}/*.so

%files gui
%{_bindir}/hp-check
%{_bindir}/hp-print
%{_bindir}/hp-systray
%{_bindir}/hp-toolbox
%{_datadir}/applications/*.desktop
# Files
%{_datadir}/hplip/check.py*
%{_datadir}/hplip/print.py*
%{_datadir}/hplip/systray.py*
%{_datadir}/hplip/toolbox.py*
# Directories
%{_datadir}/hplip/data/images
%{_datadir}/hplip/ui4

%files -n hpijs -f ppds-nohpps
%{_bindir}/hpijs
%{_bindir}/hpcups-update-ppds
%dir %{_datadir}/ppd/HP
%{_datadir}/cups/drv/*
%{_cups_serverbin}/filter/hpcups
%{_cups_serverbin}/filter/hpcupsfax

%files -n libsane-hpaio
%{_libdir}/sane/libsane-*.so*
%config(noreplace) %{_sysconfdir}/sane.d/dll.d/hpaio

%post -n hpijs
%{_bindir}/hpcups-update-ppds &>/dev/null ||:

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.15.6-4
- Rebuild for new 4.0 release.

