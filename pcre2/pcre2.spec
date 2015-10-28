Name:       pcre2
Version:    10.20
Release:    3
Summary:    Perl-compatible regular expression library
# the library:                          BSD
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
#Not distributed in binary package
# autotools:                            GPLv3+ with exception
# install-sh:                           MIT
License:    BSD
URL:        http://www.pcre.org/
Source:     ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{?rcversion:Testing/}%{name}-%{version}.tar.bz2
# Fix compiling classes with a negative escape and a property escape,
# upstream bug #1697, fixed in upstream after 10.20.
Patch1:     pcre2-10.20-Fix-compiler-bug-for-classes-such-as-W-p-Any.patch
# Fix integer overflow for patterns whose minimum matching length is large,
# upstream bug #1699, fixed in upstream after 10.20.
Patch2:     pcre2-10.20-Fix-integer-overflow-for-patterns-whose-minimum-matc.patch

# New libtool to get rid of RPATH and to use distribution autotools
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  readline-devel

%description
PCRE2 is a re-working of the original PCRE (Perl-compatible regular
expression) library to provide an entirely new API.

PCRE2 is written in C, and it has its own API. There are three sets of
functions, one for the 8-bit library, which processes strings of bytes, one
for the 16-bit library, which processes strings of 16-bit values, and one for
the 32-bit library, which processes strings of 32-bit values. There are no C++
wrappers.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.


%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   gcc

%description devel
Development files (headers, libraries for dynamic linking, documentation)
for %{name}.  The header file for the POSIX-style functions is called
pcre2posix.h.

%package static
Summary:    Static library for %{name}
Requires:   %{name}-devel%{_isa} = %{version}-%{release}

%description static
Library for static linking for %{name}.

%package tools
Summary:    Auxiliary utilities for %{name}
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
License:    BSD and GPLv3+
Requires:   %{name}%{_isa} = %{version}-%{release}

%description tools
Utilities demonstrating PCRE2 capabilities like pcre2grep or pcre2test.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
# Because of multilib patch
libtoolize --copy --force
autoreconf -vif

%build
%configure \
    --enable-jit \
    --enable-pcre2grep-jit \
    --disable-bsr-anycrlf \
    --disable-coverage \
    --disable-ebcdic \
    --enable-newline-is-lf \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --disable-pcre2test-libedit \
    --enable-pcre2test-libreadline \
    --disable-pcre2grep-libbz2 \
    --disable-pcre2grep-libz \
    --disable-rebuild-chartables \
    --enable-shared \
    --enable-stack-for-recursion \
    --enable-static \
    --enable-unicode \
    --disable-valgrind
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre2

%check
make %{?_smp_mflags} check VERBOSE=yes

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS README

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre2-config.*
%{_mandir}/man3/*
%{_bindir}/pcre2-config
%doc doc/*.txt doc/html
%doc HACKING ./src/pcre2demo.c

%files static
%{_libdir}/*.a
%{!?_licensedir:%global license %%doc}
%license COPYING LICENCE

%files tools
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
%{_mandir}/man1/pcre2grep.*
%{_mandir}/man1/pcre2test.*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 10.20-3
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- initial build.
