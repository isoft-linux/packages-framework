%global glib2_version                   2.36
%global gobject_introspection_version   1.30.0
%global polkit_version                  0.102
%global systemd_version                 209
%global libatasmart_version             0.17
%global dbus_version                    1.4.0

Summary: Disk Manager
Name: udisks2
Version: 2.1.6
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://www.freedesktop.org/wiki/Software/udisks
Source0: http://udisks.freedesktop.org/releases/udisks-%{version}.tar.bz2
Patch0: udisks-2.1.6-fix-udisksctl-segfault.patch

BuildRequires: pkgconfig(gio-unix-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gobject-introspection-1.0) >= %{gobject_introspection_version}
BuildRequires: pkgconfig(gudev-1.0) >= %{systemd_version}
BuildRequires: pkgconfig(libatasmart) >= %{libatasmart_version}
BuildRequires: pkgconfig(libsystemd) >= %{systemd_version}
BuildRequires: pkgconfig(polkit-gobject-1) >= %{polkit_version}
BuildRequires: libacl-devel
BuildRequires: chrpath
BuildRequires: gtk-doc
BuildRequires: intltool

# For systemd scriptlet snippets.
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# needed to pull in the system bus daemon
Requires: dbus >= %{dbus_version}
# needed to pull in the udev daemon
Requires: systemd >= %{systemd_version}
# we need at least this version for bugfixes / features etc.
Requires: libatasmart >= %{libatasmart_version}
# for mount, umount, mkswap
Requires: util-linux
# for mkfs.ext3, mkfs.ext3, e2label
Requires: e2fsprogs
# for mkfs.xfs, xfs_admin
Requires: xfsprogs
# for mkfs.vfat
Requires: dosfstools
# for partitioning
Requires: parted
Requires: gdisk
# for ejecting removable disks
Requires: eject

# for MD-RAID
Requires: mdadm

Requires: libudisks2%{?_isa} = %{version}-%{release}

%description
udisks provides a daemon, D-Bus API and command line tools for
managing disks and storage devices. This package is for the udisks 2.x
series.

%package -n libudisks2
Summary: Dynamic library to access the udisks daemon
Group: System Environment/Libraries
License: LGPLv2+

%description -n libudisks2
This package contains the dynamic library libudisks2, which provides
access to the udisks daemon. This package is for the udisks 2.x
series.

%package -n libudisks2-devel
Summary: Development files for libudisks2
Group: Development/Libraries
Requires: libudisks2%{?_isa} = %{version}-%{release}
License: LGPLv2+

%description -n libudisks2-devel
This package contains the development files for the library
libudisks2, a dynamic library, which provides access to the udisks
daemon. This package is for the udisks 2.x series.

%prep
%setup -q -n udisks-%{version}
%patch0 -p1

%build
%configure --enable-gtk-doc
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

chrpath --delete $RPM_BUILD_ROOT%{_sbindir}/umount.udisks2
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/udisksctl
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/udisks2/udisksd

%find_lang %{name}


%check
make check


%post
%systemd_post udisks2.service

%preun
%systemd_preun udisks2.service

%postun
%systemd_postun_with_restart udisks2.service

%post -n libudisks2 -p /sbin/ldconfig

%postun -n libudisks2 -p /sbin/ldconfig


%files -f %{name}.lang
%doc README AUTHORS NEWS HACKING
%dir %{_sysconfdir}/udisks2
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.UDisks2.conf
%{_datadir}/bash-completion/completions/udisksctl
%{_prefix}/lib/systemd/system/udisks2.service
%{_prefix}/lib/udev/rules.d/80-udisks2.rules
%{_sbindir}/umount.udisks2
%dir %{_libexecdir}/udisks2
%{_libexecdir}/udisks2/udisksd
%{_bindir}/udisksctl
%{_mandir}/man1/udisksctl.1*
%{_mandir}/man8/udisks.8*
%{_mandir}/man8/udisksd.8*
%{_mandir}/man8/umount.udisks2.8*
%{_datadir}/polkit-1/actions/org.freedesktop.udisks2.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.UDisks2.service
# Permissions for local state data are 0700 to avoid leaking information
# about e.g. mounts to unprivileged users
%attr(0700,root,root) %dir %{_localstatedir}/lib/udisks2

%files -n libudisks2
# The COPYING file contains both the GPL (daemon and tools) and LGPL (library
# and development headers).
%license COPYING
%{_libdir}/libudisks2.so.*
%{_libdir}/girepository-1.0/UDisks-2.0.typelib

%files -n libudisks2-devel
%{_libdir}/libudisks2.so
%dir %{_includedir}/udisks2
%dir %{_includedir}/udisks2/udisks
%{_includedir}/udisks2/udisks/*.h
%{_datadir}/gir-1.0/UDisks-2.0.gir
%dir %{_datadir}/gtk-doc/html/udisks2
%{_datadir}/gtk-doc/html/udisks2/*
%{_libdir}/pkgconfig/udisks2.pc

%changelog
