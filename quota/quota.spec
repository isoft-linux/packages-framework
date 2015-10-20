#allow remote set quota by defined rpcsetquota to 1(set to 0 to disabled it)
%{!?rpcsetquota:%define rpcsetquota 1}

Name: quota
Epoch: 1
Version: 4.02
Release: 4%{?dist}
Summary: System administration tools for monitoring users' disk usage
# quota_nld.c, quotaio_xfs.h:       GPLv2
# bylabel.c copied from util-linux: GPLv2+
# svc_socket.c copied from glibc:   LGPLv2+
# doc/quotas.ms, quotaops.c, quot.c, quotaon.c, edquota.c, quot.h, quota.c,
# quotaio_v1.c:                     BSD
License: BSD and LGPLv2+ and GPLv2 and GPLv2+
Group: System Environment/Base
URL: http://sourceforge.net/projects/linuxquota/
Source0: http://downloads.sourceforge.net/linuxquota/%{name}-%{version}.tar.gz
Source1: quota_nld.service
Source2: quota_nld.sysconfig
Source3: rpc-rquotad.service
Source4: rpc-rquotad.sysconfig
# Not accepted changes (378a64006bb1e818e84a1c77808563b802b028fa)
# Some of the lines have been superseded by other commits probably.
Patch0: quota-4.02-warnquota.patch
Patch1: quota-4.02-Build-rpc.rquotad-as-PIE.patch
Patch2: quota-3.13-wrong-ports.patch
BuildRequires: dbus-devel
BuildRequires: e2fsprogs-devel
BuildRequires: gettext
BuildRequires: openldap-devel
BuildRequires: pkgconfig(libnl-3.0) >= 3.1
BuildRequires: pkgconfig(libnl-genl-3.0)
BuildRequires: systemd
BuildRequires: tcp_wrappers-devel
Requires: tcp_wrappers
Requires: quota-nls = %{epoch}:%{version}-%{release}
Conflicts: kernel < 2.4

%description
The quota package contains system administration tools for monitoring
and limiting user and or group disk usage per file system.


%package nld
Group: System Environment/Daemons
Summary: quota_nld daemon
Requires: quota-nls = %{epoch}:%{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description nld
Daemon that listens on netlink socket and processes received quota warnings.
Note, that you have to enable the kernel support for sending quota messages
over netlink (in Filesystems->Quota menu). The daemon supports forwarding
warning messages to the system D-Bus (so that desktop manager can display
a dialog) and writing them to the terminal user has last accessed.


%package rpc
Group: System Environment/Daemons
Summary: RPC quota daemon
Requires: quota-nls = %{epoch}:%{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Conflicts: quota < 1:4.02-3

%description rpc
The RPC daemon allows to query and set disk quotas over network. If you run
the deamon on NFS server, you could use quota tools to manage the quotas from
NFS client.


%package warnquota
Group: System Environment/Base
Summary: Send e-mail to users over quota
Requires: quota-nls = %{epoch}:%{version}-%{release}

%description warnquota
Utility that checks disk quota for each local file system and mails a warning
message to those users who have reached their soft limit.  It is typically run
via cron(8).


%package nls
Group: System Environment/Base
Summary: Gettext catalogs for disk quota tools
BuildArch: noarch

%description nls
Disk quota tools messages translated into different natural languages.


%package devel
Group: Development/Libraries
Summary: Development files for quota
Requires: quota =  %{epoch}:%{version}-%{release}

%description devel
The quota package contains system administration tools for monitoring
and limiting user and or group disk usage per file system.

This package contains development header files for implementing quotas
on remote machines.


%package doc
Group: Documentation
Summary: Additional documentation for disk quotas
Requires: quota =  %{epoch}:%{version}-%{release}
BuildArch: noarch
AutoReq: 0

%description doc
This package contains additional documentation for disk quotas concept in
Linux/UNIX environment.


%prep
%setup -q -n quota-tools
%patch0 -p1
%ifnarch ppc ppc64
%patch1 -p1
%endif
%patch2 -p1


%build
%global _hardened_build 1
%configure \
    --enable-ext2direct=yes \
    --enable-ldapmail=yes \
    --enable-netlink=yes \
    --enable-rootsbin=no \
%if %{rpcsetquota}
    --enable-rpcsetquota=yes \
%endif
    --enable-strip-binaries=no
make


%install
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/{man1,man3,man5,man8}
make install INSTALL='install -p' ROOTDIR=%{buildroot}
install -m 644 warnquota.conf %{buildroot}%{_sysconfdir}
ln -s  quotaon.8.gz \
  %{buildroot}%{_mandir}/man8/quotaoff.8

install -p -m644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/quota_nld.service
install -p -m644 -D %{SOURCE2} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/quota_nld
install -p -m644 -D %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/rpc-rquotad.service
install -p -m644 -D %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rpc-rquotad

%find_lang %{name}


%post nld
%systemd_post quota_nld.service

%preun nld
%systemd_preun quota_nld.service

%postun nld
%systemd_postun_with_restart quota_nld.service


%post rpc
%systemd_post rpc-rquotad.service

%preun rpc
%systemd_preun rpc-rquotad.service

%postun rpc
%systemd_postun_with_restart rpc-rquotad.service


%files
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/*
%exclude %{_sbindir}/quota_nld
%exclude %{_sbindir}/rpc.rquotad
%exclude %{_sbindir}/warnquota
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man8/*
%exclude %{_mandir}/man8/quota_nld.8*
%exclude %{_mandir}/man8/rpc.rquotad.8*
%exclude %{_mandir}/man8/warnquota.8*
%doc Changelog

%files nld
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/quota_nld
%{_unitdir}/quota_nld.service
%attr(0755,root,root) %{_sbindir}/quota_nld
%attr(0644,root,root) %{_mandir}/man8/quota_nld.8*
%doc Changelog

%files rpc
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/rpc-rquotad
%{_unitdir}/rpc-rquotad.service
%{_sbindir}/rpc.rquotad
%{_mandir}/man8/rpc.rquotad.8*
%doc Changelog

%files warnquota
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/quotagrpadmins
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/quotatab
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/warnquota.conf
%attr(0755,root,root) %{_sbindir}/warnquota
%attr(0644,root,root) %{_mandir}/man5/*
%attr(0644,root,root) %{_mandir}/man8/warnquota.8*
%doc Changelog README.ldap-support README.mailserver

%files nls -f %{name}.lang
%doc Changelog

%files devel
%dir %{_includedir}/rpcsvc
%{_includedir}/rpcsvc/*
%attr(0644,root,root) %{_mandir}/man3/*

%files doc
%doc doc/* ldap-scripts


%changelog
