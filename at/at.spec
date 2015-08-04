%bcond_without pam

Summary:	Job spooling tools
Name:		at
Version:	3.1.16
Release:	6
License:	GPLv3+ and GPLv2+ and ISC and MIT and Public Domain
Group:		System Environment/Daemons
URL:		http://ftp.debian.org/debian/pool/main/a/at

Source:		http://ftp.debian.org/debian/pool/main/a/at/at_%{version}.orig.tar.gz

# git upstream source git://git.debian.org/git/collab-maint/at.git
Source1:	pam_atd
Source3:	atd.sysconf
Source5:	atd.systemd

Patch0:		at-aarch64.patch
Patch1:		at-3.1.14-makefile.patch
Patch2:		at-3.1.14-pam.patch
Patch3:		at-3.1.14-selinux.patch
Patch4:		at-3.1.14-opt_V.patch
Patch5:		at-3.1.14-shell.patch
Patch6:		at-3.1.14-nitpicks.patch
Patch8:		at-3.1.14-fix_no_export.patch 
Patch9:		at-3.1.14-mailwithhostname.patch
Patch10:	at-3.1.14-usePOSIXtimers.patch
Patch12:	at-3.1.14-wrong_format.patch
Patch13:	at-3.1.16-noabort.patch
Patch14:	at-3.1.16-fclose-error.patch

BuildRequires: fileutils
BuildRequires: flex bison autoconf
BuildRequires: perl(Test::Harness)
BuildRequires: perl(Test::More)

%if %{with pam}
BuildRequires: pam-devel
%endif
Conflicts: crontabs <= 1.5
# No, I'm not kidding
BuildRequires: smtpdaemon

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

# at-sysvinit subpackage dropped
Obsoletes: at-sysvinit < 3.1.16-1

%description
At and batch read commands from standard input or from a specified
file. At allows you to specify that a command will be run at a
particular time. Batch will execute commands when the system load
levels drop to a particular level. Both commands use user's shell.

You should install the at package if you need a utility for
time-oriented job control. Note: If it is a recurring job that will
need to be repeated at the same time every day/week, etc. you should
use crontab instead.

%prep
%setup -q
cp %{SOURCE1} .
%patch0 -p1 -b .arm
%patch1 -p1 -b .make
%patch2 -p1 -b .pam
#%patch3 -p1 -b .selinux
%patch4 -p1 -b .opt_V
%patch5 -p1 -b .shell
%patch6 -p1 -b .nit
%patch8 -p1 -b .export
%patch9 -p1 -b .mail
%patch10 -p1 -b .posix
%patch12 -p1 -b .wrong
#%patch13 -p1 -b .noabort
%patch14 -p1 -b .fclose

%build
# patch9 touches configure.in
autoconf
# uselles files
rm -f lex.yy.* y.tab.*
%configure --with-atspool=%{_localstatedir}/spool/at/spool \
	--with-jobdir=%{_localstatedir}/spool/at \
	--with-daemon_username=root  \
	--with-daemon_groupname=root \
	--without-selinux \
%if %{with pam}
	--with-pam
%endif

make

%install
make install \
	DAEMON_USERNAME=`id -nu`\
	DAEMON_GROUPNAME=`id -ng` \
	DESTDIR=%{buildroot}\
	sbindir=%{buildroot}%{_prefix}/sbin\
	bindir=%{buildroot}%{_bindir}\
	prefix=%{buildroot}%{_prefix}\
	exec_prefix=%{buildroot}%{_prefix}\
	docdir=%{buildroot}/usr/doc\
	mandir=%{buildroot}%{_mandir}\
	etcdir=%{buildroot}%{_sysconfdir} \
	ATJOB_DIR=%{buildroot}%{_localstatedir}/spool/at \
	ATSPOOL_DIR=%{buildroot}%{_localstatedir}/spool/at/spool \
	INSTALL_ROOT_USER=`id -nu` \
	INSTALL_ROOT_GROUP=`id -nu`;

echo > %{buildroot}%{_sysconfdir}/at.deny
mkdir docs
cp  %{buildroot}/%{_prefix}/doc/at/* docs/

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/atd

mkdir -p %{buildroot}/etc/sysconfig
install -m 644 %{SOURCE3} %{buildroot}/etc/sysconfig/atd

# install systemd initscript
mkdir -p %{buildroot}/%{_unitdir}/
install -m 644 %{SOURCE5} %{buildroot}/%{_unitdir}/atd.service

# remove unpackaged files from the buildroot
rm -r  %{buildroot}%{_prefix}/doc

%check
make test

%post
touch %{_localstatedir}/spool/at/.SEQ
chmod 600 %{_localstatedir}/spool/at/.SEQ
chown daemon:daemon %{_localstatedir}/spool/at/.SEQ
%systemd_post atd.service

%preun
%systemd_preun atd.service

%postun
%systemd_postun_with_restart atd.service

%triggerun -- at < 3.1.12-6
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply atd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save atd

# The package is allowed to autostart:
/bin/systemctl enable atd.service >/dev/null 2>&1

/sbin/chkconfig --del atd >/dev/null 2>&1 || :
/bin/systemctl try-restart atd.service >/dev/null 2>&1 || :
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%doc docs/*
%attr(0644,root,root)		%config(noreplace) %{_sysconfdir}/at.deny
%attr(0644,root,root)		%config(noreplace) %{_sysconfdir}/sysconfig/atd
%attr(0700,daemon,daemon)	%dir %{_localstatedir}/spool/at
%attr(0600,daemon,daemon)	%verify(not md5 size mtime) %ghost %{_localstatedir}/spool/at/.SEQ
%attr(0700,daemon,daemon)	%dir %{_localstatedir}/spool/at/spool
%attr(0644,root,root)		%config(noreplace) %{_sysconfdir}/pam.d/atd
%{_sbindir}/atrun
%attr(0755,root,root)		%{_sbindir}/atd
%{_mandir}/man*/*
%{_bindir}/batch
%{_bindir}/atrm
%{_bindir}/atq
%attr(4755,root,root)		%{_bindir}/at
%attr(0644,root,root)		/%{_unitdir}/atd.service

%changelog
