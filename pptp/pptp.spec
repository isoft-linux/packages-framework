Name:		pptp
Version:	1.8.0
Release:	8
Summary:	Point-to-Point Tunneling Protocol (PPTP) Client
License:	GPLv2+
URL:		http://pptpclient.sourceforge.net/
Source0:	http://downloads.sf.net/pptpclient/pptp-%{version}.tar.gz
Source1:	pptp-tmpfs.conf
Patch0:		pptp-1.7.2-pptpsetup-mppe.patch
# patch from upstream
Patch1:		pptp-1.8.0-vector-remove-fix.patch
Patch2:		pptp-1.8.0-call-use-after-free-fix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	/usr/bin/pod2man
Requires:	ppp >= 2.4.2, /sbin/ip
Requires:	systemd-units

%description
Client for the proprietary Microsoft Point-to-Point Tunneling
Protocol, PPTP. Allows connection to a PPTP based VPN as used
by employers and some cable and ADSL service providers.

%package setup
Summary:	PPTP Tunnel Configuration Script
Requires:	%{name} = %{version}-%{release}

%description setup
This package provides a simple configuration script for setting up PPTP
tunnels.

%prep
%setup -q

# Don't check for MPPE capability in kernel and pppd at all because current
# Fedora releases and EL ≥ 5 include MPPE support out of the box (#502967)
%patch0 -p1 -b .mppe

%patch1 -p1 -b .vector-remove-fix
%patch2 -p1 -b .call-use-after-free-fix

# Pacify rpmlint
perl -pi -e 's/install -o root -m 555 pptp/install -m 755 pptp/;' Makefile

%build
OUR_CFLAGS="-Wall %{optflags} -Wextra -Wstrict-aliasing=2 -Wnested-externs -Wstrict-prototypes"
make %{?_smp_mflags} CFLAGS="$OUR_CFLAGS" IP=/sbin/ip

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -d -m 750 %{buildroot}%{_localstatedir}/run/pptp

# Make sure /var/run/pptp exists at boot time for systems
# with /var/run on tmpfs (#656672)
install -d -m 755 %{buildroot}%{_prefix}/lib/tmpfiles.d
install -p -m 644 %{SOURCE1} %{buildroot}%{_prefix}/lib/tmpfiles.d/pptp.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING DEVELOPERS NEWS README TODO USING
%doc ChangeLog Documentation/DESIGN.PPTP PROTOCOL-SECURITY
%{_prefix}/lib/tmpfiles.d/pptp.conf
%{_sbindir}/pptp
%{_mandir}/man8/pptp.8*
%dir %attr(750,root,root) %{_localstatedir}/run/pptp/
%config(noreplace) %{_sysconfdir}/ppp/options.pptp

%files setup
%defattr(-,root,root,-)
%{_sbindir}/pptpsetup
%{_mandir}/man8/pptpsetup.8*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.8.0-8
- Rebuild for new 4.0 release.

