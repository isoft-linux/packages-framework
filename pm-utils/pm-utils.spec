# power.d stuff breaks more than it helps, so drop it for now
%bcond_with power_d
%global quirkdbver 20100619
Name: pm-utils
Summary: Power management utilities and scripts
License: GPLv2
Version: 1.4.1
Release: 23
Group:  Framework/Runtime/Utility
URL: http://pm-utils.freedesktop.org
%ifnarch s390 s390x
Requires: kbd
%if %{with power_d}
# power.d/disable_wol
Requires: ethtool
# power.d/harddisk
Requires: hdparm
# power.d/wireless
Requires: wireless-tools
%endif
%endif

Source0: http://pm-utils.freedesktop.org/releases/pm-utils-%{version}.tar.gz
Source1: http://pm-utils.freedesktop.org/releases/pm-quirks-%{quirkdbver}.tar.gz

Source23: pm-utils-bugreport-info.sh

# Use append instead of write for init_logfile (#660329)
Patch0: pm-utils-1.4.1-init-logfile-append.patch
# Fix typo in 55NetworkManager (#722759)
Patch1: pm-utils-1.4.1-networkmanager-typo-fix.patch
# Add support for grub2 in 01grub hook
Patch2: pm-utils-1.4.1-grub2.patch
# Fix hooks exit code logging
Patch3: pm-utils-1.4.1-hook-exit-code-log.patch
# Fix line spacing in logs to be easier to read (#750755)
Patch4: pm-utils-1.4.1-log-line-spacing-fix.patch
# Fix NetworkManager dbus methods (fd.o #42500 / RH #740342)
Patch5: pm-utils-1.4.1-nm_method.patch
# Add support for in-kernel (from kernel 3.6) suspend to both (#843657)
Patch6: pm-utils-1.4.1-add-in-kernel-suspend-to-both.patch

%description
The pm-utils package contains utilities and scripts useful for tasks related
to power management.

%package devel
Summary: Files for development using %{name}
Group:  Framework/Development/Library
Requires: %{name} = %{version}-%{release}
# for /usr/share/pkgconfig
Requires:       pkgconfig

%description devel
This package contains the pkg-config files for development
when building programs that use %{name}.

%prep
%setup -q
tar -xzf %{SOURCE1}
%patch0 -p1 -b .init-logfile-append
%patch1 -p1 -b .network-manager-typo-fix.patch
%patch2 -p1 -b .grub2
%patch3 -p1 -b .hook-exit-code-log
%patch4 -p1 -b .log-line-spacing-fix
%patch5 -p1 -b .nm_method
%patch6 -p1 -b .add-in-kernel-suspend-to-both

%build
%configure --docdir=%{_docdir}/%{name}-%{version}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

install -D -m 0600 /dev/null $RPM_BUILD_ROOT%{_localstatedir}/log/pm-suspend.log
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/pm-utils/{locks,pm-suspend,pm-powersave}
touch $RPM_BUILD_ROOT%{_localstatedir}/run/pm-utils/locks/{pm-suspend.lock,pm-powersave.lock}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/pm-utils/{pm-suspend,pm-powersave}/storage
install -D -m 0755 %{SOURCE23} $RPM_BUILD_ROOT%{_sbindir}/pm-utils-bugreport-info.sh

# Install quirks
cp -r video-quirks $RPM_BUILD_ROOT%{_libdir}/pm-utils

%if ! %{with power_d}
rm $RPM_BUILD_ROOT%{_libdir}/pm-utils/power.d/*
%endif

# Install extra documentation
cp -p COPYING AUTHORS ChangeLog $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

%preun
# Clean storage to prevent left-behind files. These files are dynamically
# created in runtime (also with dynamic names), thus it is hard to track
# them individually.
rm -rf %{_localstatedir}/run/pm-utils/{pm-suspend,pm-powersave}/storage/*

%files
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}
%{_libdir}/pm-utils/bin/
%{_libdir}/pm-utils/defaults
%{_libdir}/pm-utils/functions
%{_libdir}/pm-utils/module.d/*
%{_libdir}/pm-utils/pm-functions
%if %{with power_d}
%{_libdir}/pm-utils/power.d/*
%endif
%{_libdir}/pm-utils/sleep.d/*
%{_bindir}/on_ac_power
%{_bindir}/pm-is-supported
%{_sbindir}/pm-utils-bugreport-info.sh
%{_sbindir}/pm-hibernate
%{_sbindir}/pm-powersave
%{_sbindir}/pm-suspend
%{_sbindir}/pm-suspend-hybrid
%ghost %{_localstatedir}/run/pm-utils
%{_libdir}/pm-utils/video-quirks

# no logrotate needed, because only one run of pm-utils is stored
# in the logfile
%ghost %verify(not md5 size mtime) %{_localstatedir}/log/pm-suspend.log
%{_mandir}/man1/on_ac_power.1.gz
%{_mandir}/man1/pm-is-supported.1.gz
%{_mandir}/man8/pm-action.8.gz
%{_mandir}/man8/pm-hibernate.8.gz
%{_mandir}/man8/pm-pmu.8.gz
%{_mandir}/man8/pm-powersave.8.gz
%{_mandir}/man8/pm-suspend-hybrid.8.gz
%{_mandir}/man8/pm-suspend.8.gz


%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/pm-utils.pc

%changelog
