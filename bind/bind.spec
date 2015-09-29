#We only ship bind utils in this package. since we are desktop.

%global PATCHVER P3
%global VERSION %{version}%{?PREVER}%{?PATCHVER:-%{PATCHVER}}

Summary:  The Berkeley Internet Name Domain (BIND) DNS (Domain Name System) server
Name:     bind
License:  ISC
Version:  9.10.2
Release:  9%{?PATCHVER:.%{PATCHVER}}%{?PREVER:.%{PREVER}}%{?dist}
Epoch:    32
Url:      http://www.isc.org/products/BIND/
Source0:   ftp://ftp.isc.org/isc/bind9/%{VERSION}/bind-%{VERSION}.tar.gz

Source36: trusted-key.key

# Common patches
Patch10: bind-9.5-PIE.patch
Patch16: bind-9.3.2-redhat_doc.patch
Patch72: bind-9.5-dlz-64bit.patch
Patch101:bind-96-old-api.patch
Patch102:bind-95-rh452060.patch
Patch106:bind93-rh490837.patch
Patch109:bind97-rh478718.patch
Patch110:bind97-rh570851.patch
Patch112:bind97-rh645544.patch
Patch119:bind97-rh693982.patch
Patch123:bind98-rh735103.patch
Patch125:bind99-buildfix.patch
Patch130:bind-9.9.1-P2-dlz-libdb.patch
Patch131:bind-9.9.1-P2-multlib-conflict.patch
Patch133:bind99-rh640538.patch
Patch134:bind97-rh669163.patch
# Fedora specific patch to distribute native-pkcs#11 functionality
Patch136:bind-9.10-dist-native-pkcs11.patch
# [ISC-Bugs #38710] Python3 issue: print used as a statement in dnssec-coverage.py
Patch137:bind-9.10-ISC-Bugs-38710.patch

# SDB patches
Patch11: bind-9.3.2b2-sdbsrc.patch
Patch12: bind-9.10-sdb.patch

# needs inpection
Patch17: bind-9.3.2b1-fix_sdb_ldap.patch
Patch104: bind-9.10-dyndb.patch

# [ISC-Bugs #36101] IDN support in host/dig/nslookup using GNU libidn(2)
Patch73: bind-99-libidn.patch


Requires:       coreutils
BuildRequires:  openssl-devel, libtool, autoconf, pkgconfig, libcap-devel
BuildRequires:  libidn-devel, libxml2-devel
BuildRequires:  systemd

# needed for %%{__python3} macro
BuildRequires:  python3-devel

# Needed to regenerate dig.1 manpage
BuildRequires: docbook-style-xsl, libxslt

%description
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(Domain Name System) protocols. BIND includes a DNS server (named),
which resolves host names to IP addresses; a resolver library
(routines for applications to use when interfacing with DNS); and
tools for verifying that the DNS server is operating properly.

%package utils
Summary: Utilities for querying DNS name servers

%description utils
Bind-utils contains a collection of utilities for querying DNS (Domain
Name System) name servers to find out information about Internet
hosts. These tools will provide you with the IP addresses for given
host names, as well as other information about registered domains and
network addresses.

You should install bind-utils if you need to get information from DNS name
servers.

%prep
%setup -q -n %{name}-%{VERSION}

# Common patches
%patch10 -p1 -b .PIE
%patch16 -p1 -b .redhat_doc
%patch104 -p1 -b .dyndb
%ifnarch alpha ia64
%patch72 -p1 -b .64bit
%endif
%patch73 -p1 -b .libidn
%patch102 -p1 -b .rh452060
%patch106 -p0 -b .rh490837
%patch109 -p1 -b .rh478718
%patch110 -p1 -b .rh570851
%patch112 -p1 -b .rh645544
%patch119 -p1 -b .rh693982
%patch125 -p1 -b .buildfix
%patch130 -p1 -b .libdb
%patch131 -p1 -b .multlib-conflict
%patch137 -p1 -b .ISC-Bugs-38710

%patch133 -p1 -b .rh640538
%patch134 -p1 -b .rh669163

%build
export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
export CPPFLAGS="$CPPFLAGS -DDIG_SIGCHASE"
export STD_CDEFINES="$CPPFLAGS"

libtoolize -c -f; aclocal -I libtool.m4 --force; autoconf -f

%configure \
  --with-python=%{__python3} \
  --with-libtool \
  --localstatedir=/var \
  --enable-threads \
  --enable-ipv6 \
  --enable-filter-aaaa \
  --enable-rrl \
  --with-pic \
  --enable-static \
  --disable-shared \
  --disable-openssl-version-check \
  --enable-exportlib \
  --with-export-libdir=%{_libdir} \
  --with-export-includedir=%{_includedir} \
  --includedir=%{_includedir}/bind9 \
  --with-tuning=large \
  --without-geoip \
  --without-libjson \
  --enable-fixed-rrset \
  --with-docbook-xsl=%{_datadir}/sgml/docbook/xsl-stylesheets

make %{?_smp_mflags}

# Regenerate dig.1 manpage
pushd bin/dig
make man
popd

pushd bin/python
make man
popd

%install
rm -rf ${RPM_BUILD_ROOT}

make DESTDIR=${RPM_BUILD_ROOT} install

# Remove unwanted files
rm -f ${RPM_BUILD_ROOT}/etc/bind.keys

rm -rf ${RPM_BUILD_ROOT}%{_includedir}
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man3
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man5
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man8
rm -rf ${RPM_BUILD_ROOT}%{_libdir}
rm -rf ${RPM_BUILD_ROOT}%{_sbindir}
rm -rf ${RPM_BUILD_ROOT}%{_bindir}/bind9-config
rm -rf ${RPM_BUILD_ROOT}%{_bindir}/isc-config.sh
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man1/bind9-config.1*
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man1/isc-config.sh.1*
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man1/named-rrchecker.1*
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man1/arpaname.1*


%clean
rm -rf ${RPM_BUILD_ROOT}:;

%files utils
%defattr(-,root,root,-)
%{_bindir}/dig
%{_bindir}/delv
%{_bindir}/host
%{_bindir}/nslookup
%{_bindir}/nsupdate
%{_mandir}/man1/host.1*
%{_mandir}/man1/nsupdate.1*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/delv.1*
%{_mandir}/man1/nslookup.1*

%changelog
* Fri Aug 14 2015 Cjacker <cjacker@foxmail.com>
- initial build.
- only ship bind utils such as nslookup/dig etc.
