Summary: Utility to set the date and time via NTP
Name: ntpdate
Version: 4.2.6p5
Release: 32%{?dist}
License: (MIT and BSD and BSD with advertising) and GPLv2
URL: http://www.ntp.org
Source0: http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/ntp-%{version}.tar.gz
#manpage
Source1: ntpdate.8

BuildRequires: libcap-devel openssl-devel libedit-devel
BuildRequires: bison

%description
The Network Time Protocol (NTP) is used to synchronize a computer's
time with another reference time source. This package includes ntpd
(a daemon which continuously adjusts system time) and utilities used
to query and configure the ntpd daemon.

Perl scripts ntp-wait and ntptrace are in the ntp-perl package,
ntpdate is in the ntpdate package and sntp is in the sntp package.
The documentation is in the ntp-doc package.

ntpdate is a program for retrieving the date and time from
NTP servers.

%prep
%setup -q -n ntp-%{version}
%build
sed -i 's|$CFLAGS -Wstrict-overflow|$CFLAGS|' configure sntp/configure
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fno-strict-overflow"
%configure

pushd ntpdate
make %{?_smp_mflags}
popd

%install
pushd ntpdate
make DESTDIR=$RPM_BUILD_ROOT bindir=%{_sbindir} install
popd

#install manpage
install -D -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man8/ntpdate.8

%files
%{_sbindir}/ntpdate
%{_mandir}/man8/ntpdate.8*

%changelog
* Fri Aug 14 2015 Cjacker <cjacker@foxmail.com>
- initial build.
- only ship ntpdate utility.

