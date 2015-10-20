Name:           rpcbind
Version:        0.2.3
Release:        0.2%{?dist}
Summary:        Universal Addresses to RPC Program Number Mapper
Group:          System Environment/Daemons
License:        BSD
URL:            http://nfsv4.bullopensource.org

BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Source0:        http://downloads.sourceforge.net/rpcbind/%{name}-%{version}.tar.bz2
Source1: rpcbind.service
Source2: rpcbind.socket
Source3: rpcbind.sysconfig

Requires: glibc-common setup
Conflicts: man-pages < 2.43-12
BuildRequires: automake, autoconf, libtool, systemd, systemd-devel
BuildRequires: libtirpc-devel, quota-devel, tcp_wrappers-devel
Requires(pre): coreutils shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd coreutils

Provides: portmap = %{version}-%{release}
Obsoletes: portmap <= 4.0-65.3

%description
The rpcbind utility is a server that converts RPC program numbers into
universal addresses.  It must be running on the host to be able to make
RPC calls on a server on that machine.

%prep
%setup -q

%build
%ifarch s390 s390x
PIE="-fPIE"
%else
PIE="-fpie"
%endif
export PIE

RPCBUSR=rpc
RPCBDIR=/tmp
CFLAGS="`echo $RPM_OPT_FLAGS $ARCH_OPT_FLAGS $PIE`"

autoreconf -fisv
%configure CFLAGS="$CFLAGS" LDFLAGS="-pie" \
    --enable-warmstarts \
    --with-statedir="$RPCBDIR" \
    --with-rpcuser="$RPCBUSR" \
    --enable-libwrap \
    --enable-debug

make all

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}{/sbin,/usr/sbin,/etc/sysconfig}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_mandir}/man8
make DESTDIR=$RPM_BUILD_ROOT install

mv -f ${RPM_BUILD_ROOT}%{_bindir}/rpcbind ${RPM_BUILD_ROOT}/sbin
mv -f ${RPM_BUILD_ROOT}%{_bindir}/rpcinfo ${RPM_BUILD_ROOT}%{_sbindir}
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m644 %{SOURCE3} %{buildroot}/etc/sysconfig/rpcbind

%clean
rm -rf %{buildroot}

%pre

# Check the validity of the rpc uid and gid.
# If they don't exist, create them
# If they exist but are the wrong value, remove them 
#   and recreate them with the correct value
# If they exist and are the correct value do nothing
rpcid=`getent passwd rpc | cut -d: -f 3`
if [ -n "$rpcid" -a "$rpcid" != "32" ]; then
	/usr/sbin/userdel  rpc 2> /dev/null || :
	/usr/sbin/groupdel rpc 2> /dev/null || : 
fi
if [ -z "$rpcid" -o "$rpcid" != "32" ]; then
	/usr/sbin/groupadd -o -g 32 rpc > /dev/null 2>&1
	/usr/sbin/useradd -o -l -c "Rpcbind Daemon" -d /var/lib/rpcbind -g 32 \
    	-M -s /sbin/nologin -u 32 rpc > /dev/null 2>&1
fi

%post
/bin/systemctl enable rpcbind.socket >/dev/null 2>&1 || :

%preun
%systemd_preun rpcbind.service rpcbind.socket
if [ $1 -eq 0 ]; then
	/usr/sbin/userdel  rpc 2>/dev/null || :
	/usr/sbin/groupdel rpc 2>/dev/null || :
fi

%postun
%systemd_postun_with_restart rpcbind.service rpcbind.socket

%triggerun -- rpcbind < 0.2.0-15
%{_bindir}/systemd-sysv-convert --save rpcbind >/dev/null 2>&1 ||:
/bin/systemctl --no-reload enable rpcbind.service >/dev/null 2>&1
/bin/systemctl try-restart rpcbind.service >/dev/null 2>&1 || :

%triggerun -- rpcbind > 0.2.2-2.0
/bin/systemctl enable rpcbind.socket

%files
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/rpcbind
%doc AUTHORS ChangeLog README
/sbin/rpcbind
%{_sbindir}/rpcinfo
%{_mandir}/man8/*
%{_unitdir}/rpcbind.service
%{_unitdir}/rpcbind.socket

%changelog
