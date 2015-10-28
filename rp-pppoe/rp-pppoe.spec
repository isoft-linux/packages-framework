Name: rp-pppoe
Version: 3.11
Release: 15%{?dist}
Summary: A PPP over Ethernet client (for xDSL support).
License: GPLv2+
Url: http://www.roaringpenguin.com/pppoe/

Source: http://www.roaringpenguin.com/files/download/rp-pppoe-%{version}.tar.gz
Source1: pppoe-connect
Source2: pppoe-setup
Source3: pppoe-start
Source4: pppoe-status
Source5: pppoe-stop
Source6: pppoe-server.service

Patch0: rp-pppoe-3.8-redhat.patch
Patch1: rp-pppoe-3.11-ip-allocation.patch

BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: coreutils
BuildRequires: ppp-devel
BuildRequires: systemd

Requires: ppp >= 2.4.6
Requires: iproute >= 2.6
Requires: coreutils
Requires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# _pkgdocdir is available in rhel >= 6 and fedora >= 20
# This line can be removed once f19 is EOL.
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. This package contains the
Roaring Penguin PPPoE client, a user-mode program that does not
require any kernel modifications. It is fully compliant with RFC 2516,
the official PPPoE specification.

%prep
%setup -q
%patch0 -p1 -b .config
%patch1 -p1 -b .ip-allocation

# configure honors docdir, but Makefile.in doesn't
sed -i -e 's,^docdir=.*$,docdir=@docdir@,' src/Makefile.in

%build
cd src
autoconf
export CFLAGS="%{optflags} -D_GNU_SOURCE -fno-strict-aliasing"
%configure --docdir=%{_pkgdocdir}
make

%install
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_unitdir}

make -C src install DESTDIR=%{buildroot}

install -m 0755 %{SOURCE1} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE2} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE3} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE4} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE5} %{buildroot}%{_sbindir}
install -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/pppoe-server.service

ln -sf pppoe-stop %{buildroot}%{_sbindir}/adsl-stop
ln -sf pppoe-start %{buildroot}%{_sbindir}/adsl-start

rm -rf %{buildroot}/etc/ppp/pppoe.conf \
       %{buildroot}/etc/rc.d/init.d/pppoe \
       %{buildroot}%{_sysconfdir}/ppp/plugins

%post
%systemd_post pppoe-server.service

%preun
%systemd_preun pppoe-server.service

%postun
%systemd_postun_with_restart pppoe-server.service

%files
%doc scripts/pppoe-connect scripts/pppoe-setup scripts/pppoe-init
%doc scripts/pppoe-start scripts/pppoe-status scripts/pppoe-stop
%doc configs
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%config(noreplace) %{_sysconfdir}/ppp/firewall*
%{_unitdir}/pppoe-server.service
%{_sbindir}/*
%{_mandir}/man?/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.11-15
- Rebuild for new 4.0 release.

