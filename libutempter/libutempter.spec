%define utempter_compat_ver 0.5.2

Summary: A privileged helper for utmp/wtmp updates
Name: libutempter
Version: 1.1.6
Release: 2%{?dist}
License: LGPLv2+
URL: ftp://ftp.altlinux.org/pub/people/ldv/utempter

Source0: ftp://ftp.altlinux.org/pub/people/ldv/utempter/%{name}-%{version}.tar.bz2

# Compile with PIE and RELRO flags.
Patch0: libutempter-pierelro.patch

Requires(pre): shadow-utils
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Provides: utempter = %{utempter_compat_ver}

%description
This library provides interface for terminal emulators such as
screen and xterm to record user sessions to utmp and wtmp files.

%package devel
Summary: Development environment for utempter
Requires: %{name} = %{version}-%{release}

%description devel
This package contains development files required to build
utempter-based software.

%prep
%setup -q
%patch0 -p1 -b .pierelro

%build
make CFLAGS="$RPM_OPT_FLAGS" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

%install
make install DESTDIR="$RPM_BUILD_ROOT" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

# NOTE: Static lib intentionally disabled.
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%pre
{
    %{_sbindir}/groupadd -g 22 -r -f utmp || :
    %{_sbindir}/groupadd -g 35 -r -f utempter || :
}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{_libdir}/libutempter.so.0
%{_libdir}/libutempter.so.1.*
%dir %attr(755,root,utempter) %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter

%files devel
%{_includedir}/utempter.h
%{_libdir}/libutempter.so
%{_mandir}/man3/*

%changelog
* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 1.1.6-2
- Initial build

