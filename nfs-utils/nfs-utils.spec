Summary: NFS utilities and supporting clients and daemons for the kernel NFS server
Name: nfs-utils
URL: http://sourceforge.net/projects/nfs
Version: 1.3.2
Release: 11%{?dist}
Epoch: 1

# group all 32bit related archs
%define all_32bit_archs i386 i486 i586 i686 athlon ppc sparcv9

Source0: https://www.kernel.org/pub/linux/utils/nfs-utils/%{version}/%{name}-%{version}.tar.xz

Source1: id_resolver.conf
Source2: nfs.sysconfig
Source3: nfs-utils_env.sh
Source4: lockd.conf

Patch001: nfs-utils-1.3.3-rc5.patch

Patch100: nfs-utils-1.2.1-statdpath-man.patch
Patch101: nfs-utils-1.2.1-exp-subtree-warn-off.patch
Patch102: nfs-utils-1.2.3-sm-notify-res_init.patch
Patch103: nfs-utils-1.2.5-idmap-errmsg.patch
Patch104: nfs-utils-1.3.2-systemd-gssargs.patch

Provides: exportfs    = %{epoch}:%{version}-%{release}
Provides: nfsstat     = %{epoch}:%{version}-%{release}
Provides: showmount   = %{epoch}:%{version}-%{release}
Provides: rpcdebug    = %{epoch}:%{version}-%{release}
Provides: rpc.idmapd  = %{epoch}:%{version}-%{release}
Provides: rpc.mountd  = %{epoch}:%{version}-%{release}
Provides: rpc.nfsd    = %{epoch}:%{version}-%{release}
Provides: rpc.statd   = %{epoch}:%{version}-%{release}
Provides: rpc.gssd    = %{epoch}:%{version}-%{release}
Provides: mount.nfs   = %{epoch}:%{version}-%{release}
Provides: mount.nfs4  = %{epoch}:%{version}-%{release}
Provides: umount.nfs  = %{epoch}:%{version}-%{release}
Provides: umount.nfs4 = %{epoch}:%{version}-%{release}
Provides: sm-notify   = %{epoch}:%{version}-%{release}
Provides: start-statd = %{epoch}:%{version}-%{release}

License: MIT and GPLv2 and GPLv2+ and BSD
Requires: rpcbind, sed, gawk, sh-utils, fileutils, textutils, grep
Requires: kmod, keyutils, quota
BuildRequires: libevent-devel libcap-devel
BuildRequires: libnfsidmap-devel libtirpc-devel libblkid-devel
BuildRequires: krb5-libs >= 1.4 autoconf >= 2.57 openldap-devel >= 2.2
BuildRequires: automake, libtool, glibc-headers, device-mapper-devel
BuildRequires: krb5-devel, tcp_wrappers-devel, libmount-devel
BuildRequires: sqlite-devel
Requires(pre): shadow-utils >= 4.0.3-25
Requires(pre): /sbin/nologin
Requires: libnfsidmap libevent
Requires: libtirpc >= 0.2.3-1 libblkid libcap libmount
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: gssproxy => 0.3.0-0

%description
The nfs-utils package provides a daemon for the kernel NFS server and
related tools, which provides a much higher level of performance than the
traditional Linux NFS server used by most users.

This package also contains the showmount program.  Showmount queries the
mount daemon on a remote host for information about the NFS (Network File
System) server on the remote host.  For example, showmount can display the
clients which are mounted on that host.

This package also contains the mount.nfs and umount.nfs program.

%prep
%setup -q

%patch001 -p1

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1

# Remove .orig files
find . -name "*.orig" | xargs rm -f

%build

%ifarch s390 s390x sparcv9 sparc64
PIE="-fPIE"
%else
PIE="-fpie"
%endif
export PIE

sh -x autogen.sh

CFLAGS="`echo $RPM_OPT_FLAGS $ARCH_OPT_FLAGS $PIE -D_FILE_OFFSET_BITS=64`"

%define _statdpath /var/lib/nfs/statd
%configure \
    CFLAGS="$CFLAGS" \
    CPPFLAGS="$DEFINES" \
    LDFLAGS="-pie" \
    --enable-mountconfig \
    --enable-ipv6 \
	--with-statdpath=%{_statdpath} \
	--enable-libmount-mount

make %{?_smp_mflags} all

%install
rm -rf $RPM_BUILD_ROOT/*

mkdir -p $RPM_BUILD_ROOT%/sbin
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}/nfs.target.wants
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/request-key.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/
make DESTDIR=$RPM_BUILD_ROOT install
install -s -m 755 tools/rpcdebug/rpcdebug $RPM_BUILD_ROOT%{_sbindir}
install -m 644 utils/mount/nfsmount.conf  $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/request-key.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nfs

for file in systemd/*.service  ; do
	install -m 644 $file $RPM_BUILD_ROOT%{_unitdir}
done
for file in systemd/*.target  ; do
	install -m 644 $file $RPM_BUILD_ROOT%{_unitdir}
done
for file in systemd/*.mount  ; do
	install -m 644 $file $RPM_BUILD_ROOT%{_unitdir}
done

mkdir -p $RPM_BUILD_ROOT/run/sysconfig
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/scripts
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/systemd/scripts/nfs-utils_env.sh
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/lockd.conf

#
# For backwards compatablity 
#
cd $RPM_BUILD_ROOT%{_unitdir}
ln -s nfs-server.service nfs.service
ln -s rpc-gssd.service nfs-secure.service
ln -s nfs-idmapd.service  nfs-idmap.service
ln -s rpc-statd.service nfs-lock.service

mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/rpc_pipefs

touch $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/rmtab
mv $RPM_BUILD_ROOT%{_sbindir}/rpc.statd $RPM_BUILD_ROOT/sbin

mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/statd/sm
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/statd/sm.bak
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/v4recovery
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/exports.d

%clean
rm -rf $RPM_BUILD_ROOT/*

%pre
# move files so the running service will have this applied as well
for x in gssd idmapd ; do
    if [ -f /var/lock/subsys/rpc.$x ]; then
		mv /var/lock/subsys/rpc.$x /var/lock/subsys/rpc$x
    fi
done

%define rpcuser_uid 29
# Create rpcuser gid as long as it does not already exist
cat /etc/group | cut -d':' -f 1 | grep --quiet rpcuser 2>/dev/null
if [ "$?" -eq 1 ]; then
    /usr/sbin/groupadd -g %{rpcuser_uid} rpcuser >/dev/null 2>&1 || :
else
    /usr/sbin/groupmod -g %{rpcuser_uid} rpcuser >/dev/null 2>&1 || :
fi

# Create rpcuser uid as long as it does not already exist.
cat /etc/passwd | cut -d':' -f 1 | grep --quiet rpcuser 2>/dev/null
if [ "$?" -eq 1 ]; then
    /usr/sbin/useradd -l -c "RPC Service User" -r -g %{rpcuser_uid} \
        -s /sbin/nologin -u %{rpcuser_uid} -d /var/lib/nfs rpcuser >/dev/null 2>&1 || :
else
 /usr/sbin/usermod -u %{rpcuser_uid} -g %{rpcuser_uid} rpcuser >/dev/null 2>&1 || :
fi 

# Using the 16-bit value of -2 for the nfsnobody uid and gid
%define nfsnobody_uid	65534

# Create nfsnobody gid as long as it does not already exist
cat /etc/group | cut -d':' -f 1 | grep --quiet nfsnobody 2>/dev/null
if [ "$?" -eq 1 ]; then
    /usr/sbin/groupadd -g %{nfsnobody_uid} nfsnobody >/dev/null 2>&1 || :
else
    /usr/sbin/groupmod -g %{nfsnobody_uid} nfsnobody >/dev/null 2>&1 || :
fi

# Create nfsnobody uid as long as it does not already exist.
cat /etc/passwd | cut -d':' -f 1 | grep --quiet nfsnobody 2>/dev/null
if [ $? -eq 1 ]; then
    /usr/sbin/useradd -l -c "Anonymous NFS User" -r -g %{nfsnobody_uid} \
		-s /sbin/nologin -u %{nfsnobody_uid} -d /var/lib/nfs nfsnobody >/dev/null 2>&1 || :
else

   /usr/sbin/usermod -u %{nfsnobody_uid} -g %{nfsnobody_uid} nfsnobody >/dev/null 2>&1 || :
fi

%post
if [ $1 -eq 1 ] ; then
	# Initial installation
	/bin/systemctl enable nfs-client.target >/dev/null 2>&1 || :
	/bin/systemctl start nfs-client.target  >/dev/null 2>&1 || :
fi
%systemd_post nfs-config
%systemd_post nfs-server

# Make sure statd used the correct uid/gid.
chown -R rpcuser:rpcuser /var/lib/nfs/statd

%preun
if [ $1 -eq 0 ]; then
	%systemd_preun nfs-client.target
	%systemd_preun nfs-server.server

    /usr/sbin/userdel rpcuser 2>/dev/null || :
    /usr/sbin/groupdel rpcuser 2>/dev/null || :
    /usr/sbin/userdel nfsnobody 2>/dev/null || :
    /usr/sbin/groupdel nfsnobody 2>/dev/null || :
    rm -rf /var/lib/nfs/statd
    rm -rf /var/lib/nfs/v4recovery
fi

%postun
%systemd_postun_with_restart  nfs-client.target
%systemd_postun_with_restart  nfs-server

/bin/systemctl --system daemon-reload >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/sysconfig/nfs
%config(noreplace) /etc/nfsmount.conf
%dir %{_sysconfdir}/exports.d
%dir %{_sharedstatedir}/nfs/v4recovery
%dir %{_sharedstatedir}/nfs/rpc_pipefs
%dir %{_sharedstatedir}/nfs
%dir %attr(700,rpcuser,rpcuser) %{_sharedstatedir}/nfs/statd
%dir %attr(700,rpcuser,rpcuser) %{_sharedstatedir}/nfs/statd/sm
%dir %attr(700,rpcuser,rpcuser) %{_sharedstatedir}/nfs/statd/sm.bak
%config(noreplace) %attr(644,rpcuser,rpcuser) %{_statdpath}/state
%config(noreplace) %{_sharedstatedir}/nfs/xtab
%config(noreplace) %{_sharedstatedir}/nfs/etab
%config(noreplace) %{_sharedstatedir}/nfs/rmtab
%config(noreplace) %{_sysconfdir}/request-key.d/id_resolver.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/lockd.conf
%doc linux-nfs/ChangeLog linux-nfs/KNOWNBUGS linux-nfs/NEW linux-nfs/README
%doc linux-nfs/THANKS linux-nfs/TODO
/sbin/rpc.statd
/sbin/osd_login
/sbin/nfsdcltrack
%{_sbindir}/exportfs
%{_sbindir}/nfsstat
%{_sbindir}/rpcdebug
%{_sbindir}/rpc.mountd
%{_sbindir}/rpc.nfsd
%{_sbindir}/showmount
%{_sbindir}/rpc.idmapd
%{_sbindir}/rpc.gssd
%{_sbindir}/sm-notify
%{_sbindir}/start-statd
%{_sbindir}/mountstats
%{_sbindir}/nfsiostat
%{_sbindir}/nfsidmap
%{_sbindir}/blkmapd
%{_mandir}/*/*
%{_unitdir}/*
%attr(755,root,root) /usr/lib/systemd/scripts/nfs-utils_env.sh

%attr(4755,root,root)	/sbin/mount.nfs
/sbin/mount.nfs4
/sbin/umount.nfs
/sbin/umount.nfs4

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:1.3.2-11
- Rebuild for new 4.0 release.

