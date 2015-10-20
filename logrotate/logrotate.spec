Summary: Rotates, compresses, removes and mails system log files
Name: logrotate
Version: 3.9.1
Release: 3%{?dist}
License: GPL+
Url: https://fedorahosted.org/logrotate/
Source: https://fedorahosted.org/releases/l/o/logrotate/logrotate-%{version}.tar.gz
Source1: rwtab
# Change the location of status file
Patch0: logrotate-3.9.1-statusfile.patch

# Daily rotate and keep one week for desktop
Patch1: logrotate-for-desktop.patch

Requires: coreutils >= 5.92 popt
BuildRequires: popt-devel libacl-devel acl
BuildRequires: autoconf automake libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  Logrotate
allows for the automatic rotation compression, removal and mailing of
log files.  Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.  Normally,
logrotate runs as a daily cron job.

Install the logrotate package if you need a utility to deal with the
log files on your system.

%prep
%setup -q
%patch0 -p1 -b .statusfile
%patch1 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"

./autogen.sh
%configure
make %{?_smp_mflags}

%check
make test

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/logrotate

install -p -m 644 examples/logrotate-default $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.conf
install -p -m 755 examples/logrotate.cron $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily/logrotate
touch $RPM_BUILD_ROOT/%{_localstatedir}/lib/logrotate/logrotate.status

# Make sure logrotate is able to run on read-only root
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rwtab.d
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/logrotate

%pre
# If /var/lib/logrotate/logrotate.status does not exist, create it and copy
# the /var/lib/logrotate.status in it (if it exists). We have to do that in pre
# script, otherwise the /var/lib/logrotate/logrotate.status would not be there,
# because during the update, it is removed/renamed.
if [ ! -d %{_localstatedir}/lib/logrotate/ -a -f %{_localstatedir}/lib/logrotate.status ]; then
  mkdir -p %{_localstatedir}/lib/logrotate
  cp -a %{_localstatedir}/lib/logrotate.status %{_localstatedir}/lib/logrotate
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc CHANGES
%attr(0755, root, root) %{_sbindir}/logrotate
%attr(0644, root, root) %{_mandir}/man8/logrotate.8*
%attr(0644, root, root) %{_mandir}/man5/logrotate.conf.5*
%attr(0755, root, root) %{_sysconfdir}/cron.daily/logrotate
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/logrotate.conf
%attr(0755, root, root) %dir %{_sysconfdir}/logrotate.d
%attr(0644, root, root) %verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/logrotate/logrotate.status
%config(noreplace) %{_sysconfdir}/rwtab.d/logrotate

%changelog
* Thu Oct 15 2015 Cjacker <cjacker@foxmail.com>
- add patch to enable daily rotate and keep logs one week for Desktop.
