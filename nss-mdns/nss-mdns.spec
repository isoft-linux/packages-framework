Summary: glibc plugin for .local name resolution
Name: nss-mdns
Version: 0.10
Release: 17
License: LGPLv2+
URL: http://0pointer.de/lennart/projects/nss-mdns/
Source: http://0pointer.de/lennart/projects/nss-mdns/nss-mdns-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: avahi
 
%description
nss-mdns is a plugin for the GNU Name Service Switch (NSS) functionality of
the GNU C Library (glibc) providing host name resolution via Multicast DNS
(aka Zeroconf, aka Apple Rendezvous, aka Apple Bonjour), effectively allowing 
name resolution by common Unix/Linux programs in the ad-hoc mDNS domain .local.

nss-mdns provides client functionality only, which means that you have to
run a mDNS responder daemon separately from nss-mdns if you want to register
the local host name via mDNS (e.g. Avahi).

%prep
%setup -q

%build
%configure --libdir=/%{_lib} --enable-avahi=yes --enable-legacy=no
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
# Perl-fu to add mdns4_minimal to the hosts line of /etc/nsswitch.conf
if [ -f /etc/nsswitch.conf ] ; then
	sed -i.bak '
		/^hosts:/ !b
		/\<mdns\(4\|6\)\?\(_minimal\)\?\>/ b
		s/\([[:blank:]]\+\)dns\>/\1mdns4_minimal [NOTFOUND=return] dns/g
		' /etc/nsswitch.conf
fi

%preun
# sed-fu to remove mdns4_minimal from the hosts line of /etc/nsswitch.conf
if [ "$1" -eq 0 -a -f /etc/nsswitch.conf ] ; then
	sed -i.bak '
		/^hosts:/ !b
		s/[[:blank:]]\+mdns\(4\|6\)\?\(_minimal\( \[NOTFOUND=return\]\)\?\)\?//g
	' /etc/nsswitch.conf
fi

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README
/%{_lib}/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.10-17
- Rebuild for new 4.0 release.

