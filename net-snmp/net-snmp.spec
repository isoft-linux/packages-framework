# use netsnmp_tcp_wrappers 0 to disable tcp_wrappers support
%{!?netsnmp_tcp_wrappers:%global netsnmp_tcp_wrappers 1}
# use nestnmp_check 0 to speed up packaging by disabling 'make test'
%{!?netsnmp_check: %global netsnmp_check 1}

# allow compilation on Fedora 11 and older
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
# Arches on which we need to prevent arch conflicts on net-snmp-config.h
%global multilib_arches %{ix86} ia64 ppc ppc64 s390 s390x x86_64 sparc sparcv9 sparc64 aarch64

Summary: A collection of SNMP protocol tools and libraries
Name: net-snmp
Version: 5.7.3
Release: 6%{?dist}
Epoch: 1

License: BSD
URL: http://net-snmp.sourceforge.net/
Source0: https://downloads.sourceforge.net/project/net-snmp/net-snmp/%{version}/net-snmp-%{version}.tar.gz
Source1: net-snmp.redhat.conf
Source2: net-snmpd.init
Source3: net-snmptrapd.init
Source4: net-snmp-config.h
Source5: net-snmp-config
Source6: net-snmp-trapd.redhat.conf
Source7: net-snmpd.sysconfig
Source8: net-snmptrapd.sysconfig
Source9: net-snmp-tmpfs.conf
Source10: snmpd.service
Source11: snmptrapd.service
Source12: IETF-MIB-LICENSE.txt
Patch1: net-snmp-5.7.2-pie.patch
Patch2: net-snmp-5.5-dir-fix.patch
Patch3: net-snmp-5.6-multilib.patch
Patch4: net-snmp-5.5-apsl-copying.patch
Patch5: net-snmp-5.6-test-debug.patch
Patch6: net-snmp-5.7.2-systemd.patch
Patch7: net-snmp-5.7.2-create-user-multilib.patch
Patch8: net-snmp-5.7.2-autoreconf.patch
Patch9: net-snmp-5.7-agentx-crash.patch
Patch10: net-snmp-5.5-agentx-disconnect-crash.patch
Patch11: net-snmp-5.7.2-cert-path.patch
Patch12: net-snmp-5.7.3-snmpstatus-null.patch

# for /bin/rm
Requires(preun): coreutils
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-agent-libs%{?_isa} = %{epoch}:%{version}-%{release}

BuildRequires: openssl-devel, bzip2-devel, libelfutils-devel
BuildRequires: libelfutils-devel, librpm-devel
BuildRequires: perl-devel, perl(ExtUtils::Embed), procps
BuildRequires: python-devel, python-setuptools
BuildRequires: chrpath
# for netstat, needed by 'make test'
BuildRequires: net-tools
# for make test
BuildRequires: perl(TAP::Harness)
BuildRequires: systemd-units
%ifnarch s390 s390x ppc64le
BuildRequires: lm_sensors-devel >= 3
%endif
%if %{netsnmp_tcp_wrappers}
BuildRequires: tcp_wrappers-devel
%endif
BuildRequires: autoconf, automake

%description
SNMP (Simple Network Management Protocol) is a protocol used for
network management. The NET-SNMP project includes various SNMP tools:
an extensible agent, an SNMP library, tools for requesting or setting
information from SNMP agents, tools for generating and handling SNMP
traps, a version of the netstat command which uses SNMP, and a Tk/Perl
mib browser. This package contains the snmpd and snmptrapd daemons,
documentation, etc.

You will probably also want to install the net-snmp-utils package,
which contains NET-SNMP utilities.

%package utils
Summary: Network management utilities using SNMP, from the NET-SNMP project
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description utils
The net-snmp-utils package contains various utilities for use with the
NET-SNMP network management project.

Install this package if you need utilities for managing your network
using the SNMP protocol. You will also need to install the net-snmp
package.

%package devel
Summary: The development environment for the NET-SNMP project
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-agent-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: libelfutils-devel, librpm-devel, openssl-devel
%if %{netsnmp_tcp_wrappers}
Requires: tcp_wrappers-devel
%endif
%ifnarch s390 s390x ppc64le
Requires: lm_sensors-devel
%endif
# pull perl development libraries, net-snmp agent libraries may link to them
Requires: perl-devel%{?_isa}

%description devel
The net-snmp-devel package contains the development libraries and
header files for use with the NET-SNMP project's network management
tools.

Install the net-snmp-devel package if you would like to develop
applications for use with the NET-SNMP project's network management
tools. You'll also need to have the net-snmp and net-snmp-utils
packages installed.

%package perl
Summary: The perl NET-SNMP module and the mib2c tool
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}, perl
Requires: %{name}-agent-libs%{?_isa} = %{epoch}:%{version}-%{release}
BuildRequires: perl

%description perl
The net-snmp-perl package contains the perl files to use SNMP from within
Perl.

Install the net-snmp-perl package, if you want to use mib2c or SNMP 
with perl.

#%package gui
#Group: Applications/System
#Summary: An interactive graphical MIB browser for SNMP
#Requires: perl-Tk, net-snmp-perl%{?_isa} = %{epoch}:%{version}-%{release}
#
#%description gui
#The net-snmp-gui package contains tkmib utility, which is a graphical user 
#interface for browsing the Message Information Bases (MIBs). It is also 
#capable of sending or retrieving the SNMP management information to/from 
#the remote agents interactively.
#
#Install the net-snmp-gui package, if you want to use this interactive utility.

%package libs
Summary: The NET-SNMP runtime client libraries

%description libs
The net-snmp-libs package contains the runtime client libraries for shared
binaries and applications.

%package agent-libs
Summary: The NET-SNMP runtime agent libraries
# the libs link against libperl.so:
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description agent-libs
The net-snmp-agent-libs package contains the runtime agent libraries for shared
binaries and applications.

%package python
Summary: The Python 'netsnmp' module for the Net-SNMP
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description python
The 'netsnmp' module provides a full featured, tri-lingual SNMP (SNMPv3, 
SNMPv2c, SNMPv1) client API. The 'netsnmp' module internals rely on the
Net-SNMP toolkit library.

%prep
%setup -q
cp %{SOURCE12} .

%ifnarch ia64
%patch1 -p1 -b .pie
%endif

%patch2 -p1 -b .dir-fix
%patch3 -p1 -b .multilib
%patch4 -p1 -b .apsl
%patch5 -p1
%patch6 -p1 -b .systemd
%patch7 -p1 -b .multilib
%patch8 -p1 -b .autoreconf
%patch9 -p1 -b .agentx-crash
%patch10 -p1 -b .agentx-disconnect-crash
%patch11 -p1 -b .cert-path
%patch12 -p1 -b .snmpstatus-null

%ifarch sparc64 s390 s390x
# disable failing test - see https://bugzilla.redhat.com/show_bug.cgi?id=680697
rm testing/fulltests/default/T200*
%endif

%build

# Autoreconf to get autoconf 2.69 for ARM (#926223)
autoreconf

MIBS="host agentx smux \
     ucd-snmp/diskio tcp-mib udp-mib mibII/mta_sendmail \
     ip-mib/ipv4InterfaceTable ip-mib/ipv6InterfaceTable \
     ip-mib/ipAddressPrefixTable/ipAddressPrefixTable \
     ip-mib/ipDefaultRouterTable/ipDefaultRouterTable \
     ip-mib/ipv6ScopeZoneIndexTable ip-mib/ipIfStatsTable \
     sctp-mib rmon-mib etherlike-mib"

%ifnarch s390 s390x ppc64le
# there are no lm_sensors on s390
MIBS="$MIBS ucd-snmp/lmsensorsMib"
%endif

%configure \
    --disable-static --enable-shared \
    --with-cflags="$RPM_OPT_FLAGS -D_RPM_4_4_COMPAT" \
    --with-ldflags="-Wl,-z,relro -Wl,-z,now" \
    --with-sys-location="Unknown" \
    --with-logfile="/var/log/snmpd.log" \
    --with-persistent-directory="/var/lib/net-snmp" \
    --with-mib-modules="$MIBS" \
%if %{netsnmp_tcp_wrappers}
    --with-libwrap=yes \
%endif
    --sysconfdir=%{_sysconfdir} \
    --enable-ipv6 \
    --enable-ucd-snmp-compatibility \
    --with-openssl \
    --with-pic \
    --enable-embedded-perl \
    --enable-as-needed \
    --with-perl-modules="INSTALLDIRS=vendor" \
    --enable-mfd-rewrites \
    --enable-local-smux \
    --with-temp-file-pattern=/var/run/net-snmp/snmp-tmp-XXXXXX \
    --with-transports="DTLSUDP TLSTCP" \
    --with-security-modules=tsm  \
    --without-mysql \
    --with-systemd \
    --with-sys-contact="root@localhost" <<EOF
EOF

# store original libtool file, we will need it later
cp libtool libtool.orig
# remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# the package is not %%_smp_mflags safe
make

# remove rpath from compiled perl libs
find perl/blib -type f -name "*.so" -print -exec chrpath --delete {} \;

# compile python module
pushd python
%{__python} setup.py --basedir="../" build
popd


%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

# Determine which arch net-snmp-config.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif

%ifarch %{multilib_arches}
# Do an net-snmp-config.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, as they each need
# their own correct-but-different versions of net-snmp-config.h to be usable.
mv ${RPM_BUILD_ROOT}/%{_bindir}/net-snmp-config ${RPM_BUILD_ROOT}/%{_bindir}/net-snmp-config-${basearch}
install -m 755 %SOURCE5 ${RPM_BUILD_ROOT}/%{_bindir}/net-snmp-config
mv ${RPM_BUILD_ROOT}/%{_includedir}/net-snmp/net-snmp-config.h ${RPM_BUILD_ROOT}/%{_includedir}/net-snmp/net-snmp-config-${basearch}.h
install -m644 %SOURCE4 ${RPM_BUILD_ROOT}/%{_includedir}/net-snmp/net-snmp-config.h
%endif

install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/snmp
install -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_sysconfdir}/snmp/snmpd.conf
install -m 644 %SOURCE6 ${RPM_BUILD_ROOT}%{_sysconfdir}/snmp/snmptrapd.conf

install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
install -m 644 %SOURCE7 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/snmpd
install -m 644 %SOURCE8 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/snmptrapd

# prepare /var/lib/net-snmp
install -d ${RPM_BUILD_ROOT}%{_localstatedir}/lib/net-snmp
install -d ${RPM_BUILD_ROOT}%{_localstatedir}/lib/net-snmp/mib_indexes
install -d ${RPM_BUILD_ROOT}%{_localstatedir}/lib/net-snmp/cert_indexes
install -d ${RPM_BUILD_ROOT}%{_localstatedir}/run/net-snmp

# remove things we don't want to distribute
rm -f ${RPM_BUILD_ROOT}%{_bindir}/snmpinform
ln -s snmptrap ${RPM_BUILD_ROOT}/usr/bin/snmpinform
rm -f ${RPM_BUILD_ROOT}%{_bindir}/snmpcheck
rm -f ${RPM_BUILD_ROOT}/%{_bindir}/fixproc
rm -f ${RPM_BUILD_ROOT}/%{_mandir}/man1/fixproc*
rm -f ${RPM_BUILD_ROOT}/%{_bindir}/ipf-mod.pl
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/libsnmp*

# remove special perl files
find $RPM_BUILD_ROOT -name perllocal.pod \
    -o -name .packlist \
    -o -name "*.bs" \
    -o -name Makefile.subs.pl \
    | xargs -ri rm -f {}
# remove docs that do not apply to Linux
rm -f README.aix README.hpux11 README.osX README.Panasonic_AM3X.txt README.solaris README.win32

# copy missing mib2c.conf files
install -m 644 local/mib2c.*.conf ${RPM_BUILD_ROOT}%{_datadir}/snmp

# install python module
pushd python
%{__python} setup.py --basedir=.. install -O1 --skip-build --root $RPM_BUILD_ROOT 
popd

find $RPM_BUILD_ROOT -name '*.so' | xargs chmod 0755

# trim down massive ChangeLog
dd bs=1024 count=250 if=ChangeLog of=ChangeLog.trimmed

# convert files to UTF-8
for file in README COPYING; do
    iconv -f 8859_1 -t UTF-8 <$file >$file.utf8
    mv $file.utf8 $file
done

# remove executable bit from documentation samples
chmod 644 local/passtest local/ipf-mod.pl

# dirty hack for #603243, until it's fixed properly upstream
install -m 755 -d $RPM_BUILD_ROOT/usr/include/net-snmp/agent/util_funcs
install -m 644  agent/mibgroup/util_funcs/*.h $RPM_BUILD_ROOT/usr/include/net-snmp/agent/util_funcs

# systemd stuff
install -m 755 -d $RPM_BUILD_ROOT/%{_tmpfilesdir}
install -m 644 %SOURCE9 $RPM_BUILD_ROOT/%{_tmpfilesdir}/net-snmp.conf
install -m 755 -d $RPM_BUILD_ROOT/%{_unitdir}
install -m 644 %SOURCE10 %SOURCE11 $RPM_BUILD_ROOT/%{_unitdir}/

%check
%if %{netsnmp_check}
%ifarch ppc ppc64
rm -vf testing/fulltests/default/T200snmpv2cwalkall_simple
%endif
# restore libtool, for unknown reason it does not work with the one without rpath
cp -f libtool.orig libtool
# temporary workaround to make test "extending agent functionality with pass" working
chmod 755 local/passtest

LD_LIBRARY_PATH=${RPM_BUILD_ROOT}/%{_libdir} make test
%endif


%post
%systemd_post snmpd.service snmptrapd.service

%preun
%systemd_preun snmpd.service snmptrapd.service


%postun
%systemd_postun_with_restart snmpd.service snmptrapd.service


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post agent-libs -p /sbin/ldconfig

%postun agent-libs -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%doc COPYING ChangeLog.trimmed EXAMPLE.conf FAQ NEWS TODO
%doc README README.agent-mibs README.agentx README.krb5 README.snmpv3
%doc local/passtest local/ipf-mod.pl
%doc README.thread AGENT.txt PORTING local/README.mib2c
%doc IETF-MIB-LICENSE.txt
%dir %{_sysconfdir}/snmp
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/snmp/snmpd.conf
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/snmp/snmptrapd.conf
%{_bindir}/snmpconf
%{_bindir}/net-snmp-create-v3-user
%{_sbindir}/*
%attr(0644,root,root) %{_mandir}/man[58]/snmp*d*
%attr(0644,root,root) %{_mandir}/man5/snmp_config.5.gz
%attr(0644,root,root) %{_mandir}/man5/variables*
%attr(0644,root,root) %{_mandir}/man1/net-snmp-create-v3-user*
%attr(0644,root,root) %{_mandir}/man1/snmpconf.1.gz
%dir %{_datadir}/snmp
%{_datadir}/snmp/snmpconf-data
%dir %{_localstatedir}/run/net-snmp
%{_tmpfilesdir}/net-snmp.conf
%{_unitdir}/snmp*
%config(noreplace) %{_sysconfdir}/sysconfig/snmpd
%config(noreplace) %{_sysconfdir}/sysconfig/snmptrapd
%{_bindir}/agentxtrap
%attr(0644,root,root) %{_mandir}/man1/agentxtrap.1*

%files utils
%{_bindir}/encode_keychange
%{_bindir}/snmp[^c-]*
%attr(0644,root,root) %{_mandir}/man1/snmp[^-]*.1*
%attr(0644,root,root) %{_mandir}/man1/encode_keychange*.1*
%attr(0644,root,root) %{_mandir}/man5/snmp.conf.5.gz
%attr(0644,root,root) %{_mandir}/man5/variables.5.gz

%files devel
%{_libdir}/lib*.so
/usr/include/*
%attr(0644,root,root) %{_mandir}/man3/*.3.*
%attr(0755,root,root) %{_bindir}/net-snmp-config*
%attr(0644,root,root) %{_mandir}/man1/net-snmp-config*.1.*

%files perl
%{_bindir}/mib2c-update
%{_bindir}/mib2c
%{_bindir}/snmp-bridge-mib
%{_bindir}/net-snmp-cert
%dir %{_datadir}/snmp
%{_datadir}/snmp/mib2c*
%{_datadir}/snmp/*.pl
%{_bindir}/traptoemail
%attr(0644,root,root) %{_mandir}/man[15]/mib2c*
%attr(0644,root,root) %{_mandir}/man3/*.3pm.*
%attr(0644,root,root) %{_mandir}/man1/traptoemail*.1*
%attr(0644,root,root) %{_mandir}/man1/snmp-bridge-mib.1*
%{perl_vendorarch}/*SNMP*
%{perl_vendorarch}/auto/*SNMP*
%{perl_vendorarch}/auto/Bundle/*SNMP*

%files python
%doc README
%{python_sitearch}/*

#%files gui
#%{_bindir}/tkmib
#%attr(0644,root,root) %{_mandir}/man1/tkmib.1*

%files libs
%doc COPYING README ChangeLog.trimmed FAQ NEWS TODO
%doc IETF-MIB-LICENSE.txt
%{_libdir}/libnetsnmp.so.*
%dir %{_datadir}/snmp
%dir %{_datadir}/snmp/mibs
%{_datadir}/snmp/mibs/*
%dir %{_localstatedir}/lib/net-snmp
%dir %{_localstatedir}/lib/net-snmp/mib_indexes
%dir %{_localstatedir}/lib/net-snmp/cert_indexes

%files agent-libs
%{_libdir}/libnetsnmpagent*.so.*
%{_libdir}/libnetsnmphelpers*.so.*
%{_libdir}/libnetsnmpmibs*.so.*
%{_libdir}/libnetsnmptrapd*.so.*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:5.7.3-6
- Rebuild for new 4.0 release.

