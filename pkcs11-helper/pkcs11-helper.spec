Name:           pkcs11-helper
Version:        1.11
Release:        6
Summary:        A library for using PKCS#11 providers

Group:          System Environment/Libraries
License:        GPLv2 or BSD
URL:            http://www.opensc-project.org/opensc/wiki/pkcs11-helper
Source0:        http://downloads.sourceforge.net/opensc/pkcs11-helper-%{version}.tar.bz2
Patch1:         0001-certificate-ignore-certificates-without-CKA_ID.patch
Patch2:         pkcs11-helper-rfc7512.patch

BuildRequires:  doxygen graphviz
BuildRequires:  openssl-devel

%description
pkcs11-helper is a library that simplifies the interaction with PKCS#11
providers for end-user applications using a simple API and optional OpenSSL
engine. The library allows using multiple PKCS#11 providers at the same time,
enumerating available token certificates, or selecting a certificate directly
by serialized id, handling card removal and card insert events, handling card
re-insert to a different slot, supporting session expiration and much more all
using a simple API. 

%package        devel
Summary:        Development files for pkcs11-helper
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel
# for /usr/share/aclocal
Requires:       automake

%description    devel
This package contains header files and documentation necessary for developing
programs using the pkcs11-helper library.


%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
%configure --disable-static --enable-doc
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Use %%doc to install documentation in a standard location
mkdir apidocdir
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/api/ apidocdir/
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/

# Remove libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING* README THANKS
%{_libdir}/libpkcs11-helper.so.*


%files devel
%doc apidocdir/*
%{_includedir}/pkcs11-helper-1.0/
%{_libdir}/libpkcs11-helper.so
%{_libdir}/pkgconfig/libpkcs11-helper-1.pc
%{_datadir}/aclocal/pkcs11-helper-1.m4
%{_mandir}/man8/pkcs11-helper-1.8*


%changelog
