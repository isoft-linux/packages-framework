%define _root_libdir    /%{_lib}

Summary: NFSv4 User and Group ID Mapping Library
Name: libnfsidmap
Version: 0.26
Release: 4.2%{?dist}
Provides: nfs-utils-lib
Obsoletes: nfs-utils-lib
URL: http://linux-nfs.org/wiki/index.php/Main_Page
License: BSD

Source0:  https://fedorapeople.org/~steved/%{name}/%{version}/%{name}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pkgconfig, openldap-devel
BuildRequires: automake, libtool
Requires(postun): /sbin/ldconfig
Requires(pre): /sbin/ldconfig
Requires: openldap

%description
Library that handles mapping between names and ids for NFSv4.

%package devel
Summary: Development files for the libnfsidmap library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

Patch001: libnfsidmap-0.27-rc3.patch

%description devel
This package includes header files and libraries necessary for
developing programs which use the libnfsidmap library.

%prep
%setup -q 

%patch001 -p1

rm configure.in
%build
./autogen.sh
%configure --disable-static  --with-pluginpath=%{_root_libdir}/%name
make %{?_smp_mflags} all

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} \
    libdir=%{_root_libdir} pkgconfigdir=%{_libdir}/pkgconfig

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_mandir}/man5

install -m 644 idmapd.conf %{buildroot}%{_sysconfdir}/idmapd.conf

# Delete unneeded libtool libs
rm -rf %{buildroot}%{_root_libdir}/*.{a,la}
rm -rf %{buildroot}%{_root_libdir}/%{name}/*.{a,la}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README COPYING
%config(noreplace) %{_sysconfdir}/idmapd.conf
%{_root_libdir}/*.so.*
%{_root_libdir}/%{name}
%{_root_libdir}/%{name}/*.so
%{_mandir}/*/*

%files devel
%defattr(0644,root,root,755)
%{_libdir}/pkgconfig/libnfsidmap.pc
%{_includedir}/nfsidmap.h
%{_root_libdir}/*.so

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.26-4.2
- Rebuild for new 4.0 release.

