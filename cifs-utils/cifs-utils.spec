Name:           cifs-utils
Version:        6.4
Release:        1
Summary:        Utilities for mounting and managing CIFS mounts

Group:          System Environment/Daemons
License:        GPLv3
URL:            http://linux-cifs.samba.org/cifs-utils/


Source0:        ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2
Patch0:         cifs-utils-fix-missing-header.patch

BuildRequires:  krb5-devel autoconf automake

%description
The SMB/CIFS protocol is a standard file sharing protocol widely deployed
on Microsoft Windows machines. This package contains tools for mounting
shares on Linux using the SMB/CIFS protocol. The tools in this package
work in conjunction with support in the kernel to allow one to mount a
SMB/CIFS share onto a client and use it as if it were a standard Linux
file system.

%package devel
Summary:        Files needed for building plugins for cifs-utils
Group:          Development/Libraries

%description devel
The SMB/CIFS protocol is a standard file sharing protocol widely deployed
on Microsoft Windows machines. This package contains the header file
necessary for building ID mapping plugins for cifs-utils.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%configure --prefix=/usr ROOTSBINDIR=%{_sbindir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_libdir}/%{name}/idmapwb.so %{buildroot}%{_sysconfdir}/%{name}/idmap-plugin
mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/mount.cifs
%{_mandir}/man8/mount.cifs.8.gz
/etc/cifs-utils/idmap-plugin
/etc/request-key.d/cifs.idmap.conf
/etc/request-key.d/cifs.spnego.conf
/usr/bin/getcifsacl
/usr/bin/setcifsacl
/usr/lib/cifs-utils/idmapwb.so
/usr/share/man/man1/getcifsacl.1.gz
/usr/share/man/man1/setcifsacl.1.gz
/usr/share/man/man8/idmapwb.8.gz

%files devel
%{_includedir}/cifsidmap.h

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

