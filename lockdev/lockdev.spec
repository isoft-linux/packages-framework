# Where lock files are stored
%global _lockdir /run/lock/lockdev

%global checkout 20111007git
%global co_date  2011-10-07

Summary: A library for locking devices
Name: lockdev
Version: 1.0.4
Release: 0.20.%{checkout}%{?dist}
License: LGPLv2
Group: System Environment/Libraries
URL: https://alioth.debian.org/projects/lockdev/

# This is a nightly snapshot downloaded via
# https://alioth.debian.org/snapshots.php?group_id=100443
Source0: lockdev-%{version}.%{checkout}.tar.gz

Patch1: lockdev-euidaccess.patch

Requires(pre): shadow-utils
Requires(post): glibc
Requires(postun): glibc
Requires: systemd

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: systemd

%description
Lockdev provides a reliable way to put an exclusive lock to devices
using both FSSTND and SVr4 methods.

%package devel
Summary: The header files for the lockdev library
Group: System Environment/Libraries
Requires: lockdev = %{version}-%{release}

%description devel
The lockdev library provides a reliable way to put an exclusive lock
on devices using both FSSTND and SVr4 methods. The lockdev-devel
package contains the development headers.


%prep
%setup -q -n lockdev-scm-%{co_date}

# Replace access() calls with euidaccess() (600636#c33)
%patch1 -p1 -b .access

%build
# Generate version information from git release tag
./scripts/git-version > VERSION

# To satisfy automake
touch ChangeLog

# Bootstrap autotools
autoreconf --verbose --force --install

CFLAGS="%{optflags} -D_PATH_LOCK=\\\"%{_lockdir}\\\"" \
%configure --disable-static --enable-helper --disable-silent-rules

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la

# %%ghosted, but needs to be in buildroot
# on reboot re-created by %%{_prefix}/lib/tmpfiles.d/legacy.conf
mkdir -p %{buildroot}%{_lockdir}

%pre
getent group lock >/dev/null 2>&1 || groupadd -g 54 -r -f lock >/dev/null 2>&1 || :

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
# for the time until first reboot
%tmpfiles_create
fi

%postun -p /sbin/ldconfig


%files
%doc COPYING AUTHORS
%ghost %dir %attr(0775,root,lock) %{_lockdir}
%attr(2711,root,lock)  %{_sbindir}/lockdev
%{_libdir}/*.so.*
%{_mandir}/man8/*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/lockdev.pc
%{_mandir}/man3/*
%{_includedir}/*

%changelog
