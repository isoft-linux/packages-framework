%define snapshot .svn550

Name:		vpnc
Version:	0.5.3
Release:	27%{snapshot}

Summary:	IPSec VPN client compatible with Cisco equipment

License:	GPLv2+
URL:		http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:	http://www.unix-ag.uni-kl.de/~massar/vpnc/%{name}-%{version}%{snapshot}.tar.gz
Source1:	generic-vpnc.conf

Source8:	%{name}-tmpfiles.conf

Patch1:		vpnc-0.5.1-dpd.patch
Patch2:		vpnc-0.5.3-use-autodie.patch

BuildRequires:	libgcrypt-devel > 1.1.90
BuildRequires:	gnutls-devel
BuildRequires:	perl(autodie)
Requires:	iproute vpnc-script

%description
A VPN client compatible with Cisco's EasyVPN equipment.

Supports IPSec (ESP) with Mode Configuration and Xauth.  Supports only
shared-secret IPSec authentication, 3DES, MD5, and IP tunneling.

%prep
%setup -q
%patch1 -p1 -b .dpd
%patch2 -p1 -b .autodie

%build
CFLAGS="$RPM_OPT_FLAGS -fPIE" LDFLAGS="$RPM_OPT_FLAGS -pie" make PREFIX=/usr 

%install
make install DESTDIR="$RPM_BUILD_ROOT" PREFIX=/usr
rm -f $RPM_BUILD_ROOT%{_bindir}/pcf2vpnc
chmod 0644 pcf2vpnc
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/pcf2vpnc.1
chmod 0644 $RPM_BUILD_ROOT%{_mandir}/man8/vpnc.8
install -m 0600 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/vpnc/default.conf


rm -f $RPM_BUILD_ROOT%{_datadir}/doc/vpnc/COPYING
# vpnc-script is packaged in a separate package
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/vpnc/vpnc-script

mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m 0755 %{buildroot}%{_localstatedir}/run/%{name}/

%files
%defattr(-,root,root)
%doc README COPYING pcf2vpnc pcf2vpnc.1

%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/vpnc/default.conf
%{_sbindir}/vpnc
%{_bindir}/cisco-decrypt
%{_sbindir}/vpnc-disconnect
%{_mandir}/man8/vpnc.*
%{_mandir}/man1/cisco-decrypt.*
%dir %{_localstatedir}/run/%{name}/



%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.5.3-27.svn550
- Rebuild for new 4.0 release.

