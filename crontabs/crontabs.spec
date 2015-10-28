%global snap_release 20130830git
Summary: Root crontab files used to schedule the execution of programs
Name: crontabs
Version: 1.11
Release: 11.%{snap_release}%{?dist}
License: Public Domain and GPLv2
URL: https://fedorahosted.org/crontabs 
Source0: https://fedorahosted.org/releases/c/r/crontabs/%{name}-%{version}-1.%{snap_release}.tar.gz
BuildArch: noarch
Requires: /etc/cron.d
Requires: run-parts
%description
This package is used by Fedora mainly for executing files by cron.

The crontabs package contains root crontab files and directories.
You will need to install cron daemon to run the jobs from the crontabs.
The cron daemon such as cronie or fcron checks the crontab files to
see when particular commands are scheduled to be executed.  If commands
are scheduled, it executes them.

Crontabs handles a basic system function, so it should be installed on
your system.

%prep
%setup -q 

%build
#empty

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/cron.{hourly,daily,weekly,monthly}
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man4/

install -m644 ./crontab $RPM_BUILD_ROOT/etc/crontab
#install -m755 ./run-parts $RPM_BUILD_ROOT/usr/bin/run-parts
install -m644 ./{crontabs,run-parts}.4 $RPM_BUILD_ROOT/%{_mandir}/man4/

mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/
touch $RPM_BUILD_ROOT/etc/sysconfig/run-parts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/crontab
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/run-parts
#%{_bindir}/run-parts
%dir /etc/cron.hourly
%dir /etc/cron.daily
%dir /etc/cron.weekly
%dir /etc/cron.monthly
%{_mandir}/man4/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.11-11.20130830git
- Rebuild for new 4.0 release.

