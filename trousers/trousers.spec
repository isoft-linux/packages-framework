Name: trousers
Summary: TCG's Software Stack v1.2
Version: 0.3.13
Release: 5
License: BSD
Group: System Environment/Libraries
Url: http://trousers.sourceforge.net

Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: tcsd.service
Patch1:  trousers-0.3.13-noinline.patch

BuildRequires: libtool, openssl-devel
BuildRequires: systemd
Requires(pre): shadow-utils
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: %{name}-lib%{?_isa} = %{version}-%{release}

%description
TrouSerS is an implementation of the Trusted Computing Group's Software Stack
(TSS) specification. You can use TrouSerS to write applications that make use
of your TPM hardware. TPM hardware can create, store and use RSA keys
securely (without ever being exposed in memory), verify a platform's software
state using cryptographic hashes and more.

%package lib
Summary: TrouSerS libtspi library
Group: Development/Libraries
# Needed obsoletes due to the -lib subpackage split
Obsoletes: trousers < 0.3.13-4

%description lib
The libtspi library for use in Trusted Computing enabled applications.

%package static
Summary: TrouSerS TCG Device Driver Library
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The TCG Device Driver Library (TDDL) used by the TrouSerS tcsd as the
interface to the TPM's device driver. For more information about writing
applications to the TDDL interface, see the latest TSS spec at
https://www.trustedcomputinggroup.org/specs/TSS.

%package devel
Summary: TrouSerS header files and documentation
Group: Development/Libraries
Requires: %{name}-lib%{?_isa} = %{version}-%{release}

%description devel
Header files and man pages for use in creating Trusted Computing enabled
applications.

%prep
%setup -q
%patch1 -p1 -b .noinline
# fix man page paths
sed -i -e 's|/var/tpm|/var/lib/tpm|g' -e 's|/usr/local/var|/var|g' man/man5/tcsd.conf.5.in man/man8/tcsd.8.in

%build
%configure --with-gui=openssl
make -k %{?_smp_mflags}

%install
mkdir -p ${RPM_BUILD_ROOT}/%{_localstatedir}/lib/tpm
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/libtspi.la
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/

%pre
getent group tss >/dev/null || groupadd -g 59 -r tss
getent passwd tss >/dev/null || \
useradd -r -u 59 -g tss -d /dev/null -s /sbin/nologin \
 -c "Account used by the trousers package to sandbox the tcsd daemon" tss
exit 0

%post
%systemd_post tcsd.service

%preun
%systemd_preun tcsd.service

%postun
%systemd_postun_with_restart tcsd.service 

%post lib -p /sbin/ldconfig

%postun lib -p /sbin/ldconfig

%files
%doc README ChangeLog
%{_sbindir}/tcsd
%config(noreplace) %attr(0600, tss, tss) %{_sysconfdir}/tcsd.conf
%{_mandir}/man5/*
%{_mandir}/man8/*
%attr(644,root,root) %{_unitdir}/tcsd.service
%attr(0700, tss, tss) %{_localstatedir}/lib/tpm/

%files lib
%license LICENSE
%{_libdir}/libtspi.so.?
%{_libdir}/libtspi.so.?.?.?

%files devel
# The files to be used by developers, 'trousers-devel'
%doc doc/LTC-TSS_LLD_08_r2.pdf doc/TSS_programming_SNAFUs.txt
%attr(0755, root, root) %{_libdir}/libtspi.so
%{_includedir}/tss/
%{_includedir}/trousers/
%{_mandir}/man3/Tspi_*

%files static
# The only static library shipped by trousers, the TDDL
%{_libdir}/libtddl.a

%changelog
