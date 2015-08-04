Summary:            Advanced IP routing and network device configuration tools
Name:               iproute
Version:            3.16.0 
Release:            1 
Group:              Applications/System
URL:                http://www.linuxfoundation.org/collaborate/workgroups/networking/%{name}2
Source0:            http://devresources.linuxfoundation.org/dev/iproute2/download/%{name}2-%{version}.tar.xz

License:            GPLv2+ and Public Domain
BuildRequires:      flex libdb-devel bison
BuildRequires:      iptables-devel >= 1.4.5
Requires:           iptables >= 1.4.5

%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
2.4.x and 2.6.x kernel.

%package devel
Summary:            iproute development files
Group:              Development/Libraries
License:            GPLv2+
Provides:           iproute-static = %{version}-%{release}

%description devel
The libnetlink static library.

%prep
%setup -q -n iproute2-%{version}

sed -i '/^TARGETS=/s: arpd : :' misc/Makefile
sed -i 's:/usr/local:/usr:' tc/m_ipt.c include/iptables.h || return 1
sed -i -e 's:=/share:=/usr/share:' \
        -e 's:-Werror::' Makefile || return 1

%build
./configure
make CCOPTS="-D_GNU_SOURCE $RPM_OPT_FLAGS"

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_docdir}/iproute2
rpmclean
%files
%defattr(-,root,root,-)
%{_sysconfdir}/iproute2
/sbin/bridge
/sbin/ctstat
/sbin/genl
/sbin/ifcfg
/sbin/ifstat
/sbin/ip
/sbin/lnstat
/sbin/nstat
/sbin/routef
/sbin/routel
/sbin/rtacct
/sbin/rtmon
/sbin/rtpr
/sbin/rtstat
/sbin/ss
/sbin/tc
%{_libdir}/tc
%{_mandir}/man3/*
%{_mandir}/man7/*
%{_mandir}/man8/*
/var/lib/arpd
