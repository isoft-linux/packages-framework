
Summary: Open implementation of Service Location Protocol V2
Name:    openslp
Version: 2.0.0
Release: 8

License: BSD
URL:     http://sourceforge.net/projects/openslp/
Source0: http://downloads.sf.net/openslp/openslp-%{version}.tar.gz

Source1: slpd.init
# Source1,2: simple man pages (slightly modified help2man output)
Source2: slpd.8.gz
Source3: slptool.1.gz
# Source3: service file
Source4: slpd.service

# Patch1: creates script from upstream init script that sets multicast
#     prior to the start of the service
Patch1:  openslp-2.0.0-multicast-set.patch
# Patch2: notify systemd of start-up completion
Patch2:  openslp-2.0.0-notify-systemd-of-start-up.patch

BuildRequires: automake libtool
BuildRequires: bison
BuildRequires: flex 
BuildRequires: openssl-devel
BuildRequires: systemd-units systemd-devel

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined
by RFC 2608 and RFC 2614.

%package devel
Summary: OpenSLP headers and libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
OpenSLP header files and libraries.

%package server
Summary: OpenSLP server daemon
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: net-tools
%description server
OpenSLP server daemon to dynamically register services.


%prep
%setup -q

%patch1 -p1 -b .multicast-set
%patch2 -p2 -b .systemd

# tarball goof (?), it wants to re-automake anyway, so let's do it right.
#libtoolize --force
#aclocal
#autoconf
#automake --add-missing
autoreconf -f -i

# remove CVS leftovers...
find . -name "CVS" | xargs rm -rf


%build

# for x86_64
export CFLAGS="-fPIC -fno-strict-aliasing -fPIE -DPIE $RPM_OPT_FLAGS"
# for slpd
export LDFLAGS="-pie -Wl,-z,now"

%configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --sysconfdir=%{_sysconfdir} \
  --localstatedir=/var \
  --disable-dependency-tracking \
  --disable-static \
  --enable-slpv2-security \
  --disable-rpath \
  --enable-async-api

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/slp.reg.d

# install script that sets multicast
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/%{name}-server
install -m 0755 etc/slpd.all_init ${RPM_BUILD_ROOT}/usr/lib/%{name}-server/slp-multicast-set.sh

# install service file
mkdir -p ${RPM_BUILD_ROOT}/%{_unitdir}
install -p -m 644 %{SOURCE4} ${RPM_BUILD_ROOT}/%{_unitdir}/slpd.service

# install man page
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8/
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1/
cp %SOURCE2 ${RPM_BUILD_ROOT}/%{_mandir}/man8/
cp %SOURCE3 ${RPM_BUILD_ROOT}/%{_mandir}/man1/

# nuke unpackaged/unwanted files
rm -rf $RPM_BUILD_ROOT/usr/doc
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post server
%systemd_post slpd.service

%preun server
%systemd_preun slpd.service

%postun server
%systemd_postun_with_restart slpd.service


%files
%defattr(-,root,root)
%doc AUTHORS COPYING FAQ NEWS README THANKS
%config(noreplace) %{_sysconfdir}/slp.conf
%{_bindir}/slptool
%{_libdir}/libslp.so.1*
%{_mandir}/man1/*

%files server
%defattr(-,root,root)
%doc doc/doc/html/IntroductionToSLP
%doc doc/doc/html/UsersGuide
%doc doc/doc/html/faq*
%{_sbindir}/slpd
%config(noreplace) %{_sysconfdir}/slp.reg
%config(noreplace) %{_sysconfdir}/slp.spi
%{_unitdir}/slpd.service
%{_mandir}/man8/*
/usr/lib/%{name}-server/slp-multicast-set.sh

%files devel
%defattr(-,root,root)
%doc doc/doc/html/ProgrammersGuide
%doc doc/doc/rfc
%{_includedir}/slp.h
%{_libdir}/libslp.so


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.0.0-8
- Rebuild for new 4.0 release.

