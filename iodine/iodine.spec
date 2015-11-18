Name: iodine
Version: 0.7.0
Release: 5%{?dist}
Summary: Solution to tunnel IPv4 data through a DNS server
License: ISC
URL: http://code.kryo.se/iodine/
Source0: http://code.kryo.se/%{name}/%{name}-%{version}%{?prerel}.tar.gz

Source1: %{name}-client.conf
Source2: %{name}-server.conf

Source5: %{name}.logrotate.client
Source6: %{name}.logrotate.server

Source7: %{name}-client.service
Source8: %{name}-server.service

# http://dev.kryo.se/iodine/ticket/119
Patch1: iodine-0.7.0.split-man.patch

BuildRequires: zlib-devel
BuildRequires: systemd

Requires: %{name}-client
Requires: %{name}-server

%description
iodine lets you tunnel IPv4 data through a DNS server. This can be usable in
different situations where internet access is firewalled, but DNS queries are
allowed.

It runs on Linux, Mac OS X, FreeBSD, NetBSD, OpenBSD and Windows and needs a
TUN/TAP device. The bandwidth is asymmetrical with limited upstream and up to
1 Mbit/s downstream.

%package client
Summary: Client part of solution to tunnel IPv4 data through a DNS server
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Provides: bundled(md5-deutsch)

%description client
iodine lets you tunnel IPv4 data through a DNS server. This can be usable in
different situations where internet access is firewalled, but DNS queries are
allowed.

It runs on Linux, Mac OS X, FreeBSD, NetBSD, OpenBSD and Windows and needs a
TUN/TAP device. The bandwidth is asymmetrical with limited upstream and up to
1 Mbit/s downstream.

This is the client part of iodine sulution.

%package server
Summary: Server part of solution to tunnel IPv4 data through a DNS server
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: net-tools
Provides: bundled(md5-deutsch)

%description server
iodine lets you tunnel IPv4 data through a DNS server. This can be usable in
different situations where internet access is firewalled, but DNS queries are
allowed.

It runs on Linux, Mac OS X, FreeBSD, NetBSD, OpenBSD and Windows and needs a
TUN/TAP device. The bandwidth is asymmetrical with limited upstream and up to
1 Mbit/s downstream.

This is the server part of iodine solution.

%prep
%setup -q -n %{name}-%{version}%{?prerel}
%patch1 -p1 -b .split-man

%build
# It is fail to build without -c gcc flag (comes from upstream Makefile).
make %{?_smp_mflags} prefix=%{_prefix} CFLAGS="-c %{optflags} -DLINUX"

%install
make install prefix=%{buildroot}%{_prefix}

install -Dp -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-client
install -Dp -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-server

install -Dp -m 0644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}-client
install -Dp -m 0644 %{SOURCE6} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}-server

install -Dp -m 0644 %{SOURCE7} %{buildroot}/%{_unitdir}/%{name}-client.service
install -Dp -m 0644 %{SOURCE8} %{buildroot}/%{_unitdir}/%{name}-server.service

%post client
%systemd_post %{name}-client.service

%preun client
%systemd_preun %{name}-client.service

%postun client
%systemd_postun_with_restart %{name}-client.service

%post server
%systemd_post %{name}-server.service

%preun server
%systemd_preun %{name}-server.service

%postun server
%systemd_postun_with_restart %{name}-server.service

%files client
%{_sbindir}/%{name}
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}-client
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-client
%{_mandir}/man8/%{name}.8.gz
%{_unitdir}/%{name}-client.service

%files server
%{_sbindir}/%{name}d
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}-server
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-server
%{_mandir}/man8/%{name}d.8.gz
%{_unitdir}/%{name}-server.service

%changelog
* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 0.7.0-5
- Rebuild

