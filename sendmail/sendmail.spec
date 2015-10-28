# package options
%global with_tls    no	
%global with_sasl2  no	
%global with_milter	yes
%global with_ldap   no	
%global enable_pie	yes

%global sendmailcf %{_datadir}/sendmail-cf
%global stdir %{_localstatedir}/log/mail
%global smshell /sbin/nologin
%global spooldir %{_localstatedir}/spool
%global maildir %{_sysconfdir}/mail

# hardened build if not overrided
%{!?_hardened_build:%global _hardened_build 1}

%if %{?_hardened_build:%{_hardened_build}}%{!?_hardened_build:0}
%global relro -Xlinker -z -Xlinker relro -Xlinker -z -Xlinker now
%endif

Summary: A widely used Mail Transport Agent (MTA)
Name: sendmail
Version: 8.15.1
Release: 7%{?dist}
License: Sendmail
URL: http://www.sendmail.org/
Source0: ftp://ftp.sendmail.org/pub/sendmail/sendmail.%{version}.tar.gz
# Systemd Service file
Source1: sendmail.service
# NetworkManager dispatch script
Source2: sendmail.nm-dispatcher
# script to generate db and cf files
Source3: sendmail.etc-mail-make
# default sysconfig file
Source4: sendmail.sysconfig
# default /etc/mail/Makefile
Source5: sendmail.etc-mail-Makefile
# default sendmail.mc
Source6: sendmail-redhat.mc
# Systemd Service file
Source7: sm-client.service
# pam config
Source8: sendmail.pam
Source9: sendmail.init
# sasl2 config
Source11: Sendmail-sasl2.conf
# default /etc/mail/access
Source12: sendmail-etc-mail-access
# default /etc/mail/domaintable
Source13: sendmail-etc-mail-domaintable
# default /etc/mail/local-host-names
Source14: sendmail-etc-mail-local-host-names
# default /etc/mail/mailertable
Source15: sendmail-etc-mail-mailertable
# default /etc/mail/trusted-users
Source16: sendmail-etc-mail-trusted-users
# default /etc/mail/virtusertable
Source17: sendmail-etc-mail-virtusertable
# fix man path and makemap man page
Patch3: sendmail-8.14.4-makemapman.patch
# fix smrsh paths
Patch4: sendmail-8.14.3-smrsh_paths.patch
# fix sm-client.pid path
Patch7: sendmail-8.14.9-pid.patch
# fix sendmail man page
Patch10: sendmail-8.15.1-manpage.patch
# compile with -fpie
Patch11: sendmail-8.15.1-dynamic.patch
# fix cyrus path
Patch12: sendmail-8.13.0-cyrus.patch
# fix aliases.db path
Patch13: sendmail-8.15.1-aliases_dir.patch
# fix vacation Makefile
Patch14: sendmail-8.14.9-vacation.patch
# remove version information from sendmail helpfile
Patch15: sendmail-8.14.9-noversion.patch
# do not accept localhost.localdomain as valid address from SMTP
Patch16: sendmail-8.15.1-localdomain.patch
# build libmilter as DSO
Patch17: sendmail-8.14.3-sharedmilter.patch
# skip colon separator when parsing service name in ServiceSwitchFile
Patch18: sendmail-8.15.1-switchfile.patch
# handle IPv6:::1 in block_bad_helo.m4 like 127.0.0.1, #549217
Patch21: sendmail-8.15.1-ipv6-bad-helo.patch
# silence warning about missing sasl2 config in /usr/lib*, now in /etc/sasl2
Patch23: sendmail-8.14.8-sasl2-in-etc.patch
# upstream reserved option ID 0xe7 for testing of this new feature, #576643
Patch25: sendmail-8.15.1-qos.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: tcp_wrappers-devel
BuildRequires: libdb-devel
BuildRequires: groff
BuildRequires: ghostscript
BuildRequires: m4
BuildRequires: systemd
Provides: MTA smtpdaemon server(smtp)
Requires(post): systemd coreutils %{_sbindir}/alternatives
Requires(preun): systemd %{_sbindir}/alternatives
Requires(postun): systemd coreutils %{_sbindir}/alternatives
Requires(pre): shadow-utils
Requires: procmail
Requires: bash >= 2.0
Requires: setup >= 2.5.31-1
BuildRequires: setup >= 2.5.31-1
%if "%{with_tls}" == "yes"
BuildRequires: openssl-devel
%endif
%if "%{with_sasl2}" == "yes"
BuildRequires: cyrus-sasl-devel openssl-devel
Requires: %{_sbindir}/saslauthd
%endif
%if "%{with_ldap}" == "yes"
BuildRequires: openldap-devel openssl-devel
%endif


%description
The Sendmail program is a very widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another. Sendmail is not a client
program, which you use to read your email. Sendmail is a
behind-the-scenes program which actually moves your email over
networks or the Internet to where you want it to go.

If you ever need to reconfigure Sendmail, you will also need to have
the sendmail-cf package installed. If you need documentation on
Sendmail, you can install the sendmail-doc package.

%package doc
Summary: Documentation about the Sendmail Mail Transport Agent program
BuildArch: noarch
Requires: sendmail = %{version}-%{release}

%description doc
This package contains the Sendmail Installation and Operation Guide (PDF),
text files containing configuration documentation, plus a number of
contributed scripts and tools for use with Sendmail.

%package devel
Summary: Extra development include files and development files
Requires: sendmail = %{version}-%{release}
Requires: sendmail-milter = %{version}-%{release}

%description devel
Include files and devel libraries for e.g. the milter add-ons as part
of sendmail.

%package cf
Summary: The files needed to reconfigure Sendmail
Requires: sendmail = %{version}-%{release}
BuildArch: noarch
Requires: m4

%description cf
This package includes the configuration files you need to generate the
sendmail.cf file distributed with the sendmail package. You will need
the sendmail-cf package if you ever need to reconfigure and rebuild
your sendmail.cf file.

%package milter
Summary: The sendmail milter library

%description milter
The sendmail Mail Filter API (Milter) is designed to allow third-party
programs access to mail messages as they are being processed in order to
filter meta-information and content.

This package includes the milter shared library.

%prep
%setup -q

%patch3 -p1 -b .makemapman
%patch4 -p1 -b .smrsh_paths
%patch7 -p1 -b .pid
%patch10 -p1 -b .manpage
%patch11 -p1 -b .dynamic
%patch12 -p1 -b .cyrus
%patch13 -p1 -b .aliases_dir
%patch14 -p1 -b .vacation
%patch15 -p1 -b .noversion
%patch16 -p1 -b .localdomain

cp devtools/M4/UNIX/{,shared}library.m4
%patch17 -p1 -b .sharedmilter

%patch18 -p1 -b .switchfile
%patch21 -p1 -b .ipv6-bad-helo
%patch23 -p1 -b .sasl2-in-etc
%patch25 -p1 -b .qos

for f in RELEASE_NOTES contrib/etrn.0; do
	iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
		touch -r ${f}{,_} && mv -f ${f}{_,}
done

sed -i 's|/usr/local/bin/perl|%{_bindir}/perl|' contrib/*.pl

%build
# generate redhat config file
cat > redhat.config.m4 << EOF
define(\`confMAPDEF', \`-DNEWDB -DNIS -DMAP_REGEX -DSOCKETMAP')
define(\`confOPTIMIZE', \`\`\`\`${RPM_OPT_FLAGS}'''')
define(\`confENVDEF', \`-I%{_includedir}/libdb -I/usr/kerberos/include -Wall -DXDEBUG=0 -DTCPWRAPPERS -DNETINET6 -DHES_GETMAILHOST -DUSE_VENDOR_CF_PATH=1 -D_FFR_TLS_1 -D_FFR_LINUX_MHNL -D_FFR_QOS -D_FFR_TLS_EC -D_FILE_OFFSET_BITS=64 -DHESIOD_ALLOW_NUMERIC_LOGIN')
define(\`confLIBDIRS', \`-L/usr/kerberos/%{_lib}')
define(\`confLIBS', \`-lnsl -lwrap -lcrypt -ldb -lresolv %{?relro:%{relro}}')
define(\`confMANOWN', \`root')
define(\`confMANGRP', \`root')
define(\`confMANMODE', \`644')
define(\`confMAN1SRC', \`1')
define(\`confMAN5SRC', \`5')
define(\`confMAN8SRC', \`8')
define(\`confSTDIR', \`%{stdir}')
define(\`STATUS_FILE', \`%{stdir}/statistics')
define(\`confLIBSEARCH', \`db resolv 44bsd')
EOF
#'

cat >> redhat.config.m4 << EOF
%ifarch ppc %{power64} s390x
APPENDDEF(\`confOPTIMIZE', \`-DSM_CONF_SHM=0')
%else
APPENDDEF(\`confOPTIMIZE', \`')
%endif
EOF

%if "%{enable_pie}" == "yes"
%ifarch s390 s390x sparc sparcv9 sparc64
%global _fpie -fPIE
%else
%global _fpie -fpie
%endif
cat >> redhat.config.m4 << EOF
APPENDDEF(\`confOPTIMIZE', \`%{_fpie}')
APPENDDEF(\`confLIBS', \`-pie')
EOF
%endif

%if "%{with_tls}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`conf_sendmail_ENVDEF', \`-DSTARTTLS')dnl
APPENDDEF(\`conf_sendmail_LIBS', \`-lssl -lcrypto')dnl
EOF
%endif

%if "%{with_sasl2}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`confENVDEF', \`-DSASL=2')dnl
APPENDDEF(\`confLIBS', \`-lsasl2 -lcrypto')dnl
EOF
%endif

%if "%{with_milter}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`conf_sendmail_ENVDEF', \`-DMILTER')dnl
EOF
%endif

%if "%{with_ldap}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`confMAPDEF', \`-DLDAPMAP -DLDAP_DEPRECATED')dnl
APPENDDEF(\`confENVDEF', \`-DSM_CONF_LDAP_MEMFREE=1')dnl
APPENDDEF(\`confLIBS', \`-lldap -llber -lssl -lcrypto')dnl
EOF
%endif

DIRS="libsmutil sendmail mailstats rmail praliases smrsh makemap"

%if "%{with_milter}" == "yes"
DIRS="libmilter $DIRS"
%endif

for i in $DIRS; do
	pushd $i
	sh Build -f ../redhat.config.m4
	popd
done

make -C doc/op op.pdf

%install
rm -rf %{buildroot}

# create directories
for d in %{_bindir} %{_sbindir} %{_includedir}/libmilter \
	%{_libdir} %{_mandir}/man{1,5,8} %{maildir} %{stdir} %{spooldir} \
	%{_docdir}/sendmail %{sendmailcf} %{_sysconfdir}/smrsh\
	%{spooldir}/clientmqueue %{_sysconfdir}/sysconfig %{_initrddir} \
	%{_sysconfdir}/pam.d %{_docdir}/sendmail/contrib \
	%{_sysconfdir}/NetworkManager/dispatcher.d
do
	install -m 755 -d %{buildroot}$d
done
install -m 700 -d %{buildroot}%{spooldir}/mqueue

# create /usr/lib for 64 bit architectures
%if "%{_libdir}" != "/usr/lib"
install -m 755 -d %{buildroot}/usr/lib
%endif

nameuser=`id -nu`
namegroup=`id -ng`

Make() {
	make $@ \
		DESTDIR=%{buildroot} \
		LIBDIR=%{_libdir} \
		MANROOT=%{_mandir}/man \
		LIBMODE=0755 INCMODE=0644 \
		SBINOWN=${nameuser} SBINGRP=${namegroup} \
		UBINOWN=${nameuser} UBINGRP=${namegroup} \
		MANOWN=${nameuser} MANGRP=${namegroup} \
		INCOWN=${nameuser} INCGRP=${namegroup} \
		LIBOWN=${nameuser} LIBGRP=${namegroup} \
		GBINOWN=${nameuser} GBINGRP=${namegroup} \
		CFOWN=${nameuser} CFGRP=${namegroup} \
		CFMODE=0644 MSPQOWN=${nameuser}
}

OBJDIR=obj.$(uname -s).$(uname -r).$(uname -m)

Make install -C $OBJDIR/libmilter
Make install -C $OBJDIR/sendmail
Make install -C $OBJDIR/mailstats
Make force-install -C $OBJDIR/rmail
Make install -C $OBJDIR/praliases
Make install -C $OBJDIR/smrsh
Make install -C $OBJDIR/makemap

# replace absolute with relative symlinks
ln -sf ../sbin/makemap %{buildroot}%{_bindir}/makemap
for f in hoststat mailq newaliases purgestat ; do
	ln -sf ../sbin/sendmail.sendmail %{buildroot}%{_bindir}/${f}
done

# use /usr/lib, even for 64 bit architectures
ln -sf ../sbin/sendmail.sendmail %{buildroot}/usr/lib/sendmail.sendmail

# install docs for sendmail
install -p -m 644 FAQ %{buildroot}%{_docdir}/sendmail
install -p -m 644 KNOWNBUGS %{buildroot}%{_docdir}/sendmail
install -p -m 644 LICENSE %{buildroot}%{_docdir}/sendmail
install -p -m 644 README %{buildroot}%{_docdir}/sendmail
install -p -m 644 RELEASE_NOTES %{buildroot}%{_docdir}/sendmail
gzip -9 %{buildroot}%{_docdir}/sendmail/RELEASE_NOTES

# install docs for sendmail-doc
install -m 644 doc/op/op.pdf %{buildroot}%{_docdir}/sendmail
install -p -m 644 sendmail/README %{buildroot}%{_docdir}/sendmail/README.sendmail
install -p -m 644 sendmail/SECURITY %{buildroot}%{_docdir}/sendmail
install -p -m 644 smrsh/README %{buildroot}%{_docdir}/sendmail/README.smrsh
install -p -m 644 libmilter/README %{buildroot}%{_docdir}/sendmail/README.libmilter
install -p -m 644 cf/README %{buildroot}%{_docdir}/sendmail/README.cf
install -p -m 644 contrib/* %{buildroot}%{_docdir}/sendmail/contrib

# install the cf files for the sendmail-cf package.
cp -ar cf/* %{buildroot}%{sendmailcf}
# remove patch backup files
rm -rf %{buildroot}%{sendmailcf}/cf/Build.*
rm -rf %{buildroot}%{sendmailcf}/*/*.mc.*
rm -rf %{buildroot}%{sendmailcf}/*/*.m4.*
# remove cf/README file because it is useless for end users
rm -f %{buildroot}%{sendmailcf}/cf/README

# install sendmail.mc with proper paths
install -m 644 %{SOURCE6} %{buildroot}%{maildir}/sendmail.mc
sed -i -e 's|@@PATH@@|%{sendmailcf}|' %{buildroot}%{maildir}/sendmail.mc
touch -r %{SOURCE6} %{buildroot}%{maildir}/sendmail.mc

# create sendmail.cf
cp %{buildroot}%{maildir}/sendmail.mc cf/cf/redhat.mc
sed -i -e 's|%{sendmailcf}|\.\.|' cf/cf/redhat.mc
%if "%{stdir}" != "%{maildir}"
sed -i -e 's:%{maildir}/statistics:%{stdir}/statistics:' cf/cf/redhat.mc
%endif
(cd cf/cf && m4 redhat.mc > redhat.cf)
install -m 644 cf/cf/redhat.cf %{buildroot}%{maildir}/sendmail.cf
install -p -m 644 cf/cf/submit.mc %{buildroot}%{maildir}/submit.mc

# remove our build info as it causes multiarch conflicts
sed -i '/##### built by.*on/,+3d' %{buildroot}%{maildir}/{submit,sendmail}.cf \
	%{buildroot}%{sendmailcf}/cf/submit.cf

install -p -m 644 %{SOURCE12} %{buildroot}%{maildir}/access
install -p -m 644 %{SOURCE13} %{buildroot}%{maildir}/domaintable
install -p -m 644 %{SOURCE14} %{buildroot}%{maildir}/local-host-names
install -p -m 644 %{SOURCE15} %{buildroot}%{maildir}/mailertable
install -p -m 644 %{SOURCE16} %{buildroot}%{maildir}/trusted-users
install -p -m 644 %{SOURCE17} %{buildroot}%{maildir}/virtusertable

# create db ghosts
for map in virtusertable access domaintable mailertable ; do
	touch %{buildroot}%{maildir}/${map}.db
	chmod 0644 %{buildroot}%{maildir}/${map}.db
done

touch %{buildroot}%{maildir}/aliasesdb-stamp

install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/sendmail
install -p -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/10-sendmail
install -p -m 755 %{SOURCE3} %{buildroot}%{maildir}/make
install -p -m 644 %{SOURCE5} %{buildroot}%{maildir}/Makefile

chmod 644 %{buildroot}%{maildir}/helpfile

# Systemd
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m644 %{SOURCE7} %{buildroot}%{_unitdir}

# fix permissions to allow debuginfo extraction and stripping
chmod 755 %{buildroot}%{_sbindir}/{mailstats,makemap,praliases,sendmail,smrsh}
chmod 755 %{buildroot}%{_bindir}/rmail

%if "%{with_sasl2}" == "yes"
install -m 755 -d %{buildroot}%{_sysconfdir}/sasl2
install -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/sasl2/Sendmail.conf
%endif
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/smtp.sendmail

# fix path for statistics file in man pages
%if "%{stdir}" != "%{maildir}"
sed -i -e 's:%{maildir}/statistics:%{stdir}/statistics:' %{buildroot}%{_mandir}/man*/*
%endif

# rename files for alternative usage
mv %{buildroot}%{_sbindir}/sendmail %{buildroot}%{_sbindir}/sendmail.sendmail
touch %{buildroot}%{_sbindir}/sendmail
mv %{buildroot}%{_sbindir}/makemap %{buildroot}%{_sbindir}/makemap.sendmail
touch %{buildroot}%{_sbindir}/makemap
for i in mailq newaliases rmail; do
	mv %{buildroot}%{_bindir}/$i %{buildroot}%{_bindir}/$i.sendmail
	touch %{buildroot}%{_bindir}/$i
done
mv %{buildroot}%{_mandir}/man1/mailq.1 %{buildroot}%{_mandir}/man1/mailq.sendmail.1
touch %{buildroot}%{_mandir}/man1/mailq.1
mv %{buildroot}%{_mandir}/man1/newaliases.1 %{buildroot}%{_mandir}/man1/newaliases.sendmail.1
touch %{buildroot}%{_mandir}/man1/newaliases.1
mv %{buildroot}%{_mandir}/man5/aliases.5 %{buildroot}%{_mandir}/man5/aliases.sendmail.5
touch %{buildroot}%{_mandir}/man5/aliases.5
mv %{buildroot}%{_mandir}/man8/sendmail.8 %{buildroot}%{_mandir}/man8/sendmail.sendmail.8
touch %{buildroot}%{_mandir}/man8/sendmail.8
mv %{buildroot}%{_mandir}/man8/rmail.8 %{buildroot}%{_mandir}/man8/rmail.sendmail.8
touch %{buildroot}%{_mandir}/man8/rmail.8
mv %{buildroot}%{_mandir}/man8/makemap.8 %{buildroot}%{_mandir}/man8/makemap.sendmail.8
touch %{buildroot}%{_mandir}/man8/makemap.8
touch %{buildroot}/usr/lib/sendmail
touch %{buildroot}%{_sysconfdir}/pam.d/smtp

# create stub man pages
for m in man8/hoststat.8 man8/purgestat.8; do
	[ -f %{buildroot}%{_mandir}/$m ] || 
		echo ".so man8/sendmail.8" > %{buildroot}%{_mandir}/$m
done

%clean
rm -rf %{buildroot}

%pre
getent group mailnull >/dev/null || \
  %{_sbindir}/groupadd -g 47 -r mailnull >/dev/null 2>&1
getent passwd mailnull >/dev/null || \
  %{_sbindir}/useradd -u 47 -g mailnull -d %{spooldir}/mqueue -r \
  -s %{smshell} mailnull >/dev/null 2>&1
getent group smmsp >/dev/null || \
  %{_sbindir}/groupadd -g 51 -r smmsp >/dev/null 2>&1
getent passwd smmsp >/dev/null || \
  %{_sbindir}/useradd -u 51 -g smmsp -d %{spooldir}/mqueue -r \
  -s %{smshell} smmsp >/dev/null 2>&1

# hack to turn sbin/makemap and man8/makemap.8.gz into alternatives symlink
# (part of the rhbz#1219178 fix), this could be probably dropped in f25+
[ -h %{_sbindir}/makemap ] || rm -f %{_sbindir}/makemap || :
[ -h %{_mandir}/man8/makemap.8.gz ] || rm -f %{_mandir}/man8/makemap.8.gz || :

exit 0

%postun
%systemd_postun_with_restart sendmail.service sm-client.service
if [ $1 -ge 1 ] ; then
	mta=`readlink %{_sysconfdir}/alternatives/mta`
	if [ "$mta" == "%{_sbindir}/sendmail.sendmail" ]; then
		%{_sbindir}/alternatives --set mta %{_sbindir}/sendmail.sendmail
	fi
fi
exit 0

%post
%systemd_post sendmail.service sm-client.service

# Set up the alternatives files for MTAs.
%{_sbindir}/alternatives --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.sendmail 90 \
	--slave %{_sbindir}/makemap mta-makemap %{_sbindir}/makemap.sendmail \
	--slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.sendmail \
	--slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.sendmail \
	--slave %{_bindir}/rmail mta-rmail %{_bindir}/rmail.sendmail \
	--slave /usr/lib/sendmail mta-sendmail /usr/lib/sendmail.sendmail \
	--slave %{_sysconfdir}/pam.d/smtp mta-pam %{_sysconfdir}/pam.d/smtp.sendmail \
	--slave %{_mandir}/man8/sendmail.8.gz mta-sendmailman %{_mandir}/man8/sendmail.sendmail.8.gz \
	--slave %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man1/mailq.sendmail.1.gz \
	--slave %{_mandir}/man1/newaliases.1.gz mta-newaliasesman %{_mandir}/man1/newaliases.sendmail.1.gz \
	--slave %{_mandir}/man5/aliases.5.gz mta-aliasesman %{_mandir}/man5/aliases.sendmail.5.gz \
	--slave %{_mandir}/man8/rmail.8.gz mta-rmailman %{_mandir}/man8/rmail.sendmail.8.gz \
	--slave %{_mandir}/man8/makemap.8.gz mta-makemapman %{_mandir}/man8/makemap.sendmail.8.gz \
	--initscript sendmail > /dev/null 2>&1

# Rebuild maps.
{
	chown root %{_sysconfdir}/aliases.db %{maildir}/access.db \
		%{maildir}/mailertable.db %{maildir}/domaintable.db \
		%{maildir}/virtusertable.db
	SM_FORCE_DBREBUILD=1 %{maildir}/make
	SM_FORCE_DBREBUILD=1 %{maildir}/make aliases
} > /dev/null 2>&1

# Move existing SASL2 config to new location.
%if "%{with_sasl2}" == "yes"
[ -f %{_libdir}/sasl2/Sendmail.conf ] && touch -r %{_sysconfdir}/sasl2/Sendmail.conf \
  %{_libdir}/sasl2/Sendmail.conf ] && mv -f %{_libdir}/sasl2/Sendmail.conf \
  %{_sysconfdir}/sasl2 2>/dev/null || :
%endif
exit 0

%preun
%systemd_preun sendmail.service sm-client.service
if [ $1 = 0 ]; then
	%{_sbindir}/alternatives --remove mta %{_sbindir}/sendmail.sendmail
fi
exit 0

%post milter -p /sbin/ldconfig

%postun milter -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_docdir}/sendmail
%doc %{_docdir}/sendmail/FAQ
%doc %{_docdir}/sendmail/KNOWNBUGS
%doc %{_docdir}/sendmail/LICENSE
%doc %{_docdir}/sendmail/README
%doc %{_docdir}/sendmail/RELEASE_NOTES.gz
%{_bindir}/hoststat
%{_bindir}/makemap
%{_bindir}/purgestat
%{_sbindir}/mailstats
%{_sbindir}/makemap.sendmail
%{_sbindir}/praliases
%attr(2755,root,smmsp) %{_sbindir}/sendmail.sendmail
%{_bindir}/rmail.sendmail
%{_bindir}/newaliases.sendmail
%{_bindir}/mailq.sendmail
%{_sbindir}/smrsh
/usr/lib/sendmail.sendmail

%{_mandir}/man8/rmail.sendmail.8.gz
%{_mandir}/man8/praliases.8.gz
%{_mandir}/man8/mailstats.8.gz
%{_mandir}/man8/makemap.sendmail.8.gz
%{_mandir}/man8/sendmail.sendmail.8.gz
%{_mandir}/man8/smrsh.8.gz
%{_mandir}/man8/hoststat.8.gz
%{_mandir}/man8/purgestat.8.gz
%{_mandir}/man5/aliases.sendmail.5.gz
%{_mandir}/man1/newaliases.sendmail.1.gz
%{_mandir}/man1/mailq.sendmail.1.gz

# dummy attributes for rpmlint
%ghost %attr(0755,-,-) %{_sbindir}/sendmail
%ghost %attr(0755,-,-) %{_sbindir}/makemap
%ghost %attr(0755,-,-) %{_bindir}/mailq
%ghost %attr(0755,-,-) %{_bindir}/newaliases
%ghost %attr(0755,-,-) %{_bindir}/rmail
%ghost %attr(0755,-,-) /usr/lib/sendmail

%ghost %{_sysconfdir}/pam.d/smtp
%ghost %{_mandir}/man8/sendmail.8.gz
%ghost %{_mandir}/man1/mailq.1.gz
%ghost %{_mandir}/man1/newaliases.1.gz
%ghost %{_mandir}/man5/aliases.5.gz
%ghost %{_mandir}/man8/rmail.8.gz
%ghost %{_mandir}/man8/makemap.8.gz

%dir %{stdir}
%dir %{_sysconfdir}/smrsh
%dir %{maildir}
%attr(0770,smmsp,smmsp) %dir %{spooldir}/clientmqueue
%attr(0700,root,mail) %dir %{spooldir}/mqueue

%config(noreplace) %verify(not size mtime md5) %{stdir}/statistics
%config(noreplace) %{maildir}/Makefile
%config(noreplace) %{maildir}/make
%config(noreplace) %{maildir}/sendmail.cf
%config(noreplace) %{maildir}/submit.cf
%config(noreplace) %{maildir}/helpfile
%config(noreplace) %{maildir}/sendmail.mc
%config(noreplace) %{maildir}/submit.mc
%config(noreplace) %{maildir}/access
%config(noreplace) %{maildir}/domaintable
%config(noreplace) %{maildir}/local-host-names
%config(noreplace) %{maildir}/mailertable
%config(noreplace) %{maildir}/trusted-users
%config(noreplace) %{maildir}/virtusertable

%ghost %{maildir}/aliasesdb-stamp
%ghost %{maildir}/virtusertable.db
%ghost %{maildir}/access.db
%ghost %{maildir}/domaintable.db
%ghost %{maildir}/mailertable.db

%{_unitdir}/sendmail.service
%{_unitdir}/sm-client.service
%config(noreplace) %{_sysconfdir}/sysconfig/sendmail
%config(noreplace) %{_sysconfdir}/pam.d/smtp.sendmail
%{_sysconfdir}/NetworkManager/dispatcher.d/10-sendmail

%if "%{with_sasl2}" == "yes"
%config(noreplace) %{_sysconfdir}/sasl2/Sendmail.conf
%endif

%files cf
%defattr(-,root,root,-)
%doc %{sendmailcf}/README
%dir %{sendmailcf}
%{sendmailcf}/cf
%{sendmailcf}/domain
%{sendmailcf}/feature
%{sendmailcf}/hack
%{sendmailcf}/m4
%{sendmailcf}/mailer
%{sendmailcf}/ostype
%{sendmailcf}/sendmail.schema
%{sendmailcf}/sh
%{sendmailcf}/siteconfig

%files devel
%defattr(-,root,root,-)
%doc libmilter/docs/*
%dir %{_includedir}/libmilter
%{_includedir}/libmilter/*.h
%{_libdir}/libmilter.so

%files milter
%defattr(-,root,root,-)
%doc LICENSE
%doc %{_docdir}/sendmail/README.libmilter
%{_libdir}/libmilter.so.[0-9].[0-9]
%{_libdir}/libmilter.so.[0-9].[0-9].[0-9]

%files doc
%defattr(-,root,root,-)
%{_docdir}/sendmail/README.cf
%{_docdir}/sendmail/README.sendmail
%{_docdir}/sendmail/README.smrsh
%{_docdir}/sendmail/SECURITY
%{_docdir}/sendmail/op.pdf
%dir %{_docdir}/sendmail/contrib
%attr(0644,root,root) %{_docdir}/sendmail/contrib/*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 8.15.1-7
- Rebuild for new 4.0 release.

