Summary:	Toolchain to master DVD+RW/+R media
Name:		dvd+rw-tools
Version:	7.1
Release:	19%{?dist}
License:	GPLv2
Group:		Applications/Multimedia
Source:		http://fy.chalmers.se/~appro/linux/DVD+RW/tools/dvd+rw-tools-%{version}.tar.gz
Source1:	index.html
Patch1:		dvd+rw-tools-7.0.manpatch
Patch2:		dvd+rw-tools-7.0-wexit.patch
Patch3:		dvd+rw-tools-7.0-glibc2.6.90.patch
Patch4:		dvd+rw-tools-7.0-reload.patch
Patch5:		dvd+rw-tools-7.0-wctomb.patch
Patch6:		dvd+rw-tools-7.0-dvddl.patch
Patch7:		dvd+rw-tools-7.1-noevent.patch
Patch8:		dvd+rw-tools-7.1-lastshort.patch
Patch9:		dvd+rw-tools-7.1-format.patch
Patch10:	dvd+rw-tools-7.1-bluray_srm+pow.patch
Patch11:	dvd+rw-tools-7.1-bluray_pow_freespace.patch
URL:		http://fy.chalmers.se/~appro/linux/DVD+RW/
Requires:   cdrkit	
BuildRequires:	kernel-headers m4

%description
Collection of tools to master DVD+RW/+R media. For further
information see http://fy.chalmers.se/~appro/linux/DVD+RW/.

%prep
%setup -q
%patch1 -p1 -b .manpatch
%patch2 -p1 -b .wexit
%patch3 -p1 -b .glibc2.6.90
%patch4 -p1 -b .reload
%patch5 -p0 -b .wctomb
%patch6 -p0 -b .dvddl
%patch7 -p1 -b .noevent
%patch8 -p1 -b .lastshort
%patch9 -p1 -b .format
%patch10 -p1 -b .pow
%patch10 -p1 -b .freespace

install -m 644 %{SOURCE1} index.html

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
make WARN="-DDEFAULT_BUF_SIZE_MB=16 -DRLIMIT_MEMLOCK" %{?_smp_mflags}

%install
# make install DESTDIR= does not work here
%makeinstall

%files
%doc index.html LICENSE
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
