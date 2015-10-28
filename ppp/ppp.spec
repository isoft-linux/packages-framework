%global _hardened_build 1

%define libpcap_ver 1.5.3


Summary: The Point-to-Point Protocol daemon
Name: ppp
Version: 2.4.6
Release: 5
License: BSD and LGPLv2+ and GPLv2+ and Public Domain
URL: http://www.samba.org/ppp
Source0: ftp://ftp.samba.org/pub/ppp/ppp-%{version}.tar.gz
Source1: ppp-pam.conf
Source3: ppp-tmpfiles.conf
Source4: ip-down
Source5: ip-down.ipv6to4
Source6: ip-up
Source7: ip-up.ipv6to4
Source8: ipv6-down
Source9: ipv6-up
Source10: ifup-ppp
Source11: ifdown-ppp
Source12: ppp-watch.tar.xz

Patch0001: 0001-build-sys-use-gcc-as-our-compiler-of-choice.patch
Patch0002: 0002-build-sys-enable-PAM-support.patch
Patch0003: 0003-build-sys-utilize-compiler-flags-handed-to-us-by-rpm.patch
Patch0004: 0004-doc-add-configuration-samples.patch
Patch0005: 0005-build-sys-don-t-hardcode-LIBDIR-but-set-it-according.patch
Patch0006: 0006-scritps-use-change_resolv_conf-function.patch
Patch0007: 0007-build-sys-don-t-strip-binaries-during-installation.patch
Patch0008: 0008-build-sys-use-prefix-usr-instead-of-usr-local.patch
Patch0009: 0009-pppd-introduce-ipv6-accept-remote.patch
Patch0010: 0010-build-sys-enable-CBCP.patch
Patch0011: 0011-build-sys-don-t-put-connect-errors-log-to-etc-ppp.patch
Patch0012: 0012-pppd-we-don-t-want-to-accidentally-leak-fds.patch
Patch0013: 0013-everywhere-O_CLOEXEC-harder.patch
Patch0014: 0014-everywhere-use-SOCK_CLOEXEC-when-creating-socket.patch
Patch0015: 0015-pppd-move-pppd-database-to-var-run-ppp.patch
Patch0016: 0016-rp-pppoe-add-manpage-for-pppoe-discovery.patch
Patch0017: 0017-pppd-rebase-EAP-TLS-patch-v0.994.patch
Patch0018: 0018-scritps-fix-ip-up.local-sample.patch
Patch0019: 0019-sys-linux-rework-get_first_ethernet.patch
Patch0020: 0020-pppd-put-lock-files-in-var-lock-ppp.patch
Patch0021: 0021-build-sys-compile-pppol2tp-plugin-with-RPM_OPT_FLAGS.patch
Patch0022: 0022-build-sys-compile-pppol2tp-with-multilink-support.patch
Patch0023: 0023-build-sys-install-rp-pppoe-plugin-files-with-standar.patch
Patch0024: 0024-build-sys-install-pppoatm-plugin-files-with-standard.patch
Patch0025: 0025-pppd-install-pppd-binary-using-standard-perms-755.patch

#enable internal libpcap
Patch0100: ppp-enable-internal-libpcap.patch

Patch0101: ppp-musl-fix-headers.patch

Source1000: http://www.tcpdump.org/release/libpcap-%{libpcap_ver}.tar.gz
Patch1000: libpcap-man.patch

BuildRequires: pam-devel, openssl-devel, systemd, systemd-devel, glib2-devel
Requires: glibc, /etc/pam.d/system-auth, systemd
Requires(pre): /usr/bin/getent
Requires(pre): /usr/sbin/groupadd

%description
The ppp package contains the PPP (Point-to-Point Protocol) daemon and
documentation for PPP support. The PPP protocol provides a method for
transmitting datagrams over serial point-to-point links. PPP is
usually used to dial in to an ISP (Internet Service Provider) or other
organization over a modem and phone line.

%package devel
Summary: Headers for ppp plugin development

%description devel
This package contains the header files for building plugins for ppp.

%prep
%setup -q -a1000
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1
%patch0021 -p1
%patch0022 -p1
%patch0023 -p1
%patch0024 -p1
%patch0025 -p1
%patch0100 -p1
%patch0101 -p1
tar -xJf %{SOURCE12}


pushd libpcap-%{libpcap_ver}
%patch1000 -p1
popd

%build
pushd libpcap-%{libpcap_ver}
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fPIC" ./configure --prefix=`pwd`/../interbin --disable-bluetooth --disable-shared --enable-static
make %{?_smp_mflags}
make install
popd

rm -rf interbin/lib/*.so*

export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC -Wall"

%configure
make %{?_smp_mflags}
make -C ppp-watch %{?_smp_mflags}

%install
make INSTROOT=%{buildroot} install install-etcppp
install -D -m0644 include/net/ppp_defs.h $RPM_BUILD_ROOT%{_includedir}/net/ppp_defs.h

find scripts -type f | xargs chmod a-x
make ROOT=%{buildroot} -C ppp-watch install

# create log files dir
install -d %{buildroot}%{_localstatedir}/log/ppp

# install pam config
install -d %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/ppp

# install tmpfiles drop-in
install -d %{buildroot}%{_tmpfilesdir}
install -p %{SOURCE3} %{buildroot}%{_tmpfilesdir}/ppp.conf

# install scripts (previously owned by initscripts package)
install -d %{buildroot}%{_sysconfdir}/ppp
install -p %{SOURCE4} %{buildroot}%{_sysconfdir}/ppp/ip-down
install -p %{SOURCE5} %{buildroot}%{_sysconfdir}/ppp/ip-down.ipv6to4
install -p %{SOURCE6} %{buildroot}%{_sysconfdir}/ppp/ip-up
install -p %{SOURCE7} %{buildroot}%{_sysconfdir}/ppp/ip-up.ipv6to4
install -p %{SOURCE8} %{buildroot}%{_sysconfdir}/ppp/ipv6-down
install -p %{SOURCE9} %{buildroot}%{_sysconfdir}/ppp/ipv6-up

install -d %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/
install -p %{SOURCE10} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ppp
install -p %{SOURCE11} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifdown-ppp

%pre
/usr/bin/getent group dip >/dev/null 2>&1 || /usr/sbin/groupadd -r -g 40 dip >/dev/null 2>&1 || :

%post
%tmpfiles_create ppp.conf

%files
%defattr(-,root,root)
%{_sbindir}/chat
%{_sbindir}/pppd
%{_sbindir}/pppdump
%{_sbindir}/pppoe-discovery
%{_sbindir}/pppstats
%{_sbindir}/ppp-watch
%dir %{_sysconfdir}/ppp
%{_sysconfdir}/ppp/ip-up
%{_sysconfdir}/ppp/ip-down
%{_sysconfdir}/ppp/ip-up.ipv6to4
%{_sysconfdir}/ppp/ip-down.ipv6to4
%{_sysconfdir}/ppp/ipv6-up
%{_sysconfdir}/ppp/ipv6-down
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ppp
%{_sysconfdir}/sysconfig/network-scripts/ifup-ppp
%{_mandir}/man8/chat.8*
%{_mandir}/man8/pppd.8*
%{_mandir}/man8/pppdump.8*
%{_mandir}/man8/pppd-radattr.8*
%{_mandir}/man8/pppd-radius.8*
%{_mandir}/man8/pppstats.8*
%{_mandir}/man8/pppoe-discovery.8*
%{_mandir}/man8/ppp-watch.8*
%{_libdir}/pppd
%ghost %dir /run/ppp
%ghost %dir /run/lock/ppp
%attr(700, root, root) %dir %{_localstatedir}/log/ppp
%config(noreplace) %{_sysconfdir}/ppp/eaptls-client
%config(noreplace) %{_sysconfdir}/ppp/eaptls-server
%config(noreplace) %{_sysconfdir}/ppp/chap-secrets
%config(noreplace) %{_sysconfdir}/ppp/options
%config(noreplace) %{_sysconfdir}/ppp/pap-secrets
%config(noreplace) %{_sysconfdir}/pam.d/ppp
%{_tmpfilesdir}/ppp.conf

%files devel
%defattr(-,root,root)
%{_includedir}/pppd
#%{_includedir}/net/ppp_defs.h
%doc PLUGINS

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.4.6-5
- Rebuild for new 4.0 release.

