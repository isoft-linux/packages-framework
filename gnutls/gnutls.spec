%bcond_with dane
%bcond_with guile

Summary: A TLS protocol implementation
Name: gnutls
Version: 3.4.2
Release: 1
License: GPLv3+ and LGPLv2+
Group:  Framework/Runtime/Library 
BuildRequires: p11-kit-devel >= 0.20.2, gettext
BuildRequires: zlib-devel, readline-devel, libtasn1-devel >= 3.1
BuildRequires: libtool, automake, autoconf
BuildRequires: nettle-devel >= 2.7.1
BuildRequires: gperf
%if %{with dane}
BuildRequires: unbound-devel unbound-libs
%endif
%if %{with guile}
BuildRequires: guile-devel
%endif
URL: http://www.gnutls.org/
Source0: ftp://ftp.gnutls.org/gcrypt/gnutls/%{name}-%{version}.tar.xz
Source1: libgnutls-config
Patch1: gnutls-3.2.7-rpath.patch
Patch3: gnutls-3.1.11-nosrp.patch

# Wildcard bundling exception https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = 20130424

%package c++
Summary: The C++ interface to GnuTLS
Group:  Framework/Runtime/Library 
Requires: %{name} = %{version}-%{release}

%package devel
Summary: Development files for the %{name} package
Group:  Framework/Development/Library
Requires: %{name} = %{version}-%{release}
Requires: %{name}-c++ = %{version}-%{release}
%if %{with dane}
Requires: %{name}-dane = %{version}-%{release}
%endif
Requires: pkgconfig

%package utils
License: GPLv3+
Summary: Command line tools for TLS protocol
Group:  Framework/Runtime/Utility 
Requires: %{name} = %{version}-%{release}
%if %{with dane}
Requires: %{name}-dane = %{version}-%{release}
%endif

%if %{with dane}
%package dane
Summary: A DANE protocol implementation for GnuTLS
Requires: %{name} = %{version}-%{release}
%endif

%if %{with guile}
%package guile
Summary: Guile bindings for the GNUTLS library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: guile
%endif

%description
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 

%description c++
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 

%description devel
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains files needed for developing applications with
the GnuTLS library.

%description utils
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains command line TLS client and server and certificate
manipulation tools.

%if %{with dane}
%description dane
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains library that implements the DANE protocol for verifying
TLS certificates through DNSSEC.
%endif

%if %{with guile}
%description guile
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains Guile bindings for the library.
%endif

%prep
%setup -q

%patch1 -p1 -b .rpath
%patch3 -p1 -b .nosrp

sed 's/gnutls_srp.c//g' -i lib/Makefile.in
sed 's/gnutls_srp.lo//g' -i lib/Makefile.in


%build
export LDFLAGS="-Wl,--no-add-needed"
%configure --with-libtasn1-prefix=%{_prefix} \
           --with-included-libcfg \
           --enable-local-libopts \
           --disable-static \
           --disable-openssl-compatibility \
           --disable-srp-authentication \
	       --disable-non-suiteb-curves \
	   --with-system-priority-file=%{_sysconfdir}/crypto-policies/back-ends/gnutls.config \
	   --with-default-trust-store-pkcs11="pkcs11:model=p11-kit-trust;manufacturer=PKCS%2311%20Kit" \
%if %{with guile}
           --enable-guile \
%ifarch %{arm}
           --disable-largefile \
%endif
%else
           --disable-guile \
%endif
%if %{with dane}
	   --with-unbound-root-key-file=/var/lib/unbound/root.key \
           --enable-dane \
%else
           --disable-dane \
%endif
           --disable-rpath
# Note that the arm hack above is not quite right and the proper thing would
# be to compile guile with largefile support.
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/srptool
rm -f $RPM_BUILD_ROOT%{_bindir}/gnutls-srpcrypt
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/libgnutls-config
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/srptool.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*srp*
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libguile*.a
%if %{without dane}
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gnutls-dane.pc
%endif

%find_lang gnutls

%check
make check %{?_smp_mflags}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig

%if %{with dane}
%post dane -p /sbin/ldconfig

%postun dane -p /sbin/ldconfig
%endif

%if %{with guile}
%post guile -p /sbin/ldconfig

%postun guile -p /sbin/ldconfig
%endif

%files -f gnutls.lang
%defattr(-,root,root,-)
%{_libdir}/libgnutls.so.30*
%doc COPYING COPYING.LESSER README AUTHORS NEWS THANKS

%files c++
%{_libdir}/libgnutlsxx.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/libgnutls*-config
%{_includedir}/*
%{_libdir}/libgnutls*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%files utils
%defattr(-,root,root,-)
%{_bindir}/certtool
#%{_bindir}/tpmtool
#%{_bindir}/danetool
%{_bindir}/ocsptool
%{_bindir}/psktool
%{_bindir}/p11tool
%if %{with dane}
%{_bindir}/danetool
%endif
%{_bindir}/gnutls*
%{_mandir}/man1/*
%doc doc/certtool.cfg

%if %{with dane}
%files dane
%defattr(-,root,root,-)
%{_libdir}/libgnutls-dane.so.*
%endif

%if %{with guile}
%files guile
%defattr(-,root,root,-)
%{_libdir}/libguile*.so*
%{_datadir}/guile/site/gnutls
%{_datadir}/guile/site/gnutls.scm
%endif

%changelog
