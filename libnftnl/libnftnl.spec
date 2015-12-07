Name:           libnftnl
Version:        1.0.5
Release:        2%{?dist}
Summary:        Library for low-level interaction with nftables Netlink's API over libmnl

License:        GPLv2+
URL:            http://netfilter.org/projects/libnftnl/
Source0:        http://ftp.netfilter.org/pub/libnftnl/libnftnl-%{version}.tar.bz2

BuildRequires:  libmnl-devel
BuildRequires:  mxml-devel
BuildRequires:  jansson-devel

%description
A library for low-level interaction with nftables Netlink's API over libmnl.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static --disable-silent-rules --with-json-parsing --with-xml-parsing
make %{?_smp_mflags}

%check
make %{?_smp_mflags} check
#may failed in koji, run native
#cd tests
#sh ./test-script.sh

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING
%{_libdir}/*.so.*

%files devel
%{_libdir}/libnft*.so
%{_libdir}/pkgconfig/libnftnl.pc
%{_includedir}/libnftnl

%changelog
* Mon Dec 07 2015 Cjacker <cjacker@foxmail.com> - 1.0.5-2
- Initial build

