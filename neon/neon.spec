Summary: An HTTP and WebDAV client library
Name: neon
Version: 0.30.1
Release: 8 
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.webdav.org/neon/
Source0: http://www.webdav.org/neon/neon-%{version}.tar.gz
BuildRequires: expat-devel, gnutls-devel, zlib-devel
BuildRequires: pkgconfig
Requires: ca-certificates

%description
neon is an HTTP and WebDAV client library, with a C interface;
providing a high-level interface to HTTP and WebDAV methods along
with a low-level interface for HTTP request handling.  neon
supports persistent connections, proxy servers, basic, digest and
Kerberos authentication, and has complete SSL support.

%package devel
Summary: Development libraries and C header files for the neon library
Group: Development/Libraries
Requires: neon = %{version}-%{release}, gnutls-devel, zlib-devel, expat-devel
Requires: pkgconfig
# Documentation is GPLv2+
License: LGPLv2+ and GPLv2+

%description devel
The development library for the C language HTTP and WebDAV client library.

%prep
%setup -q
%build
# Use standard system CA bundle:
%define cabundle %{_sysconfdir}/ssl/certs/ca-certificates.crt
%configure \
    --with-expat \
    --enable-shared \
    --disable-static \
    --enable-warnings \
    --with-ca-bundle=%{cabundle} \
    --with-ssl=openssl \
    --enable-threadsafe-ssl=posix \
    --without-gssapi
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%find_lang %{name}

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS TODO src/COPYING.LIB NEWS README THANKS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/neon.pc
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_libdir}/*.so

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

