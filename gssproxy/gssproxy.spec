Name:		gssproxy
Version:	0.4.1
Release:	3%{?dist}
Summary:	GSSAPI Proxy

License:	MIT
URL:		http://fedorahosted.org/gss-proxy
Source0:	http://fedorahosted.org/released/gss-proxy/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%global servicename gssproxy
%global pubconfpath %{_sysconfdir}/gssproxy
%global gpstatedir %{_localstatedir}/lib/gssproxy

### Patches ###

### Dependencies ###

Requires: krb5-libs >= 1.12.0
Requires: keyutils-libs
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

### Build Dependencies ###

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: m4
BuildRequires: libxslt
BuildRequires: libxml2
BuildRequires: docbook-style-xsl
BuildRequires: doxygen
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildRequires: krb5-devel >= 1.12.0
BuildRequires: keyutils-libs-devel
BuildRequires: libini_config-devel >= 1.0.0.1
BuildRequires: libverto-devel
BuildRequires: popt-devel
BuildRequires: findutils
BuildRequires: systemd-units


%description
A proxy for GSSAPI credential handling

%prep
%setup -q


%build
autoreconf -f -i
%configure \
    --with-pubconf-path=%{pubconfpath} \
    --with-initscript=systemd \
    --disable-static \
    --disable-rpath \
    --without-selinux \
    --with-gpp-default-behavior=REMOTE_FIRST

make %{?_smp_mflags} all
make test_proxymech

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/gssproxy/proxymech.la
install -d -m755 %{buildroot}%{_sysconfdir}/gssproxy
install -m644 examples/gssproxy.conf %{buildroot}%{_sysconfdir}/gssproxy/gssproxy.conf
mkdir -p %{buildroot}%{_sysconfdir}/gss/mech.d
install -m644 examples/mech %{buildroot}%{_sysconfdir}/gss/mech.d/gssproxy.conf

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING
%{_unitdir}/gssproxy.service
%{_sbindir}/gssproxy
%attr(755,root,root) %dir %{pubconfpath}
%attr(755,root,root) %dir %{gpstatedir}
%attr(700,root,root) %dir %{gpstatedir}/clients
%attr(0600,root,root) %config(noreplace) /%{_sysconfdir}/gssproxy/gssproxy.conf
%attr(0644,root,root) %config(noreplace) /%{_sysconfdir}/gss/mech.d/gssproxy.conf
%{_libdir}/gssproxy/proxymech.so
%{_mandir}/man5/gssproxy.conf.5*
%{_mandir}/man8/gssproxy.8*
%{_mandir}/man8/gssproxy-mech.8*

%post
%systemd_post gssproxy.service

%preun
%systemd_preun gssproxy.service

%postun
%systemd_postun_with_restart gssproxy.service

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.4.1-3
- Rebuild for new 4.0 release.

