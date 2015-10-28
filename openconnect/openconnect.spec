#% define gitcount 211
#% define gitrev 584c84f

%if 0%{?gitcount} > 0
%define gitsuffix -%{gitcount}-g%{gitrev}
%define relsuffix .git%{gitcount}_%{gitrev}
%endif

%define use_gnutls 1
%define use_libproxy 1
%define use_tokens 1

Name:		openconnect
Version:	7.06
Release:	3%{?relsuffix}%{?dist}
Summary:	Open client for Cisco AnyConnect VPN

License:	LGPLv2+
URL:		http://www.infradead.org/openconnect.html
Source0:	ftp://ftp.infradead.org/pub/openconnect/openconnect-%{version}%{?gitsuffix}.tar.gz
Patch1:		openconnect-7.05-override-default-prio-string.patch
Patch2:		openconnect-7.05-ensure-dtls-ciphers-match-the-allowed.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	pkgconfig(openssl) pkgconfig(libxml-2.0)
BuildRequires:	autoconf automake libtool python gettext pkgconfig(liblz4)
Requires:	vpnc-script

%if %{use_gnutls}
BuildRequires:	pkgconfig(gnutls) trousers-devel pkgconfig(libpcsclite)
%endif
%if %{use_libproxy}
BuildRequires:	pkgconfig(libproxy-1.0)
%endif
%if %{use_tokens}
BuildRequires:  pkgconfig(liboath) pkgconfig(stoken)
%endif

%description
This package provides a client for the Cisco AnyConnect VPN protocol, which
is based on HTTPS and DTLS.

%package devel
Summary: Development package for OpenConnect VPN authentication tools
Requires: %{name}%{?_isa} = %{version}-%{release}
# RHEL5 needs these spelled out because it doesn't automatically infer from pkgconfig
%if 0%{?rhel} && 0%{?rhel} <= 5
Requires: openssl-devel zlib-devel
%endif

%description devel
This package provides the core HTTP and authentication support from
the OpenConnect VPN client, to be used by GUI authentication dialogs
for NetworkManager etc.

%prep
%setup -q -n openconnect-%{version}%{?gitsuffix}

%patch1 -p1 -b .prio
%patch2 -p1 -b .ciphers

%build
autoreconf -fvi
%configure	--with-vpnc-script=/etc/vpnc/vpnc-script \
		--with-default-gnutls-priority="@SYSTEM" \
%if !%{use_gnutls}
		--with-openssl --without-openssl-version-check \
%endif
		--htmldir=%{_docdir}/%{name}
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
%make_install
rm -f $RPM_BUILD_ROOT/%{_libdir}/libopenconnect.la
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_libdir}/libopenconnect.so.5*
%{_sbindir}/openconnect
%{_mandir}/man8/*
%doc TODO COPYING.LGPL

%files devel
%defattr(-,root,root,-)
%{_libdir}/libopenconnect.so
%{_includedir}/openconnect.h
%{_libdir}/pkgconfig/openconnect.pc
%{_datadir}/doc/openconnect
%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 7.06-3
- Rebuild for new 4.0 release.

