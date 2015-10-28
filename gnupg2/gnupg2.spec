Summary: Utility for secure communication and data storage
Name:    gnupg2
Version: 2.1.5
Release: 3

License: GPLv3+
Source0: ftp://ftp.gnupg.org/gcrypt/%{?pre:alpha/}gnupg/gnupg-%{version}%{?pre}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/%{?pre:alpha/}gnupg/gnupg-%{version}%{?pre}.tar.bz2.sig
Patch3:  gnupg-2.0.20-secmem.patch
# non-upstreamable patch adding file-is-digest option needed for Copr
Patch4:  gnupg-2.1.3-file-is-digest.patch
Patch5:  gnupg-2.1.1-ocsp-keyusage.patch
Patch6:  gnupg-2.1.1-fips-algo.patch

URL:     http://www.gnupg.org/

BuildRequires: bzip2-devel
BuildRequires: libcurl-devel
BuildRequires: docbook-utils
BuildRequires: gettext
BuildRequires: libassuan-devel >= 2.1.0
BuildRequires: libgcrypt-devel >= 1.6.0
BuildRequires: libgpg-error-devel >= 1.16
BuildRequires: libksba-devel >= 1.3.0
BuildRequires: libusb-devel
BuildRequires: pcsc-lite-libs
BuildRequires: npth-devel
BuildRequires: readline-devel ncurses-devel
BuildRequires: zlib-devel
BuildRequires: gnutls-devel

Requires: pinentry

%if 0%{?rhel} > 5
# pgp-tools, perl-GnuPG-Interface requires 'gpg' (not sure why) -- Rex
Provides: gpg = %{version}-%{release}
# Obsolete GnuPG-1 package
Provides: gnupg = %{version}-%{release}
Obsoletes: gnupg <= 1.4.10
%endif

Provides: dirmngr = %{version}-%{release}
Obsoletes: dirmngr < 1.2.0-1

%package smime
Summary: CMS encryption and signing tool and smart card support for GnuPG
Requires: gnupg2 = %{version}-%{release}


%description
GnuPG is GNU's tool for secure communication and data storage.  It can
be used to encrypt data and to create digital signatures.  It includes
an advanced key management facility and is compliant with the proposed
OpenPGP Internet standard as described in RFC2440 and the S/MIME
standard as described by several RFCs.

GnuPG 2.0 is a newer version of GnuPG with additional support for
S/MIME.  It has a different design philosophy that splits
functionality up into several modules. The S/MIME and smartcard functionality
is provided by the gnupg2-smime package.

%description smime
GnuPG is GNU's tool for secure communication and data storage. This
package adds support for smart cards and S/MIME encryption and signing
to the base GnuPG package 

%prep
%setup -q -n gnupg-%{version}

%patch3 -p1 -b .secmem
%patch4 -p1 -b .file-is-digest
%patch5 -p1 -b .keyusage
%patch6 -p1 -b .fips

# pcsc-lite library major: 0 in 1.2.0, 1 in 1.2.9+ (dlopen()'d in pcsc-wrapper)
# Note: this is just the name of the default shared lib to load in scdaemon,
# it can use other implementations too (including non-pcsc ones).
%global pcsclib %(basename $(ls -1 %{_libdir}/libpcsclite.so.? 2>/dev/null ) 2>/dev/null )

sed -i -e 's/"libpcsclite\.so"/"%{pcsclib}"/' scd/scdaemon.c


%build

%configure \
  --disable-rpath \
  --disable-gpgtar \
  --enable-standard-socket

# need scratch gpg database for tests
mkdir -p $HOME/.gnupg

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} \
  INSTALL="install -p" 

%if ! (0%{?rhel} > 5)
# drop file conflicting with gnupg-1.x
rm -f %{buildroot}%{_mandir}/man1/gpg-zip.1*
# and rename another
rename gnupg.7 gnupg2.7 %{buildroot}%{_mandir}/man7/gnupg.7*
%endif

%find_lang %{name}

# gpgconf.conf
mkdir -p %{buildroot}%{_sysconfdir}/gnupg
touch %{buildroot}%{_sysconfdir}/gnupg/gpgconf.conf

# info dir
rm -rf %{buildroot}%{_infodir}


%check
# need scratch gpg database for tests
mkdir -p $HOME/.gnupg
# some gpg2 tests (still) FAIL on non i386 platforms
make -k check


%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_sysconfdir}/gnupg
%ghost %config(noreplace) %{_sysconfdir}/gnupg/gpgconf.conf
%{_bindir}/gpg2
%{_bindir}/gpgv2
%{_bindir}/gpg-connect-agent
%{_bindir}/gpg-agent
%{_bindir}/gpgconf
%{_bindir}/gpgparsemail
%{_bindir}/g13
%{_bindir}/dirmngr
%{_bindir}/dirmngr-client
%if 0%{?rhel} > 5
%{_bindir}/gpg
%{_bindir}/gpgv
%{_bindir}/gpgsplit
%{_bindir}/gpg-zip
%else
%{_bindir}/gpgkey2ssh
%endif
%{_bindir}/watchgnupg
%{_sbindir}/*
%{_datadir}/gnupg/
%{_libexecdir}/*
%{_mandir}/man?/*
%exclude %{_datadir}/gnupg/com-certs.pem
%exclude %{_mandir}/man?/gpgsm*
%exclude %{_mandir}/man?/scdaemon*
%exclude %{_libexecdir}/scdaemon

%files smime
%defattr(-,root,root,-)
%{_bindir}/gpgsm*
%{_bindir}/kbxutil
%{_libexecdir}/scdaemon
%{_mandir}/man?/gpgsm*
%{_mandir}/man?/scdaemon*
%{_datadir}/gnupg/com-certs.pem


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.1.5-3
- Rebuild for new 4.0 release.

