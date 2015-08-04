# Pass --with externalfuse to compile against system fuse lib
# Default is internal fuse-lite.
%define with_externalfuse %{?_with_externalfuse:1}%{!?_with_externalfuse:0}

# For release candidates
# %%global subver -RC

Name:		ntfs-3g
Summary:	Linux NTFS userspace driver
Version:	2015.3.14
Release:    1	
License:	GPLv2+
Group:		System Environment/Base
Source0:	http://tuxera.com/opensource/%{name}_ntfsprogs-%{version}%{?subver}.tgz
URL:		http://www.ntfs-3g.org/
%if %{with_externalfuse}
BuildRequires:	fuse-devel
Requires:	fuse
%endif
BuildRequires:	libtool, libattr-devel
# ntfsprogs BuildRequires
BuildRequires:  libgcrypt-devel, gnutls-devel, libuuid-devel
Epoch:		2
Provides:	ntfsprogs-fuse = %{epoch}:%{version}-%{release}
Obsoletes:	ntfsprogs-fuse
Provides:	fuse-ntfs-3g = %{epoch}:%{version}-%{release}
Patch0:		ntfs-3g-musl-fixes.patch

%description
NTFS-3G is a stable, open source, GPL licensed, POSIX, read/write NTFS 
driver for Linux and many other operating systems. It provides safe 
handling of the Windows XP, Windows Server 2003, Windows 2000, Windows 
Vista, Windows Server 2008 and Windows 7 NTFS file systems. NTFS-3G can 
create, remove, rename, move files, directories, hard links, and streams; 
it can read and write normal and transparently compressed files, including 
streams and sparse files; it can handle special files like symbolic links, 
devices, and FIFOs, ACL, extended attributes; moreover it provides full 
file access right and ownership support.

%package devel
Summary:	Development files and libraries for ntfs-3g
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	pkgconfig
Provides:	ntfsprogs-devel = %{epoch}:%{version}-%{release}
# ntfsprogs-2.0.0-17 was never built. 2.0.0-16 was the last build for that 
# standalone package.
Obsoletes:	ntfsprogs-devel < 2.0.0-17

%description devel
Headers and libraries for developing applications that use ntfs-3g
functionality.

%package -n ntfsprogs
Summary:	NTFS filesystem libraries and utilities
Group:		System Environment/Base
# We don't really provide this. This code is dead and buried now.
Provides:	ntfsprogs-gnomevfs = %{epoch}:%{version}-%{release}
Obsoletes:	ntfsprogs-gnomevfs
# Needed to fix multilib issue
# ntfsprogs-2.0.0-17 was never built. 2.0.0-16 was the last build for that 
# standalone package.
Obsoletes:	ntfsprogs < 2.0.0-17

%description -n ntfsprogs
The ntfsprogs package currently consists of a library and utilities such as 
mkntfs, ntfscat, ntfsls, ntfsresize, and ntfsundelete (for a full list of 
included utilities see man 8 ntfsprogs after installation).

%prep
%setup -q -n %{name}_ntfsprogs-%{version}%{?subver}
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"
%configure \
	--disable-static \
	--disable-ldconfig \
%if 0%{?_with_externalfuse:1}
	--with-fuse=external \
%endif
	--exec-prefix=/ \
	--enable-crypto \
	--enable-extras 
make %{?_smp_mflags} LIBTOOL=%{_bindir}/libtool

%install
make LIBTOOL=%{_bindir}/libtool DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/*.a

rm -rf %{buildroot}/%{_sbindir}/mount.ntfs-3g
cp -a %{buildroot}/%{_bindir}/ntfs-3g %{buildroot}/%{_sbindir}/mount.ntfs-3g

# Actually make some symlinks for simplicity...
# ... since we're obsoleting ntfsprogs-fuse
pushd %{buildroot}/%{_bindir}
ln -s ntfs-3g ntfsmount
popd
pushd %{buildroot}/%{_sbindir}
ln -s mount.ntfs-3g mount.ntfs-fuse
# And since there is no other package in Fedora that provides an ntfs 
# mount...
ln -s mount.ntfs-3g mount.ntfs
# Need this for fsck to find it
ln -s ../bin/ntfsck fsck.ntfs
popd
mv %{buildroot}/sbin/* %{buildroot}/%{_sbindir}
rmdir %{buildroot}/sbin

# We get this on our own, thanks.
rm -rf %{buildroot}%{_defaultdocdir}/%{name}/README

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING CREDITS NEWS README
%{_sbindir}/mount.ntfs
%attr(754,root,root) %{_sbindir}/mount.ntfs-3g
%{_sbindir}/mount.ntfs-fuse
%{_sbindir}/mount.lowntfs-3g
%{_bindir}/ntfs-3g
%{_bindir}/ntfsmount
%{_bindir}/ntfs-3g.probe
%{_bindir}/ntfs-3g.secaudit
%{_bindir}/ntfs-3g.usermap
%{_bindir}/lowntfs-3g
%{_bindir}/ntfs-3g
%{_bindir}/ntfsmount
%{_libdir}/libntfs-3g.so.*
%{_mandir}/man8/mount.lowntfs-3g.*
%{_mandir}/man8/mount.ntfs-3g.*
%{_mandir}/man8/ntfs-3g*

%files devel
%{_includedir}/ntfs-3g/
%{_libdir}/libntfs-3g.so
%{_libdir}/pkgconfig/libntfs-3g.pc

%files -n ntfsprogs
%doc AUTHORS COPYING CREDITS ChangeLog NEWS README
%{_bindir}/ntfscat
%{_bindir}/ntfscluster
%{_bindir}/ntfscmp
%{_bindir}/ntfsfix
%{_bindir}/ntfsinfo
%{_bindir}/ntfsls
# Extras
%{_bindir}/ntfsdecrypt
%{_bindir}/ntfstruncate
%{_bindir}/ntfswipe
%{_sbindir}/fsck.ntfs
%{_sbindir}/mkfs.ntfs
%{_sbindir}/mkntfs
%{_sbindir}/ntfsclone
%{_sbindir}/ntfscp
%{_sbindir}/ntfslabel
%{_sbindir}/ntfsresize
%{_sbindir}/ntfsundelete
%{_mandir}/man8/mkntfs.8*
%{_mandir}/man8/mkfs.ntfs.8*
%{_mandir}/man8/ntfs[^m][^o]*.8*
%exclude %{_mandir}/man8/ntfs-3g*

%changelog
