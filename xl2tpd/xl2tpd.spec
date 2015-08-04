%global commit 5619e1771048e74b729804e8602f409af0f3faea

Summary: Layer 2 Tunnelling Protocol Daemon (RFC 2661)
Name: xl2tpd
Version: 1.3.6
Release: 9%{?dist}
License: GPL+
Url: https://github.com/xelerance/%{name}/
Group: System Environment/Daemons
Source0: https://github.com/xelerance/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Source1: xl2tpd.service
Source2: tmpfiles-xl2tpd.conf
Patch1: xl2tpd-1.3.6-conf.patch
Patch2: xl2tpd-1.3.6-md5-fips.patch
Patch3: xl2tpd-1.3.6-saref.patch

Requires: ppp >= 2.4.5-18
# If you want to authenticate against a Microsoft PDC/Active Directory
# Requires: samba-winbind
BuildRequires: libpcap-devel
BuildRequires: systemd-units
BuildRequires: openssl-devel
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
xl2tpd is an implementation of the Layer 2 Tunnelling Protocol (RFC 2661).
L2TP allows you to tunnel PPP over UDP. Some ISPs use L2TP to tunnel user
sessions from dial-in servers (modem banks, ADSL DSLAMs) to back-end PPP
servers. Another important application is Virtual Private Networks where
the IPsec protocol is used to secure the L2TP connection (L2TP/IPsec,
RFC 3193). The L2TP/IPsec protocol is mainly used by Windows and 
Mac OS X clients. On Linux, xl2tpd can be used in combination with IPsec
implementations such as Openswan.
Example configuration files for such a setup are included in this RPM.

xl2tpd works by opening a pseudo-tty for communicating with pppd.
It runs completely in userspace.

xl2tpd supports IPsec SA Reference tracking to enable overlapping internak
NAT'ed IP's by different clients (eg all clients connecting from their
linksys internal IP 192.168.1.101) as well as multiple clients behind
the same NAT router.

xl2tpd supports the pppol2tp kernel mode operations on 2.6.23 or higher,
or via a patch in contrib for 2.4.x kernels.

Xl2tpd is based on the 0.69 L2TP by Jeff McAdams <jeffm@iglou.com>
It was de-facto maintained by Jacco de Leeuw <jacco2@dds.nl> in 2002 and 2003.

%prep
%setup -qn %{name}-%{commit}
%patch1 -p1 
%patch2 -p1
%patch3 -p1

%build
#make DFLAGS="$RPM_OPT_FLAGS -g -DDEBUG_HELLO -DDEBUG_CLOSE -DDEBUG_FLOW -DDEBUG_PAYLOAD -DDEBUG_CONTROL -DDEBUG_CONTROL_XMIT -DDEBUG_FLOW_MORE -DDEBUG_MAGIC -DDEBUG_ENTROPY -DDEBUG_HIDDEN -DDEBUG_PPPD -DDEBUG_AAA -DDEBUG_FILE -DDEBUG_FLOW -DDEBUG_HELLO -DDEBUG_CLOSE -DDEBUG_ZLB -DDEBUG_AUTH"

export CFLAGS="$CFLAGS -fPIC -Wall -DTRUST_PPPD_TO_DIE"
export DFLAGS="$RPM_OPT_FLAGS -g "
export LDFLAGS="$LDFLAGS -pie -Wl,-z,relro -Wl,-z,now"
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install
install -d 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xl2tpd.service
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d/
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf

install -p -D -m644 examples/xl2tpd.conf %{buildroot}%{_sysconfdir}/xl2tpd/xl2tpd.conf
install -p -D -m644 examples/ppp-options.xl2tpd %{buildroot}%{_sysconfdir}/ppp/options.xl2tpd
install -p -D -m600 doc/l2tp-secrets.sample %{buildroot}%{_sysconfdir}/xl2tpd/l2tp-secrets
install -p -D -m600 examples/chapsecrets.sample %{buildroot}%{_sysconfdir}/ppp/chap-secrets.sample
install -p -D -m755 -d %{buildroot}%{_localstatedir}/run/xl2tpd

%preun
%systemd_preun xl2tpd.service

%post
%systemd_post xl2tpd.service

%postun
%systemd_postun_with_restart xl2tpd.service 

%files
%doc BUGS CHANGES CREDITS LICENSE README.* TODO doc/rfc2661.txt 
%doc doc/README.patents examples/chapsecrets.sample
%{_sbindir}/xl2tpd
%{_sbindir}/xl2tpd-control
%{_bindir}/pfc
%{_mandir}/*/*
%dir %{_sysconfdir}/xl2tpd
%config(noreplace) %{_sysconfdir}/xl2tpd/*
%config(noreplace) %{_sysconfdir}/ppp/*
%dir %{_localstatedir}/run/xl2tpd
%{_unitdir}/%{name}.service
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%ghost %attr(0600,root,root) %{_localstatedir}/run/xl2tpd/l2tp-control

%changelog
