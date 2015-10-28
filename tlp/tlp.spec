Name:           tlp
Version:        0.7
Release:        7%{?dist}
Summary:        Advanced power management tool for Linux
License:        GPLv2+
URL:            http://linrunner.de/tlp
Source0:        https://github.com/linrunner/TLP/archive/%{version}.tar.gz
#Provided by Andreas Roederer <tlp~at~warpnine~dot~de>:
Source1:        50-tlp.preset
BuildRequires:  systemd
#The following requires are not detected:
Requires:       ethtool
Requires:       hdparm
Requires:       iw
Requires:       lsb
Requires:       rfkill
Requires:       systemd
Requires:       udev
Requires:       usbutils
Requires:       pciutils
Requires:       kernel-tools
#Conflicts with laptop-mode-tools, note that an official
#package/package name doesn't exist, so this works for now:
Conflicts:      %{_sbindir}/laptop_mode
BuildArch:      noarch

%description
TLP brings you the benefits of advanced power management for Linux
without the need to understand every technical detail. TLP comes
with a default configuration already optimized for battery life.
Also an optional install of the smartmontools package enables hard
disk SMART data in tlp-stat (smartctl).

%package rdw
Summary:        Radio Device Wizard for TLP
Requires:       NetworkManager
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description rdw
Radio Device Wizard for TLP automatically toggles wireless networking
based on dock events and the Network Manager connection status.

%prep
%setup -q -n TLP-%{version}
#This isn't necessary for fc18+, but it makes things more consistent:
sed -i 's|/lib/udev|/usr/lib/udev|g' tlp*rules Makefile
#Bash completion should be in /usr/share
sed -i 's|etc/bash_completion.d|usr/share/bash-completion/completions|g' Makefile

%build
make

%install
make install DESTDIR=%{buildroot} TLP_NO_INIT=1 \
             TLP_NO_PMUTILS=1
#Install manpages:
mkdir -p %{buildroot}%{_mandir}/{man1,man8}
install -m 0644 man/*.1 %{buildroot}%{_mandir}/man1
install -m 0644 man/*.8 %{buildroot}%{_mandir}/man8
#Install preset (source 1):
install -Dpm 0644 %{SOURCE1} %{buildroot}/%{_presetdir}/50-tlp.preset
#Install systemd services:
install -D -m 644 tlp.service %{buildroot}%{_unitdir}/tlp.service
install -D -m 644 tlp-sleep.service %{buildroot}%{_unitdir}/tlp-sleep.service
#THIS IS A WORKAROUND FOR RFKILL!
ln -sf /dev/null systemd-rfkill@.service
install -D systemd-rfkill@.service %{buildroot}%{_sysconfdir}/systemd/system/systemd-rfkill@.service

%files
%config(noreplace) %{_sysconfdir}/default/tlp
%doc COPYING LICENSE README
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man*/*
%{_prefix}/lib/tlp-pm
%{_udevrulesdir}/85-tlp.rules
%{_udevrulesdir}/../tlp-usb-udev
%{_datadir}/bash-completion/completions/tlp
%{_presetdir}/50-tlp.preset
%{_unitdir}/*.service
#THIS IS A WORKAROUND FOR RFKILL!
%config %{_sysconfdir}/systemd/system/systemd-rfkill@.service
#%exclude %{_sysconfdir}/acpi/events/thinkpad-radiosw
#%exclude %{_sysconfdir}/acpi/thinkpad-radiosw.sh
 
%files rdw
%doc COPYING LICENSE README
%{_sysconfdir}/NetworkManager/dispatcher.d/99tlp-rdw-nm
%{_udevrulesdir}/85-tlp-rdw.rules
%{_udevrulesdir}/../tlp-rdw-udev

%post
%systemd_post tlp.service
%systemd_post tlp-sleep.service

%preun
%systemd_preun tlp.service
%systemd_preun tlp-sleep.service

%postun
%systemd_postun_with_restart tlp.service
%systemd_postun_with_restart tlp-sleep.service

%post rdw
/bin/systemctl enable NetworkManager-dispatcher.service >/dev/null 2>&1 || :

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.7-7
- Rebuild for new 4.0 release.

