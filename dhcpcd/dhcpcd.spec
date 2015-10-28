Summary:	DHCP Client Daemon
Name:		dhcpcd
Version:    6.9.0
Release:    2	
License:	BSD-Like
URL:		http://roy.marples.name/projects/dhcpcd/
Source0:	http://roy.marples.name/downloads/dhcpcd/%{name}-%{version}.tar.bz2
%description
dhcpcd is an RFC2131 compliant DHCP client. It is fully featured and yet
lightweight: the binary is 60k as reported by size(1) on Linux i386. It has
support for duplicate address detection, IPv4LL, carrier detection, and a
merged resolv.conf and ntp.conf for which other DHCP clients require third
party tools.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf %{buildroot}

%files
%doc README
%config(noreplace) %{_sysconfdir}/dhcpcd.conf
%{_sbindir}/dhcpcd
%dir %{_libexecdir}/dhcpcd-hooks
%{_libexecdir}/dhcpcd-hooks/*
%{_libexecdir}/dhcpcd-run-hooks
%{_libdir}/dhcpcd/dev/udev.so
%{_mandir}/man5/dhcpcd.conf.5*
%{_mandir}/man8/dhcpcd.8*
%{_mandir}/man8/dhcpcd-run-hooks.8*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 6.9.0-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

