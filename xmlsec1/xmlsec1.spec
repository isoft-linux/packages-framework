Summary: Library providing support for "XML Signature" and "XML Encryption" standards
Name: xmlsec1
Version: 1.2.20
Release: 3
License: MIT
Source0: http://www.aleksey.com/xmlsec/download/xmlsec1-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL: http://www.aleksey.com/xmlsec/
BuildRequires: libxml2-devel >= 2.6.0
BuildRequires: libxslt-devel >= 1.1.0
BuildRequires: openssl-devel >= 0.9.6
BuildRequires: libgcrypt-devel >= 1.2.0
BuildRequires: gnutls-devel >= 1.0.20
BuildRequires: nss-devel >= 3.2
BuildRequires: nspr-devel
BuildRequires: libltdl-devel
# extra build deps needed for autoreconf after above patch
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool


%description
XML Security Library is a C library based on LibXML2  and OpenSSL.
The library was created with a goal to support major XML security
standards "XML Digital Signature" and "XML Encryption".

%package devel
Summary: Libraries, includes, etc. to develop applications with XML Digital Signatures and XML Encryption support.
Requires: xmlsec1%{?_isa} = %{version}-%{release}
Requires: libxml2-devel%{?_isa} >= 2.6.0
Requires: libxslt-devel%{?_isa} >= 1.1.0
Requires: openssl-devel%{?_isa} >= 0.9.6
Requires: zlib-devel%{?_isa}
# pkgconfig deps are automatic in Fedora and EL>=6
%if 0%{?rhel} == 5
Requires: pkgconfig
%endif

%description devel
Libraries, includes, etc. you can use to develop applications with XML Digital
Signatures and XML Encryption support.

%package openssl
Summary: OpenSSL crypto plugin for XML Security Library
Requires: xmlsec1%{?_isa} = %{version}-%{release}

%description openssl
OpenSSL plugin for XML Security Library provides OpenSSL based crypto services
for the xmlsec library.

%package openssl-devel
Summary: OpenSSL crypto plugin for XML Security Library
Requires: xmlsec1-devel%{?_isa} = %{version}-%{release}
Requires: xmlsec1-openssl%{?_isa} = %{version}-%{release}

%description openssl-devel
Libraries, includes, etc. for developing XML Security applications with OpenSSL

%package gcrypt
Summary: GCrypt crypto plugin for XML Security Library
Requires: xmlsec1%{?_isa} = %{version}-%{release}

%description gcrypt
GCrypt plugin for XML Security Library provides GCrypt based crypto services
for the xmlsec library.

%package gcrypt-devel
Summary: GCrypt crypto plugin for XML Security Library
Requires: xmlsec1-devel%{?_isa} = %{version}-%{release}
Requires: xmlsec1-gnutls-devel%{?_isa} = %{version}-%{release}

%description gcrypt-devel
Libraries, includes, etc. for developing XML Security applications with GCrypt.

%package gnutls
Summary: GNUTls crypto plugin for XML Security Library
Requires: xmlsec1%{?_isa} = %{version}-%{release}

%description gnutls
GNUTls plugin for XML Security Library provides GNUTls based crypto services
for the xmlsec library.

%package gnutls-devel
Summary: GNUTls crypto plugin for XML Security Library
Requires: xmlsec1-devel%{?_isa} = %{version}-%{release}
Requires: xmlsec1-openssl-devel%{?_isa} = %{version}-%{release}
Requires: libgcrypt-devel%{?_isa} >= 1.2.0
Requires: gnutls-devel%{?_isa} >= 1.0.20

%description gnutls-devel
Libraries, includes, etc. for developing XML Security applications with GNUTls.

%package nss
Summary: NSS crypto plugin for XML Security Library
Requires: xmlsec1%{?_isa} = %{version}-%{release}

%description nss
NSS plugin for XML Security Library provides NSS based crypto services
for the xmlsec library

%package nss-devel
Summary: NSS crypto plugin for XML Security Library
Requires: xmlsec1-devel%{?_isa} = %{version}-%{release}
Requires: xmlsec1-nss%{?_isa} = %{version}-%{release}
Requires: nss-devel%{?_isa} >= 3.2
Requires: nspr-devel%{?_isa}

%description nss-devel
Libraries, includes, etc. for developing XML Security applications with NSS.

%prep
%setup -q

%build
autoreconf -if
%configure --disable-static
V=1 make

# positively ugly but only sane way to get around #192756
sed 's+/lib64+/$archlib+g' < xmlsec1-config | sed 's+/lib+/$archlib+g' | sed 's+ -DXMLSEC_NO_SIZE_T++' > xmlsec1-config.$$ && mv xmlsec1-config.$$ xmlsec1-config

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/include/xmlsec1
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT/usr/man/man1

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# move installed docs to include them in -devel package via %%doc magic
rm -rf __tmp_doc ; mkdir __tmp_doc
mv ${RPM_BUILD_ROOT}%{_docdir}/xmlsec1/* __tmp_doc

%clean
rm -fr ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gnutls -p /sbin/ldconfig
%postun gnutls -p /sbin/ldconfig

%post openssl -p /sbin/ldconfig
%postun openssl -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog NEWS README Copyright
%{_mandir}/man1/xmlsec1.1*
%{_libdir}/libxmlsec1.so.*
%{_bindir}/xmlsec1

%files devel
%{_bindir}/xmlsec1-config
%dir %{_includedir}/xmlsec1
%dir %{_includedir}/xmlsec1/xmlsec
%dir %{_includedir}/xmlsec1/xmlsec/private
%{_includedir}/xmlsec1/xmlsec/*.h
%{_includedir}/xmlsec1/xmlsec/private/*.h
%{_libdir}/libxmlsec1.so
%{_libdir}/pkgconfig/xmlsec1.pc
%{_libdir}/xmlsec1Conf.sh
%{_datadir}/aclocal/xmlsec1.m4
%{_mandir}/man1/xmlsec1-config.1*
%doc HACKING __tmp_doc/*

%files openssl
%{_libdir}/libxmlsec1-openssl.so.*
%{_libdir}/libxmlsec1-openssl.so

%files openssl-devel
%{_includedir}/xmlsec1/xmlsec/openssl/
%{_libdir}/pkgconfig/xmlsec1-openssl.pc

%files gcrypt
%{_libdir}/libxmlsec1-gcrypt.so.*
%{_libdir}/libxmlsec1-gcrypt.so

%files gcrypt-devel
%{_includedir}/xmlsec1/xmlsec/gcrypt/
%{_libdir}/pkgconfig/xmlsec1-gcrypt.pc

%files gnutls
%{_libdir}/libxmlsec1-gnutls.so.*
%{_libdir}/libxmlsec1-gnutls.so

%files gnutls-devel
%{_includedir}/xmlsec1/xmlsec/gnutls/
%{_libdir}/pkgconfig/xmlsec1-gnutls.pc

%files nss
%{_libdir}/libxmlsec1-nss.so.*
%{_libdir}/libxmlsec1-nss.so

%files nss-devel
%{_includedir}/xmlsec1/xmlsec/nss/
%{_libdir}/pkgconfig/xmlsec1-nss.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.2.20-3
- Rebuild for new 4.0 release.

