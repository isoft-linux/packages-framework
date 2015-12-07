Name:           nftables
Version:        0.5
Release:        2%{?dist}
Summary:        Netfilter Tables userspace utillites

License:        GPLv2
URL:            http://netfilter.org/projects/nftables/
Source0:        http://ftp.netfilter.org/pub/nftables/nftables-%{version}.tar.bz2

BuildRequires: flex
BuildRequires: bison
BuildRequires: libmnl-devel
BuildRequires: gmp-devel
BuildRequires: readline-devel
BuildRequires: libnftnl-devel
BuildRequires: docbook2X

%description
Netfilter Tables userspace utilities.

%prep
%setup -q

%build
%configure --disable-silent-rules
#fix build man when docbook2man exist.
sed -i 's|${DB2MAN}|${DB2X_DOCBOOK2MAN}|g' doc/Makefile
make %{?_smp_mflags}

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
chmod 644 $RPM_BUILD_ROOT/%{_mandir}/man8/nft*

%files
%doc COPYING TODO
%config(noreplace) %{_sysconfdir}/nftables/
%{_sbindir}/nft
%{_mandir}/man8/nft*

%changelog
* Mon Dec 07 2015 Cjacker <cjacker@foxmail.com> - 0.5-2
- Initial build

