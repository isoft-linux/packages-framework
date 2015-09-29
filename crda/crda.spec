%define         crda_version    3.18
%define         regdb_version   2015.04.06

Name:           crda
Version:        %{crda_version}_%{regdb_version}
Release:        2%{?dist}
Summary:        Regulatory compliance daemon for 802.11 wireless networking

Group:          System Environment/Base
License:        ISC
URL:            http://www.linuxwireless.org/en/developers/Regulatory/CRDA
BuildRoot:      %{_tmppath}/%{name}-%{crda_version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kernel-headers >= 2.6.27
BuildRequires:  libnl3-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  pkgconfig python m2crypto
BuildRequires:  openssl

Requires:       udev, iw
Requires:       systemd >= 190

Source0:        http://www.kernel.org/pub/software/network/crda/crda-%{crda_version}.tar.xz
Source1:        http://www.kernel.org/pub/software/network/wireless-regdb/wireless-regdb-%{regdb_version}.tar.xz
Source2:        setregdomain
Source3:        setregdomain.1

# Add udev rule to call setregdomain on wireless device add
Patch0:         regulatory-rules-setregdomain.patch
# Do not call ldconfig in crda Makefile
Patch1:         crda-remove-ldconfig.patch


%description
CRDA acts as the udev helper for communication between the kernel
and userspace for regulatory compliance. It relies on nl80211
for communication. CRDA is intended to be run only through udev
communication from the kernel.


%package devel
Summary:        Header files for use with libreg. 
Group:          Development/System


%description devel
Header files to make use of libreg for accessing regulatory info.


%prep
%setup -q -c
%setup -q -T -D -a 1

%patch0 -p1 -b .setregdomain

cd crda-%{crda_version}
%patch1 -p1 -b .ldconfig-remove

%build
export CFLAGS="%{optflags}"

# Use our own signing key to generate regulatory.bin
cd wireless-regdb-%{regdb_version}

make %{?_smp_mflags} maintainer-clean
make %{?_smp_mflags} REGDB_PRIVKEY=key.priv.pem REGDB_PUBKEY=key.pub.pem

# Build CRDA using the new key and regulatory.bin from above
cd ../crda-%{crda_version}
cp ../wireless-regdb-%{regdb_version}/key.pub.pem pubkeys

make %{?_smp_mflags} SBINDIR=%{_sbindir}/ LIBDIR=%{_libdir}/ \
	REG_BIN=../wireless-regdb-%{regdb_version}/regulatory.bin


%install
rm -rf %{buildroot}

cd crda-%{crda_version}
cp LICENSE LICENSE.crda
cp README README.crda
make install DESTDIR=%{buildroot} MANDIR=%{_mandir}/ \
	SBINDIR=%{_sbindir}/ LIBDIR=%{_libdir}/

cd ../wireless-regdb-%{regdb_version}
cp LICENSE LICENSE.wireless-regdb
cp README README.wireless-regdb
make install DESTDIR=%{buildroot} MANDIR=%{_mandir}

install -D -pm 0755 %SOURCE2 %{buildroot}%{_sbindir}
install -D -pm 0644 %SOURCE3 %{buildroot}%{_mandir}/man1/setregdomain.1


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_sbindir}/regdbdump
%{_sbindir}/setregdomain
%{_libdir}/libreg.so
/lib/udev/rules.d/85-regulatory.rules
# location of database is hardcoded to /usr/lib/%{name}
/usr/lib/%{name}
%{_mandir}/man1/setregdomain.1*
%{_mandir}/man5/regulatory.bin.5*
%{_mandir}/man8/crda.8*
%{_mandir}/man8/regdbdump.8*
%license crda-%{crda_version}/LICENSE.crda
%license wireless-regdb-%{regdb_version}/LICENSE.wireless-regdb
%doc crda-%{crda_version}/README.crda
%doc wireless-regdb-%{regdb_version}/README.wireless-regdb


%files devel
%{_includedir}/reglib/nl80211.h
%{_includedir}/reglib/regdb.h
%{_includedir}/reglib/reglib.h



%changelog
