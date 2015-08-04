Summary: Traces the route taken by packets over a TCP/IP network.
Name: traceroute
Version: 1.0.4
Release: 1.2
Epoch: 2
License: GPL
Group: Applications/Internet
Source: ftp://ftp.lst.de/pub/people/okir/traceroute/%{name}-%{version}.tar.bz2
Patch0: traceroute-1.0.4-compat.patch
BuildRoot: %{_tmppath}/%{name}-root

%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.  Traceroute displays
the IP number and host name (if possible) of the machines along the
route taken by the packets.  Traceroute is used as a network debugging
tool.  If you're having network connectivity problems, traceroute will
show you where the trouble is coming from along the route.

This is a small traceroute replacement that works without requiring a
setuid bit. This implementation relies on a number of features of the
2.4 Linux kernel. It also has IPv6 support, and does parallel probes,
which makes it a little faster.

Install traceroute if you need a tool for diagnosing network connectivity
problems.

%prep
%setup -q
%patch0 -p1 -b .compat

%build
%ifarch s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
export LDFLAGS="-pie"

make CCOPT="$CFLAGS"

%install
rm -rf %{buildroot}
install -m 755 -D %{name} %{buildroot}/bin/%{name}
install -m 644 -D %{name}.1 %{buildroot}%{_mandir}/man8/%{name}.8
#for IPv6 traceroute
#ln -sf %{name} %{buildroot}/bin/traceroute6
#ln -sf %{_mandir}/man8/%{name}.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/%{name}6.8 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/traceroute*
%{_mandir}/man8/*

%changelog
