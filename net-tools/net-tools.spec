%global checkout 20140924git

Summary: Basic networking tools
Name: net-tools
Version: 1.6 
Release: 1.%{checkout}
License: GPL+
Group: System Environment/Base
URL: http://net-tools.sourceforge.net
Source0: net-tools-code.tar.xz
Patch0: net-tools-git.patch
Patch1: net-tools-musl-fix.patch
%description
The net-tools package contains basic networking tools,
including ifconfig, netstat, route, and others.
Most of them are obsolete. For replacement check iproute package.

%prep
%setup -q -n net-tools-code
#%patch0 -p1
%patch1 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS $CFLAGS -fpie"
export LDFLAGS="$LDFLAGS -pie -Wl,-z,relro -Wl,-z,now"

cat > config.make <<EOF
# I18N=0
HAVE_AFUNIX=1
HAVE_AFINET=1
HAVE_AFINET6=1
# HAVE_AFIPX=0
# HAVE_AFATALK=0
# HAVE_AFAX25=0
HAVE_AFNETROM=1
# HAVE_AFROSE=0
# HAVE_AFX25=0
# HAVE_AFECONET=0
# HAVE_AFDECnet=0
# HAVE_AFASH=0
# HAVE_AFBLUETOOTH=0
HAVE_HWETHER=1
# HAVE_HWARC=0
HAVE_HWSLIP=1
HAVE_HWPPP=1
HAVE_HWTUNNEL=1
# HAVE_HWSTRIP=0
# HAVE_HWTR=0
# HAVE_HWAX25=0
# HAVE_HWROSE=0
HAVE_HWNETROM=1
# HAVE_HWX25=0
# HAVE_HWFR=0
# HAVE_HWSIT=0
# HAVE_HWFDDI=0
# HAVE_HWHIPPI=0
# HAVE_HWASH=0
# HAVE_HWHDLCLAPB=0
# HAVE_HWIRDA=0
# HAVE_HWEC=0
# HAVE_HWEUI64=0
# HAVE_HWIB=0
HAVE_FW_MASQUERADE=1
HAVE_IP_TOOLS=1
HAVE_MII=1
EOF

sed -n -e 's/^\(HAVE.*\)=\(.*\)/#define \1 \2/p' config.make > config.h

make

%install

make BASEDIR=%{buildroot} mandir=%{_mandir} install

# ifconfig and route are installed into /bin by default
# mv them back to /sbin for now as I (jpopelka) don't think customers would be happy
mv %{buildroot}/bin/ifconfig %{buildroot}/sbin
mv %{buildroot}/bin/route %{buildroot}/sbin

rm %{buildroot}/sbin/rarp
rm %{buildroot}%{_mandir}/man8/rarp.8*

# remove hostname (has its own package)
rm %{buildroot}/bin/dnsdomainname
rm %{buildroot}/bin/domainname
rm %{buildroot}/bin/hostname
rm %{buildroot}/bin/nisdomainname
rm %{buildroot}/bin/ypdomainname
rm -rf %{buildroot}%{_mandir}/de/man1
rm -rf %{buildroot}%{_mandir}/fr/man1
rm -rf %{buildroot}%{_mandir}/man1
rm -rf %{buildroot}%{_mandir}/pt/man1



%files
%doc COPYING
/bin/netstat
/sbin/ifconfig
/sbin/route
/sbin/arp
/sbin/ipmaddr
/sbin/iptunnel
/sbin/mii-tool
/sbin/nameif
/sbin/plipconfig
/sbin/slattach
%{_mandir}/man[58]/*

%changelog
