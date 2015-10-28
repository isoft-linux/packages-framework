Summary: Collection of performance monitoring tools for Linux
Name: sysstat
Version: 11.1.5
Release: 2%{?dist}
License: GPLv2+
URL: http://sebastien.godard.pagesperso-orange.fr/
Source: http://pagesperso-orange.fr/sebastien.godard/%{name}-%{version}.tar.xz

BuildRequires: gettext, lm_sensors-devel, systemd

Requires: findutils, xz
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The sysstat package contains the sar, sadf, mpstat, iostat, pidstat,
nfsiostat-sysstat, cifsiostat and sa tools for Linux.
The sar command collects and reports system activity information.
The information collected by sar can be saved in a file in a binary
format for future inspection. The statistics reported by sar concern
I/O transfer rates, paging activity, process-related activities,
interrupts, network activity, memory and swap space utilization, CPU
utilization, kernel activities and TTY statistics, among others. Both
UP and SMP machines are fully supported.
The sadf command may  be used to display data collected by sar in
various formats (CSV, XML, etc.).
The iostat command reports CPU utilization and I/O statistics for disks.
The mpstat command reports global and per-processor statistics.
The pidstat command reports statistics for Linux tasks (processes).
The nfsiostat-sysstat command reports I/O statistics for network filesystems.
The cifsiostat command reports I/O statistics for CIFS filesystems.

%prep
%setup -q


%build
#fix lib64 dir issue, we do not like lib64
sed -i 's/lib64/lib/g' configure.in
autoreconf -ivf

%configure --enable-install-cron --enable-copy-only --disable-file-attr \
    --disable-stripping --docdir=%{_pkgdocdir} sadc_options='-S DISK' \
    history=28 compressafter=31
make %{?_smp_mflags}

%install
%make_install
%find_lang %{name}

%post
%systemd_post sysstat.service sysstat-collect.timer sysstat-summary.timer

%preun
%systemd_preun sysstat.service sysstat-collect.timer sysstat-summary.timer
if [[ $1 -eq 0 ]]; then
    # Remove sa logs if removing sysstat completely
    rm -rf %{_localstatedir}/log/sa/*
fi

%postun
%systemd_postun sysstat.service sysstat-collect.timer sysstat-summary.timer

%files -f %{name}.lang
%doc CHANGES COPYING CREDITS FAQ README
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat.ioconf
%{_bindir}/*
%{_libdir}/sa
%{_unitdir}/sysstat*
%{_mandir}/man*/*
%{_localstatedir}/log/sa

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 11.1.5-2
- Rebuild for new 4.0 release.

* Tue Aug 25 2015 Cjacker <cjacker@foxmail.com>
- initial build.
