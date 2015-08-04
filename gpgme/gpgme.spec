Name:    gpgme
Summary: GnuPG Made Easy - high level crypto API
Version: 1.4.3
Release: 6

License: LGPLv2+
URL:     http://www.gnupg.org/related_software/gpgme/
Source0: ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-%{version}.tar.bz2.sig

Patch1: gpgme-1.3.2-config_extras.patch

# gpgsm t-verify check/test hangs if using gnupg2 < 2.0.22
# see http://bugs.g10code.com/gnupg/issue1493
Patch2: gpgme-1.4.3-no_gpgsm_t-verify.patch

# add -D_FILE_OFFSET_BITS... to gpgme-config, upstreamable
Patch3:  gpgme-1.3.2-largefile.patch

Patch4: gpgme-1.3.2-bufferoverflow.patch

BuildRequires: gawk
# see patch2 above, else we only need 2.0.4
BuildRequires: gnupg2 >= 2.0.22
BuildRequires: gnupg2-smime
BuildRequires: libgpg-error-devel >= 1.8
BuildRequires: pth-devel
BuildRequires: libassuan-devel >= 2.0.2

%define _with_gpg --with-gpg=%{_bindir}/gpg2
Requires: gnupg2


%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.  It provides a high-level crypto API for
encryption, decryption, signing, signature verification and key
management.

%package devel
Summary:  Development headers and libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libgpg-error-devel%{?_isa}
# http://bugzilla.redhat.com/676954
# TODO: see if -lassuan can be added to config_extras patch too -- Rex
#Requires: libassuan2-devel
%description devel
%{summary}


%prep
%setup -q

%patch1 -p1 -b .config_extras
#patch2 -p1 -b .no_gpgsm_t-verify
%patch3 -p1 -b .largefile
%patch4 -p1 -b .overflow

## HACK ALERT
# The config script already suppresses the -L if it's /usr/lib, so cheat and
# set it to a value which we know will be suppressed.
sed -i -e 's|^libdir=@libdir@$|libdir=@exec_prefix@/lib|g' src/gpgme-config.in


%build
%configure \
  --disable-static \
  --without-g13 \
  %{?_with_gpg}

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# unpackaged files
rm -fv $RPM_BUILD_ROOT%{_infodir}/dir
rm -fv $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rfv $RPM_BUILD_ROOT%{_datadir}/common-lisp/source/gpgme/


%check 
make check


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libgpgme.so.11*
%{_libdir}/libgpgme-pthread.so.11*


%files devel
%{_bindir}/gpgme-config
%ifarch %{multilib_arches}
%{_bindir}/gpgme-config.%{_target_cpu}
%{_includedir}/gpgme-%{__isa_bits}.h
%endif
%{_includedir}/gpgme.h
%{_libdir}/libgpgme*.so
%{_datadir}/aclocal/gpgme.m4


%changelog
