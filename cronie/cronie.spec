%bcond_without pam
%bcond_without inotify

Summary:   Cron daemon for executing programs at set times
Name:      cronie
Version:   1.5.0
Release:   2%{?dist}
License:   MIT and BSD and ISC and GPLv2+
Group:     System Environment/Base
URL:       https://fedorahosted.org/cronie
Source0:   https://fedorahosted.org/releases/c/r/cronie/%{name}-%{version}.tar.gz

Requires:  dailyjobs

%if %{with pam}
Requires:      pam >= 1.0.1
Buildrequires: pam-devel >= 1.0.1
%endif

BuildRequires:    systemd
Obsoletes:        %{name}-sysvinit

Requires(post):   coreutils sed
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(post):   systemd

%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is a fork of the original vixie-cron and
has security and configuration enhancements like the ability to use pam and
SELinux.

%package anacron
Summary:   Utility for running regular jobs
Requires:  crontabs
Group:     System Environment/Base
Provides:  dailyjobs
Provides:  anacron = 2.4
Obsoletes: anacron <= 2.3
Requires(post): coreutils
Requires:  %{name} = %{version}-%{release}

%description anacron
Anacron is part of cronie that is used for running jobs with regular
periodicity which do not have exact time of day of execution.

The default settings of anacron execute the daily, weekly, and monthly
jobs, but anacron allows setting arbitrary periodicity of jobs.

Using anacron allows running the periodic jobs even if the system is often
powered off and it also allows randomizing the time of the job execution
for better utilization of resources shared among multiple systems.

%package noanacron
Summary:   Utility for running simple regular jobs in old cron style
Group:     System Environment/Base
Provides:  dailyjobs
Requires:  crontabs
Requires:  %{name} = %{version}-%{release}

%description noanacron
Old style of running {hourly,daily,weekly,monthly}.jobs without anacron. No
extra features.

%prep
%setup -q

%build
%configure \
%if %{with pam}
--with-pam \
%endif
%if %{with inotify}
--with-inotify \
%endif
--enable-anacron \
--enable-pie \
--enable-relro

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT DESTMAN=$RPM_BUILD_ROOT%{_mandir}
mkdir -pm700 $RPM_BUILD_ROOT%{_localstatedir}/spool/cron
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
mkdir -pm755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
%if ! %{with pam}
    rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/crond
%endif
install -m 644 crond.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/crond
touch $RPM_BUILD_ROOT%{_sysconfdir}/cron.deny
install -m 644 contrib/anacrontab $RPM_BUILD_ROOT%{_sysconfdir}/anacrontab
install -c -m755 contrib/0hourly $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/0hourly
mkdir -pm 755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly
install -c -m755 contrib/0anacron $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/0anacron
mkdir -p $RPM_BUILD_ROOT/var/spool/anacron
touch $RPM_BUILD_ROOT/var/spool/anacron/cron.daily
touch $RPM_BUILD_ROOT/var/spool/anacron/cron.weekly
touch $RPM_BUILD_ROOT/var/spool/anacron/cron.monthly

# noanacron package
install -m 644 contrib/dailyjobs $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/dailyjobs

# install systemd initscript
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system/
install -m 644 contrib/cronie.systemd $RPM_BUILD_ROOT/lib/systemd/system/crond.service

%post
# run after an installation
%systemd_post crond.service

%post anacron
[ -e /var/spool/anacron/cron.daily ] || touch /var/spool/anacron/cron.daily
[ -e /var/spool/anacron/cron.weekly ] || touch /var/spool/anacron/cron.weekly
[ -e /var/spool/anacron/cron.monthly ] || touch /var/spool/anacron/cron.monthly

%preun
# run before a package is removed
%systemd_preun crond.service

%postun
# run after a package is removed
%systemd_postun_with_restart crond.service

%triggerun -- cronie-anacron < 1.4.1
# empty /etc/crontab in case there are only old regular jobs
cp -a /etc/crontab /etc/crontab.rpmsave
sed -e '/^01 \* \* \* \* root run-parts \/etc\/cron\.hourly/d'\
  -e '/^02 4 \* \* \* root run-parts \/etc\/cron\.daily/d'\
  -e '/^22 4 \* \* 0 root run-parts \/etc\/cron\.weekly/d'\
  -e '/^42 4 1 \* \* root run-parts \/etc\/cron\.monthly/d' /etc/crontab.rpmsave > /etc/crontab
exit 0

%triggerun -- cronie < 1.4.7-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply crond
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save crond

# The package is allowed to autostart:
/bin/systemctl enable crond.service >/dev/null 2>&1

/sbin/chkconfig --del crond >/dev/null 2>&1 || :
/bin/systemctl try-restart crond.service >/dev/null 2>&1 || :
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%triggerin -- pam, glibc, libselinux
# changes in pam, glibc or libselinux can make crond crash
# when it calls pam
/bin/systemctl try-restart crond.service >/dev/null 2>&1 || :

%files
%doc AUTHORS README ChangeLog
%{!?_licensedir:%global license %%doc}
%license COPYING
%attr(755,root,root) %{_sbindir}/crond
%attr(4755,root,root) %{_bindir}/crontab
%{_mandir}/man8/crond.*
%{_mandir}/man8/cron.*
%{_mandir}/man5/crontab.*
%{_mandir}/man1/crontab.*
%dir %{_localstatedir}/spool/cron
%dir %{_sysconfdir}/cron.d
%if %{with pam}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/crond
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/crond
%config(noreplace) %{_sysconfdir}/cron.deny
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cron.d/0hourly
%attr(0644,root,root) /lib/systemd/system/crond.service

%files anacron
%{_sbindir}/anacron
%attr(0755,root,root) %{_sysconfdir}/cron.hourly/0anacron
%config(noreplace) %{_sysconfdir}/anacrontab
%dir /var/spool/anacron
%ghost %attr(0600,root,root) %verify(not md5 size mtime) /var/spool/anacron/cron.daily
%ghost %attr(0600,root,root) %verify(not md5 size mtime) /var/spool/anacron/cron.weekly
%ghost %attr(0600,root,root) %verify(not md5 size mtime) /var/spool/anacron/cron.monthly
%{_mandir}/man5/anacrontab.*
%{_mandir}/man8/anacron.*

%files noanacron
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cron.d/dailyjobs

%changelog
