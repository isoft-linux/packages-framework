%global use_alternatives 1
%global lspp 0 

# {_exec_prefix}/lib/cups is correct, even on x86_64.
# It is not used for shared objects but for executables.
# It's more of a libexec-style ({_libexecdir}) usage,
# but we use lib for compatibility with 3rd party drivers (at upstream request).
%global cups_serverbin %{_exec_prefix}/lib/cups

#%%global prever rc1
#%%global VERSION %{version}%{prever}
%global VERSION %{version}

Summary: CUPS printing system
Name: cups
Epoch: 1
Version: 2.1.0
Release: 3%{?dist}
License: GPLv2
Url: http://www.cups.org/
Source0: http://www.cups.org/software/%{VERSION}/cups-%{VERSION}-source.tar.bz2
# Pixmap for desktop file
Source2: cupsprinter.png
# Logrotate configuration
Source6: cups.logrotate
# Backend for NCP protocol
Source7: ncp.backend
Source8: macros.cups

Patch1: cups-no-gzip-man.patch
Patch2: cups-system-auth.patch
Patch3: cups-multilib.patch
Patch5: cups-banners.patch
Patch6: cups-serverbin-compat.patch
Patch7: cups-no-export-ssllibs.patch
Patch8: cups-direct-usb.patch
Patch9: cups-lpr-help.patch
Patch10: cups-peercred.patch
Patch11: cups-pid.patch
Patch12: cups-eggcups.patch
Patch13: cups-driverd-timeout.patch
Patch14: cups-strict-ppd-line-length.patch
Patch15: cups-logrotate.patch
Patch16: cups-usb-paperout.patch
Patch17: cups-res_init.patch
Patch18: cups-filter-debug.patch
Patch19: cups-uri-compat.patch
Patch20: cups-str3382.patch
Patch21: cups-0755.patch
Patch22: cups-hp-deviceid-oid.patch
Patch23: cups-dnssd-deviceid.patch
Patch24: cups-ricoh-deviceid-oid.patch
Patch25: cups-systemd-socket.patch
Patch27: cups-avahi-address.patch
Patch28: cups-enum-all.patch
Patch29: cups-dymo-deviceid.patch
Patch30: cups-freebind.patch
Patch31: cups-no-gcry.patch
Patch32: cups-libusb-quirks.patch
Patch33: cups-use-ipp1.1.patch
Patch34: cups-avahi-no-threaded.patch
Patch35: cups-ipp-multifile.patch
Patch36: cups-web-devices-timeout.patch
Patch37: cups-synconclose.patch

Patch100: cups-lspp.patch

Patch101: localization-ppd-option.patch

Requires: %{name}-filesystem = %{epoch}:%{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-client%{?_isa} = %{epoch}:%{version}-%{release}

Provides: cupsddk cupsddk-drivers

BuildRequires: pam-devel pkgconfig
BuildRequires: pkgconfig(gnutls)
BuildRequires: libacl-devel
BuildRequires: openldap-devel
BuildRequires: pkgconfig(libusb-1.0)
BuildRequires: krb5-devel
BuildRequires: pkgconfig(avahi-client)
BuildRequires: systemd
BuildRequires: pkgconfig(libsystemd-daemon) pkgconfig(libsystemd-journal)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: automake

# Make sure we get postscriptdriver tags.
BuildRequires: python-cups

%if %{lspp}
BuildRequires: libselinux-devel
BuildRequires: audit-libs-devel
%endif

Requires: dbus

# Requires working PrivateTmp (bug #807672)
Requires(pre): systemd
Requires(post): systemd
Requires(post): grep, sed
Requires(preun): systemd
Requires(postun): systemd

# We ship udev rules which use setfacl.
Requires: systemd
Requires: acl

# Make sure we have some filters for converting to raster format.
Requires: ghostscript-cups
Requires: cups-filters

%package client
Summary: CUPS printing system - client programs
License: GPLv2
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%if %{use_alternatives}
Provides: /usr/bin/lpq /usr/bin/lpr /usr/bin/lp /usr/bin/cancel /usr/bin/lprm /usr/bin/lpstat
Requires: /usr/sbin/alternatives
%endif
Provides: lpr

%package devel
Summary: CUPS printing system - development environment
License: LGPLv2
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: gnutls-devel
Requires: krb5-devel
Requires: zlib-devel
Provides: cupsddk-devel

%package libs
Summary: CUPS printing system - libraries
License: LGPLv2 and zlib

%package filesystem
Summary: CUPS printing system - directory layout
BuildArch: noarch

%package lpd
Summary: CUPS printing system - lpd emulation
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Provides: lpd

%package ipptool
Summary: CUPS printing system - tool for performing IPP requests
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description
CUPS printing system provides a portable printing layer for
UNIX® operating systems. It has been developed by Apple Inc.
to promote a standard printing solution for all UNIX vendors and users.
CUPS provides the System V and Berkeley command-line interfaces.

%description client
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This package contains command-line client
programs.

%description devel
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This is the development package for creating
additional printer drivers, and other CUPS services.

%description libs
CUPS printing system provides a portable printing layer for
UNIX® operating systems. It has been developed by Apple Inc.
to promote a standard printing solution for all UNIX vendors and users.
CUPS provides the System V and Berkeley command-line interfaces.
The cups-libs package provides libraries used by applications to use CUPS
natively, without needing the lp/lpr commands.

%description filesystem
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This package provides some directories which are
required by other packages that add CUPS drivers (i.e. filters, backends etc.).

%description lpd
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This is the package that provides standard
lpd emulation.

%description ipptool
Sends IPP requests to the specified URI and tests and/or displays the results.

%prep
%setup -q -n cups-%{VERSION}

# Don't gzip man pages in the Makefile, let rpmbuild do it.
%patch1 -p1 -b .no-gzip-man
# Use the system pam configuration.
%patch2 -p1 -b .system-auth
# Prevent multilib conflict in cups-config script.
%patch3 -p1 -b .multilib
# Ignore rpm save/new files in the banners directory.
%patch5 -p1 -b .banners
# Use compatibility fallback path for ServerBin.
%patch6 -p1 -b .serverbin-compat
# Don't export SSLLIBS to cups-config.
%patch7 -p1 -b .no-export-ssllibs
# Allow file-based usb device URIs.
%patch8 -p1 -b .direct-usb
# Add --help option to lpr.
%patch9 -p1 -b .lpr-help
# Fix compilation of peer credentials support.
%patch10 -p1 -b .peercred
# Maintain a cupsd.pid file.
%patch11 -p1 -b .pid
# Fix implementation of com.redhat.PrinterSpooler D-Bus object.
%patch12 -p1 -b .eggcups
# Increase driverd timeout to 70s to accommodate foomatic (bug #744715).
%patch13 -p1 -b .driverd-timeout
# Only enforce maximum PPD line length when in strict mode.
%patch14 -p1 -b .strict-ppd-line-length
# Re-open the log if it has been logrotated under us.
%patch15 -p1 -b .logrotate
# Support for errno==ENOSPACE-based USB paper-out reporting.
%patch16 -p1 -b .usb-paperout
# Re-initialise the resolver on failure in httpAddrGetList() (bug #567353).
%patch17 -p1 -b .res_init
# Log extra debugging information if no filters are available.
%patch18 -p1 -b .filter-debug
# Allow the usb backend to understand old-style URI formats.
%patch19 -p1 -b .uri-compat
# Fix temporary filename creation.
%patch20 -p1 -b .str3382
# Use mode 0755 for binaries and libraries where appropriate.
%patch21 -p1 -b .0755
# Add an SNMP query for HP's device ID OID (STR #3552).
%patch22 -p1 -b .hp-deviceid-oid
# Mark DNS-SD Device IDs that have been guessed at with "FZY:1;".
%patch23 -p1 -b .dnssd-deviceid
# Add an SNMP query for Ricoh's device ID OID (STR #3552).
%patch24 -p1 -b .ricoh-deviceid-oid
# Make cups.service Type=notify (bug #1088918).
%patch25 -p1 -b .systemd-socket
# Use IP address when resolving DNSSD URIs (bug #948288).
%patch27 -p1 -b .avahi-address
# Return from cupsEnumDests() once all records have been returned.
%patch28 -p1 -b .enum-all
# Added IEEE 1284 Device ID for a Dymo device (bug #747866).
%patch29 -p1 -b .dymo-deviceid
# Use IP_FREEBIND socket option when binding listening sockets (bug #970809).
%patch30 -p1 -b .freebind
# Don't link against libgcrypt needlessly.
%patch31 -p1 -b .no-gcry
# Added libusb quirk for Canon PIXMA MP540 (bug #967873).
%patch32 -p1 -b .libusb-quirks
# Default to IPP/1.1 for now (bug #977813).
%patch33 -p1 -b .use-ipp1.1
# Don't use D-Bus from two threads (bug #979748).
%patch34 -p1 -b .avahi-no-threaded
# Fixes for jobs with multiple files and multiple formats.
%patch35 -p1 -b .ipp-multifile
# Increase web interface get-devices timeout to 10s (bug #996664).
%patch36 -p1 -b .web-devices-timeout
# Set the default for SyncOnClose to Yes.
%patch37 -p1 -b .synconclose

%if %{lspp}
# LSPP support.
%patch100 -p1 -b .lspp
%endif

%patch101 -p1

sed -i -e '1iMaxLogSize 0' conf/cupsd.conf.in

# Log to the system journal by default (bug #1078781).
sed -i -e 's,^ErrorLog .*$,ErrorLog syslog,' conf/cups-files.conf.in

# Let's look at the compilation command lines.
perl -pi -e "s,^.SILENT:,," Makedefs.in

f=CREDITS.txt
mv "$f" "$f"~
iconv -f MACINTOSH -t UTF-8 "$f"~ > "$f"
rm -f "$f"~

aclocal -I config-scripts
autoconf -I config-scripts

%build
export CFLAGS="$RPM_OPT_FLAGS -fstack-protector-all -DLDAP_DEPRECATED=1"
# --enable-debug to avoid stripping binaries
%configure --with-docdir=%{_datadir}/%{name}/www --enable-debug \
%if %{lspp}
	--enable-lspp \
%endif
	--with-cupsd-file-perm=0755 \
	--with-log-file-perm=0600 \
	--enable-relro \
	--with-dbusdir=%{_sysconfdir}/dbus-1 \
	--with-php=/usr/bin/php-cgi \
	--enable-avahi \
	--enable-threads \
	--enable-gnutls \
	--enable-webif \
	--with-xinetd=no \
	localedir=%{_datadir}/locale

# If we got this far, all prerequisite libraries must be here.
make %{?_smp_mflags}

%install
make BUILDROOT=%{buildroot} install

rm -rf	%{buildroot}%{_initddir} \
	%{buildroot}%{_sysconfdir}/init.d \
	%{buildroot}%{_sysconfdir}/rc?.d
mkdir -p %{buildroot}%{_unitdir}

find %{buildroot}%{_datadir}/cups/model -name "*.ppd" |xargs gzip -n9f

%if %{use_alternatives}
pushd %{buildroot}%{_bindir}
for i in cancel lp lpq lpr lprm lpstat; do
	mv $i $i.cups
done
cd %{buildroot}%{_sbindir}
mv lpc lpc.cups
cd %{buildroot}%{_mandir}/man1
for i in cancel lp lpq lpr lprm lpstat; do
	mv $i.1 $i-cups.1
done
cd %{buildroot}%{_mandir}/man8
mv lpc.8 lpc-cups.8
popd
%endif

mv %{buildroot}%{_unitdir}/org.cups.cupsd.path %{buildroot}%{_unitdir}/cups.path
mv %{buildroot}%{_unitdir}/org.cups.cupsd.service %{buildroot}%{_unitdir}/cups.service
mv %{buildroot}%{_unitdir}/org.cups.cupsd.socket %{buildroot}%{_unitdir}/cups.socket
mv %{buildroot}%{_unitdir}/org.cups.cups-lpd.socket %{buildroot}%{_unitdir}/cups-lpd.socket
mv %{buildroot}%{_unitdir}/org.cups.cups-lpd@.service %{buildroot}%{_unitdir}/cups-lpd@.service
/bin/sed -i -e "s,org.cups.cupsd,cups,g" %{buildroot}%{_unitdir}/cups.service

mkdir -p %{buildroot}%{_datadir}/pixmaps %{buildroot}%{_sysconfdir}/X11/sysconfig %{buildroot}%{_sysconfdir}/X11/applnk/System %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps
install -p -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/cups
install -p -m 755 %{SOURCE7} %{buildroot}%{cups_serverbin}/backend/ncp

# Ship an rpm macro for where to put driver executables.
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 0644 %{SOURCE8} %{buildroot}%{_rpmconfigdir}/macros.d

# Ship a printers.conf file, and a client.conf file.  That way, they get
# their SELinux file contexts set correctly.
touch %{buildroot}%{_sysconfdir}/cups/printers.conf
touch %{buildroot}%{_sysconfdir}/cups/classes.conf
touch %{buildroot}%{_sysconfdir}/cups/client.conf
touch %{buildroot}%{_sysconfdir}/cups/subscriptions.conf
touch %{buildroot}%{_sysconfdir}/cups/lpoptions

# LSB 3.2 printer driver directory
mkdir -p %{buildroot}%{_datadir}/ppd

# Remove unshipped files.
rm -rf %{buildroot}%{_mandir}/cat? %{buildroot}%{_mandir}/*/cat?
rm -f %{buildroot}%{_datadir}/applications/cups.desktop
rm -rf %{buildroot}%{_datadir}/icons
# there are pdf-banners shipped with cups-filters (#919489)
rm -rf %{buildroot}%{_datadir}/cups/banners
rm -f %{buildroot}%{_datadir}/cups/data/testprint

# install /usr/lib/tmpfiles.d/cups.conf (bug #656566, bug #893834)
mkdir -p ${RPM_BUILD_ROOT}%{_tmpfilesdir}
cat > ${RPM_BUILD_ROOT}%{_tmpfilesdir}/cups.conf <<EOF
# See tmpfiles.d(5) for details

d /run/cups 0755 root lp -
d /run/cups/certs 0511 lp sys -

d /var/spool/cups/tmp - - - 30d
EOF

# /usr/lib/tmpfiles.d/cups-lp.conf (bug #812641)
cat > ${RPM_BUILD_ROOT}%{_tmpfilesdir}/cups-lp.conf <<EOF
# Legacy parallel port character device nodes, to trigger the
# auto-loading of the kernel module on access.
#
# See tmpfiles.d(5) for details

c /dev/lp0 0660 root lp - 6:0
c /dev/lp1 0660 root lp - 6:1
c /dev/lp2 0660 root lp - 6:2
c /dev/lp3 0660 root lp - 6:3
EOF

find %{buildroot} -type f -o -type l | sed '
s:.*\('%{_datadir}'/\)\([^/_]\+\)\(.*\.po$\):%lang(\2) \1\2\3:
/^%lang(C)/d
/^\([^%].*\)/d
' > %{name}.lang

%post
%systemd_post %{name}.path %{name}.socket %{name}.service

# Remove old-style certs directory; new-style is /var/run
# (see bug #194581 for why this is necessary).
rm -rf %{_sysconfdir}/cups/certs
rm -f %{_localstatedir}/cache/cups/*.ipp %{_localstatedir}/cache/cups/*.cache

# Previous migration script unnecessarily put PageLogFormat into cups-files.conf
# (see bug #1148995)
FILE=%{_sysconfdir}/cups/cups-files.conf
for keyword in PageLogFormat; do
    /bin/sed -i -e "s,^$keyword,#$keyword,i" "$FILE" || :
done

# We've been using 'journal' name in our journal.patch for couple releases,
# but upstream decided not to use 'journal', but 'syslog'.
sed -i -e 's,^ErrorLog journal,ErrorLog syslog,' %{_sysconfdir}/cups/cups-files.conf

exit 0

%post client
%if %{use_alternatives}
/usr/sbin/alternatives --install %{_bindir}/lpr print %{_bindir}/lpr.cups 40 \
	 --slave %{_bindir}/lp print-lp %{_bindir}/lp.cups \
	 --slave %{_bindir}/lpq print-lpq %{_bindir}/lpq.cups \
	 --slave %{_bindir}/lprm print-lprm %{_bindir}/lprm.cups \
	 --slave %{_bindir}/lpstat print-lpstat %{_bindir}/lpstat.cups \
	 --slave %{_bindir}/cancel print-cancel %{_bindir}/cancel.cups \
	 --slave %{_sbindir}/lpc print-lpc %{_sbindir}/lpc.cups \
	 --slave %{_mandir}/man1/cancel.1.gz print-cancelman %{_mandir}/man1/cancel-cups.1.gz \
	 --slave %{_mandir}/man1/lp.1.gz print-lpman %{_mandir}/man1/lp-cups.1.gz \
	 --slave %{_mandir}/man8/lpc.8.gz print-lpcman %{_mandir}/man8/lpc-cups.8.gz \
	 --slave %{_mandir}/man1/lpq.1.gz print-lpqman %{_mandir}/man1/lpq-cups.1.gz \
	 --slave %{_mandir}/man1/lpr.1.gz print-lprman %{_mandir}/man1/lpr-cups.1.gz \
	 --slave %{_mandir}/man1/lprm.1.gz print-lprmman %{_mandir}/man1/lprm-cups.1.gz \
	 --slave %{_mandir}/man1/lpstat.1.gz print-lpstatman %{_mandir}/man1/lpstat-cups.1.gz
%endif
exit 0

%post lpd
%systemd_post cups-lpd.socket
exit 0

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%preun
%systemd_preun %{name}.path %{name}.socket %{name}.service
exit 0

%preun client
%if %{use_alternatives}
if [ $1 -eq 0 ] ; then
	/usr/sbin/alternatives --remove print %{_bindir}/lpr.cups
fi
%endif
exit 0

%preun lpd
%systemd_preun cups-lpd.socket
exit 0

%postun
%systemd_postun_with_restart %{name}.path %{name}.socket %{name}.service
exit 0

%postun lpd
%systemd_postun_with_restart cups-lpd.socket
exit 0

%triggerin -- samba-client
ln -sf ../../../bin/smbspool %{cups_serverbin}/backend/smb || :
exit 0

%triggerun -- samba-client
[ $2 = 0 ] || exit 0
rm -f %{cups_serverbin}/backend/smb

%triggerin -- samba4-client
ln -sf %{_bindir}/smbspool %{cups_serverbin}/backend/smb || :
exit 0

%triggerun -- samba4-client
[ $2 = 0 ] || exit 0
rm -f %{cups_serverbin}/backend/smb

%files -f %{name}.lang
%doc README.txt CREDITS.txt CHANGES.txt
%dir %attr(0755,root,lp) %{_sysconfdir}/cups
%dir %attr(0755,root,lp) %{_localstatedir}/run/cups
%dir %attr(0511,lp,sys) %{_localstatedir}/run/cups/certs
%{_tmpfilesdir}/cups.conf
%{_tmpfilesdir}/cups-lp.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) %{_sysconfdir}/cups/cupsd.conf
%attr(0640,root,lp) %{_sysconfdir}/cups/cupsd.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) %{_sysconfdir}/cups/cups-files.conf
%attr(0640,root,lp) %{_sysconfdir}/cups/cups-files.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/client.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0600,root,lp) %{_sysconfdir}/cups/classes.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0600,root,lp) %{_sysconfdir}/cups/printers.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/snmp.conf
%attr(0640,root,lp) %{_sysconfdir}/cups/snmp.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/subscriptions.conf
%{_sysconfdir}/cups/interfaces
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) %{_sysconfdir}/cups/lpoptions
%dir %attr(0755,root,lp) %{_sysconfdir}/cups/ppd
%dir %attr(0700,root,lp) %{_sysconfdir}/cups/ssl
%config(noreplace) %{_sysconfdir}/pam.d/cups
%config(noreplace) %{_sysconfdir}/logrotate.d/cups
%dir %{_datadir}/%{name}/www
%dir %{_datadir}/%{name}/www/de
%dir %{_datadir}/%{name}/www/es
%dir %{_datadir}/%{name}/www/ja
%dir %{_datadir}/%{name}/www/ru
%{_datadir}/%{name}/www/images
%{_datadir}/%{name}/www/*.css
%doc %{_datadir}/%{name}/www/index.html
%doc %{_datadir}/%{name}/www/help
%doc %{_datadir}/%{name}/www/robots.txt
%doc %{_datadir}/%{name}/www/de/index.html
%doc %{_datadir}/%{name}/www/es/index.html
%doc %{_datadir}/%{name}/www/ja/index.html
%doc %{_datadir}/%{name}/www/ru/index.html
%doc %{_datadir}/%{name}/www/apple-touch-icon.png
%dir %{_datadir}/%{name}/usb
%{_datadir}/%{name}/usb/org.cups.usb-quirks
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_unitdir}/%{name}.path
%{_bindir}/cupstestppd
%{_bindir}/cupstestdsc
%{_bindir}/ppd*
%{cups_serverbin}/backend/*
%{cups_serverbin}/cgi-bin
%dir %{cups_serverbin}/daemon
%{cups_serverbin}/daemon/cups-deviced
%{cups_serverbin}/daemon/cups-driverd
%{cups_serverbin}/daemon/cups-exec
%{cups_serverbin}/notifier
%{cups_serverbin}/filter/*
%{cups_serverbin}/monitor
%{_mandir}/man[1578]/*
# client subpackage
%exclude %{_mandir}/man1/lp*.1.gz
%exclude %{_mandir}/man1/cancel-cups.1.gz
%exclude %{_mandir}/man8/lpc-cups.8.gz
# devel subpackage
%exclude %{_mandir}/man1/cups-config.1.gz
# ipptool subpackage
%exclude %{_mandir}/man1/ipptool.1.gz
%exclude %{_mandir}/man5/ipptoolfile.5.gz
# lpd subpackage
%exclude %{_mandir}/man8/cups-lpd.8.gz
%{_sbindir}/*
# client subpackage
%exclude %{_sbindir}/lpc.cups
%dir %{_datadir}/cups/templates
%dir %{_datadir}/cups/templates/de
%dir %{_datadir}/cups/templates/es
%dir %{_datadir}/cups/templates/ja
%dir %{_datadir}/cups/templates/ru
%{_datadir}/cups/templates/*.tmpl
%{_datadir}/cups/templates/de/*.tmpl
%{_datadir}/cups/templates/es/*.tmpl
%{_datadir}/cups/templates/ja/*.tmpl
%{_datadir}/cups/templates/ru/*.tmpl
%dir %attr(1770,root,lp) %{_localstatedir}/spool/cups/tmp
%dir %attr(0710,root,lp) %{_localstatedir}/spool/cups
%dir %attr(0755,lp,sys) %{_localstatedir}/log/cups
%{_datadir}/pixmaps/cupsprinter.png
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/cups.conf
%{_datadir}/cups/drv/sample.drv
%{_datadir}/cups/examples
%{_datadir}/cups/mime/mime.types
%{_datadir}/cups/mime/mime.convs
%{_datadir}/cups/ppdc/*.defs
%{_datadir}/cups/ppdc/*.h

%files client
%{_sbindir}/lpc.cups
%{_bindir}/cancel*
%{_bindir}/lp*
%{_mandir}/man1/lp*.1.gz
%{_mandir}/man1/cancel-cups.1.gz
%{_mandir}/man8/lpc-cups.8.gz

%files libs
%doc LICENSE.txt
%{_libdir}/*.so.*

%files filesystem
%dir %{cups_serverbin}
%dir %{cups_serverbin}/backend
%dir %{cups_serverbin}/driver
%dir %{cups_serverbin}/filter
%dir %{_datadir}/cups
#%%dir %%{_datadir}/cups/banners
#%%dir %%{_datadir}/cups/charsets
%dir %{_datadir}/cups/data
%dir %{_datadir}/cups/drv
%dir %{_datadir}/cups/mime
%dir %{_datadir}/cups/model
%dir %{_datadir}/cups/ppdc
%dir %{_datadir}/ppd

%files devel
%{_bindir}/cups-config
%{_libdir}/*.so
%{_includedir}/cups
%{_mandir}/man1/cups-config.1.gz
%{_rpmconfigdir}/macros.d/macros.cups

%files lpd
%{_unitdir}/cups-lpd.socket
%{_unitdir}/cups-lpd@.service
%{cups_serverbin}/daemon/cups-lpd
%{_mandir}/man8/cups-lpd.8.gz

%files ipptool
%{_bindir}/ipptool
%{_bindir}/ippfind
%dir %{_datadir}/cups/ipptool
%{_datadir}/cups/ipptool/*
%{_mandir}/man1/ipptool.1.gz
%{_mandir}/man5/ipptoolfile.5.gz

%changelog
* Wed Dec 30 2015 xiaotian.wu@i-soft.com.cn - 1:2.1.0-3
- localization ppd option.patch to fix bug 13114

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:2.1.0-2
- Rebuild for new 4.0 release.

