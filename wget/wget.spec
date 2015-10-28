Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.16.3
Release: 3%{?dist}
License: GPLv3+
Url: http://www.gnu.org/software/wget/
Source: ftp://ftp.gnu.org/gnu/wget/wget-%{version}.tar.xz

Patch2: wget-1.16.1-path.patch
Patch3: wget-1.16-dont-run-failing-test.patch

Provides: webclient
BuildRequires: openssl-devel, pkgconfig, gettext, autoconf, libidn-devel, libuuid-devel

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you are logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.

%prep
%setup -q
%patch2 -p1 -b .path
# don't run the Test-proxied-https-auth.px test since it fails with OpenSSL
# upstream is working on fix
%patch3 -p1 -b .test

%build
if pkg-config openssl ; then
    CPPFLAGS=`pkg-config --cflags openssl`; export CPPFLAGS
    LDFLAGS=`pkg-config --libs openssl`; export LDFLAGS
fi
%configure \
    --with-ssl=openssl \
    --enable-largefile \
    --enable-opie \
    --enable-digest \
    --enable-ntlm \
    --enable-nls \
    --enable-ipv6 \
    --disable-rpath

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CFLAGS="$RPM_OPT_FLAGS"
rm -rf $RPM_BUILD_ROOT/%{_infodir}

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS MAILING-LIST NEWS README COPYING doc/sample.wgetrc
%config(noreplace) %{_sysconfdir}/wgetrc
%{_mandir}/man1/wget.*
%{_bindir}/wget

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.16.3-3
- Rebuild for new 4.0 release.

