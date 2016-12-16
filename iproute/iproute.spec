%global             cbq_version v0.7.3
Summary:            Advanced IP routing and network device configuration tools
Name:               iproute
Version:            4.2.0
Release:            4%{?dist}
URL:                http://kernel.org/pub/linux/utils/net/%{name}2/
Source0:            http://kernel.org/pub/linux/utils/net/%{name}2/%{name}2-%{version}.tar.xz
Source1:            cbq-0000.example
Source2:            avpkt

# manpage/help improvements
Patch1:             iproute2-3.19.0-docs.patch

License:            GPLv2+ and Public Domain
BuildRequires:      bison
BuildRequires:      flex
BuildRequires:      iptables-devel >= 1.4.5
BuildRequires:      libdb-devel
BuildRequires:      linuxdoc-tools
BuildRequires:      pkgconfig
BuildRequires:      psutils
# For the UsrMove transition period
Conflicts:          filesystem < 3
Provides:           /sbin/ip

%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
2.4.x and 2.6.x kernel.

%package doc
Summary:            Documentation for iproute2 utilities with examples
License:            GPLv2+

%description doc
The iproute documentation contains howtos and examples of settings.

%package devel
Summary:            iproute development files
License:            GPLv2+
Provides:           iproute-static = %{version}-%{release}

%description devel
The libnetlink static library.

%prep
%setup -q -n %{name}2-%{version}
%patch1 -p1

sed -i '/^TARGETS=/s: arpd : :' misc/Makefile

%build
export CFLAGS="%{optflags}"
export LIBDIR=/%{_libdir}
export IPT_LIB_DIR=/%{_lib}/xtables
./configure
make %{?_smp_mflags}

%install
# TODO: Update upstream build system so that we don't need to handle
# installation manually.
mkdir -p \
    %{buildroot}%{_includedir} \
    %{buildroot}%{_sbindir} \
    %{buildroot}%{_mandir}/man3 \
    %{buildroot}%{_mandir}/man7 \
    %{buildroot}%{_mandir}/man8 \
    %{buildroot}%{_libdir}/tc \
    %{buildroot}%{_sysconfdir}/iproute2 \
    %{buildroot}%{_sysconfdir}/sysconfig/cbq

for binary in \
    bridge/bridge \
    examples/cbq.init-%{cbq_version} \
    genl/genl \
    ip/ifcfg \
    ip/ip \
    ip/routef \
    ip/routel \
    ip/rtmon \
    ip/rtpr \
    misc/ifstat \
    misc/lnstat \
    misc/nstat \
    misc/rtacct \
    misc/ss \
    tc/tc
    do install -m755 ${binary} %{buildroot}%{_sbindir}
done
mv %{buildroot}%{_sbindir}/cbq.init-%{cbq_version} %{buildroot}%{_sbindir}/cbq
cd %{buildroot}%{_sbindir}
    ln -s lnstat ctstat
    ln -s lnstat rtstat
cd -

# Libs
install -m644 netem/*.dist %{buildroot}%{_libdir}/tc
#install -m755 tc/q_atm.so %{buildroot}%{_libdir}/tc
install -m755 tc/m_xt.so %{buildroot}%{_libdir}/tc
cd %{buildroot}%{_libdir}/tc
    ln -s m_xt.so m_ipt.so
cd -

# libnetlink
install -m644 include/libnetlink.h %{buildroot}%{_includedir}
install -m644 lib/libnetlink.a %{buildroot}%{_libdir}

# Manpages
iconv -f latin1 -t utf8 man/man8/ss.8 > man/man8/ss.8.utf8 &&
    mv man/man8/ss.8.utf8 man/man8/ss.8
install -m644 man/man3/*.3 %{buildroot}%{_mandir}/man3
install -m644 man/man7/*.7 %{buildroot}%{_mandir}/man7
install -m644 man/man8/*.8 %{buildroot}%{_mandir}/man8

# Config files
install -m644 etc/iproute2/* %{buildroot}%{_sysconfdir}/iproute2
for config in \
    %{SOURCE1} \
    %{SOURCE2}
    do install -m644 ${config} %{buildroot}%{_sysconfdir}/sysconfig/cbq
done

%files
%dir %{_sysconfdir}/iproute2
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README README.decnet README.iproute2+tc README.distribution README.lnstat
%{_mandir}/man7/*
%{_mandir}/man8/*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%dir %{_libdir}/tc/
%{_libdir}/tc/*
%dir %{_sysconfdir}/sysconfig/cbq
%config(noreplace) %{_sysconfdir}/sysconfig/cbq/*

%files doc
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc examples

%files devel
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man3/*
%{_libdir}/libnetlink.a
%{_includedir}/libnetlink.h

%changelog
* Fri Dec 16 2016 sulit - 4.2.0-4
- rebuild iproute

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.2.0-3
- Rebuild for new 4.0 release.

