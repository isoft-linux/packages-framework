Summary: Fast compression and decompression utilities
Name: ncompress
Version: 4.2.4.4
Release: 5
License: Public Domain
Group:  Applications/File
URL:    http://ncompress.sourceforge.net/
Source: http://prdownloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz

# allow to build ncompress
# ~> downstream
Patch0: ncompress-4.2.4.4-make.patch

# from dist-git commit 0539779d937
# (praiskup: removed redundant part as -DNOFUNCDEF is defined)
# ~> downstream
Patch1: ncompress-4.2.4.4-lfs.patch

# exit when too long filename is given (do not segfault)
# ~> #unknown
# ~> downstream
Patch2: ncompress-4.2.4.4-filenamelen.patch

# permit files > 2GB to be compressed
# ~> #126775
Patch3: ncompress-4.2.4.4-2GB.patch

# do not fail to compress on ppc/s390x
# ~> #207001
Patch4: ncompress-4.2.4.4-endians.patch

# use memmove instead of memcpy
# ~> 760657
# ~> downstream
Patch5: ncompress-4.2.4.4-memmove.patch

# silence gcc warnings
# ~> downstream
Patch6: ncompress-4.2.4.4-silence-gcc.patch

BuildRequires: glibc-devel fileutils

%description
The ncompress package contains the compress and uncompress file
compression and decompression utilities, which are compatible with the
original UNIX compress utility (.Z file extensions).  These utilities
can't handle gzipped (.gz file extensions) files, but gzip can handle
compressed files.

Install ncompress if you need compression/decompression utilities
which are compatible with the original UNIX compress utility.

%prep
%setup -q

# configure build system
# ~> downstream
%patch0 -p1 -b .configure-buildsystem

%ifarch sparc m68k armv4l ppc s390 s390x ppc64 sparc64
ARCH_FLAGS="$ARCH_FLAGS -DBYTEORDER=1234"
%endif

%ifarch alpha ia64
ARCH_FLAGS="$ARCH_FLAGS -DNOALLIGN=0"
%endif

sed "s/\$(ARCH_FLAGS)/$ARCH_FLAGS/" Makefile.def > Makefile

%patch1 -p1 -b .lfs
%patch2 -p1 -b .filenamelen
%patch3 -p1 -b .2GB
%patch4 -p1 -b .endians
%patch5 -p1 -b .memmove
%patch6 -p1 -b .silence-gcc

%build
make CC=gcc CFLAGS="%{optflags} %{?nc_endian} %{?nc_align}"

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -p -m755 compress $RPM_BUILD_ROOT/%{_bindir}
ln -sf compress $RPM_BUILD_ROOT/%{_bindir}/uncompress
install -p -m644 compress.1 $RPM_BUILD_ROOT%{_mandir}/man1
ln -sf compress.1 $RPM_BUILD_ROOT%{_mandir}/man1/uncompress.1

%files
%{_bindir}/compress
%{_bindir}/uncompress
%{_mandir}/man1/*
%doc LZW.INFO README

%changelog
