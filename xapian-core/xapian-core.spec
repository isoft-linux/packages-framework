Name:          xapian-core
Version:       1.2.21
Release:       2
Summary:       The Xapian Probabilistic Information Retrieval Library

License:       GPLv2+
URL:           http://www.xapian.org/
Source0:       http://www.oligarchy.co.uk/xapian/%{version}/%{name}-%{version}.tar.xz

BuildRequires: zlib-devel
BuildRequires: libuuid-devel
Requires:      %{name}-libs = %{version}-%{release}

%description
Xapian is an Open Source Probabilistic Information Retrieval Library. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications

%package libs
Summary:       Xapian search engine libraries

%description libs
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
libraries for applications using Xapian functionality

%package devel
Summary:       Files needed for building packages which use Xapian
Requires:      %{name} = %{version}-%{release}
Requires:      %{name}-libs = %{version}-%{release}

%description devel
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
files needed for building packages which use Xapian

%prep
%setup -q

%build
# Disable SSE on x86, but leave it intact for x86_64
%ifarch x86_64
%configure --disable-static
%else
%configure --disable-static --disable-sse
%endif

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

# Remove libtool archives
# find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Remove the dev docs, we pick them up below
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}/xapian*
%{_bindir}/quest
%{_bindir}/delve
%{_bindir}/copydatabase
%{_bindir}/simpleindex
%{_bindir}/simplesearch
%{_bindir}/simpleexpand
# man pages may be gzipped, hence the trailing wildcard.
%{_mandir}/man1/xapian*
%{_mandir}/man1/quest.1*
%{_mandir}/man1/delve.1*
%{_mandir}/man1/copydatabase.1*

%files libs
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libxapian.so.*

%files devel
%defattr(-, root, root)
%doc HACKING PLATFORMS docs/*html docs/apidoc docs/*pdf
%{_bindir}/xapian-config
%{_includedir}/xapian
%{_includedir}/xapian.h
%{_libdir}/libxapian.so
%{_libdir}/cmake/xapian
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/xapian.m4
# man pages may be gzipped, hence the trailing wildcard.
%{_mandir}/man1/xapian-config.1*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.2.21-2
- Rebuild for new 4.0 release.

