%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog
%define rsyslog_docdir %{_docdir}/rsyslog

Summary: Enhanced system logging and kernel message trapping daemon
Name: rsyslog
Version: 8.14.0
Release: 2%{?dist}
License: (GPLv3+ and ASL 2.0)
URL: http://www.rsyslog.com/
Source0: http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1: http://www.rsyslog.com/files/download/rsyslog/%{name}-doc-%{version}.tar.gz
Source2: rsyslog.conf
Source3: rsyslog.sysconfig
Source4: rsyslog.log
# tweak the upstream service file to honour configuration from /etc/sysconfig/rsyslog
Patch0: rsyslog-8.8.0-sd-service.patch
# prevent modification of trusted properties (proposed upstream)
Patch1: rsyslog-8.8.0-immutable-json-props.patch

BuildRequires: bison
BuildRequires: dos2unix
BuildRequires: flex
BuildRequires: json-c-devel
BuildRequires: libestr-devel >= 0.1.9
BuildRequires: liblogging-stdlog-devel
BuildRequires: libuuid-devel
BuildRequires: pkgconfig
BuildRequires: python-docutils
# make sure systemd version as we needed
BuildRequires: systemd-devel >= 204-8
BuildRequires: zlib-devel

Requires: logrotate >= 3.5.2
Requires: bash >= 2.0
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Provides: syslog
Obsoletes: sysklogd < 1.5-11

%description
Rsyslog is an enhanced, multi-threaded syslog daemon. It supports MySQL,
syslog/TCP, RFC 3195, permitted sender lists, filtering on any message part,
and fine grain output format control. It is compatible with stock sysklogd
and can be used as a drop-in replacement. Rsyslog is simple to set up, with
advanced features suitable for enterprise-class, encryption-protected syslog
relay chains.


%prep
# set up rsyslog-doc sources
%setup -q -a 1 -T -c
rm -r LICENSE README.md build.sh source build/objects.inv
mv build doc
# set up rsyslog sources
%setup -q -D
%patch0 -p1
%patch1 -p1

%build
%ifarch sparc64
#sparc64 need big PIE
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DPATH_PIDFILE=\\\"/var/run/syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DPATH_PIDFILE=\\\"/var/run/syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

%configure \
	--prefix=/usr \
	--disable-static \
	--disable-elasticsearch \
	--disable-gnutls \
	--disable-gssapi-krb5 \
	--disable-imdiag \
	--enable-imfile \
	--enable-imjournal \
	--disable-impstats \
	--disable-imptcp \
	--disable-libdbi \
	--disable-mail \
	--disable-mmanon \
	--disable-mmaudit \
	--disable-mmcount \
	--disable-mmjsonparse \
	--disable-mmnormalize \
	--disable-mmsnmptrapd \
	--disable-mysql \
	--disable-omhiredis \
	--enable-omjournal \
	--disable-ommongodb \
	--enable-omprog \
	--disable-omrabbitmq \
	--enable-omstdout \
	--disable-omudpspoof \
	--disable-omuxsock \
	--disable-pgsql \
	--enable-pmaixforwardedfrom \
	--enable-pmcisconames \
	--enable-pmlastmsg \
	--enable-pmrfc3164sd \
	--enable-pmsnare \
	--disable-relp \
	--disable-snmp \
	--disable-testbench \
        --disable-libgcrypt \
	--enable-unlimited-select \
	--enable-usertools \

make V=1

# small portion of the test suite seems to be consistently failing (this is more severe on arm*)
# there are also some random failures (~1 test out of the whole batch) on i686 and x86_64
# thus the test suite is disabled for now until these issues are sorted out
%check
%if 0
make V=1 check
%endif

%install
make V=1 DESTDIR=%{buildroot} install

install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -d -m 755 %{buildroot}%{_sysconfdir}/rsyslog.d
install -d -m 700 %{buildroot}%{rsyslog_statedir}
install -d -m 700 %{buildroot}%{rsyslog_pkidir}
install -d -m 755 %{buildroot}%{rsyslog_docdir}/html

install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rsyslog.conf
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/rsyslog
install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/syslog
install -p -m 644 plugins/ommysql/createDB.sql %{buildroot}%{rsyslog_docdir}/mysql-createDB.sql
install -p -m 644 plugins/ompgsql/createDB.sql %{buildroot}%{rsyslog_docdir}/pgsql-createDB.sql
dos2unix tools/recover_qi.pl
install -p -m 644 tools/recover_qi.pl %{buildroot}%{rsyslog_docdir}/recover_qi.pl
# extract documentation
cp -r doc/* %{buildroot}%{rsyslog_docdir}/html
# get rid of libtool libraries
rm -f %{buildroot}%{_libdir}/rsyslog/*.la
# get rid of socket activation by default
sed -i '/^Alias/s/^/;/;/^Requires=syslog.socket/s/^/;/' %{buildroot}%{_unitdir}/rsyslog.service
# imdiag is only used for testing
rm -f %{buildroot}%{_libdir}/rsyslog/imdiag.so

%post
for n in /var/log/{messages,secure,maillog,spooler}
do
	[ -f $n ] && continue
	umask 066 && touch $n
done
%systemd_post rsyslog.service

%preun
%systemd_preun rsyslog.service

%postun
%systemd_postun_with_restart rsyslog.service

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING*
%doc AUTHORS ChangeLog README.md
%exclude %{rsyslog_docdir}/html
%dir %{_libdir}/rsyslog
%dir %{_sysconfdir}/rsyslog.d
%dir %{rsyslog_statedir}
%dir %{rsyslog_pkidir}
%{_sbindir}/rsyslogd
%{_mandir}/man5/rsyslog.conf.5.gz
%{_mandir}/man8/rsyslogd.8.gz
%{_unitdir}/rsyslog.service
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
# plugins
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/imjournal.so
%{_libdir}/rsyslog/imklog.so
%{_libdir}/rsyslog/immark.so
%{_libdir}/rsyslog/imtcp.so
%{_libdir}/rsyslog/imudp.so
%{_libdir}/rsyslog/imuxsock.so
%{_libdir}/rsyslog/lmnet.so
%{_libdir}/rsyslog/lmnetstrms.so
%{_libdir}/rsyslog/lmnsd_ptcp.so
%{_libdir}/rsyslog/lmregexp.so
%{_libdir}/rsyslog/lmstrmsrv.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/mmexternal.so
%{_libdir}/rsyslog/omjournal.so
%{_libdir}/rsyslog/omprog.so
%{_libdir}/rsyslog/omstdout.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/pmaixforwardedfrom.so
%{_libdir}/rsyslog/pmcisconames.so
%{_libdir}/rsyslog/pmlastmsg.so
%{_libdir}/rsyslog/pmsnare.so

%changelog
* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 8.14.0-2
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 8.10.0-2
- Rebuild for new 4.0 release.

