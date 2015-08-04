Summary: A collection of CD/DVD utilities
Name: cdrkit
Version: 1.1.11
Release: 11 
License: GPLv2
Group: Applications/System
URL: http://cdrkit.org/
Source: http://cdrkit.org/releases/cdrkit-%{version}.tar.gz

BuildRequires: cmake libcap-devel zlib-devel perl file-devel bzip2-devel

%description
cdrkit is a collection of CD/DVD utilities.

%prep
%setup -q 

find . -type f -print0 | xargs -0 perl -pi -e 's#/usr/local/bin/perl#/usr/bin/perl#g'
find doc -type f -print0 | xargs -0 chmod a-x 

%build
# disable rcmd, it is security risk and not implemented in musl
sed -i include/xconfig.h.in -e "s/#define HAVE_RCMD 1/#undef HAVE_RCMD/g"   
export CFLAGS="$RPM_OPT_FLAGS -D__THROW=''"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/usr
perl -pi -e 's#^require v5.8.1;##g' $RPM_BUILD_ROOT%{_bindir}/dirsplit
ln -s genisoimage $RPM_BUILD_ROOT%{_bindir}/mkisofs
ln -s genisoimage $RPM_BUILD_ROOT%{_bindir}/mkhybrid
ln -s icedax $RPM_BUILD_ROOT%{_bindir}/cdda2wav
ln -s wodim $RPM_BUILD_ROOT%{_bindir}/cdrecord
ln -s wodim $RPM_BUILD_ROOT%{_bindir}/dvdrecord

# missing man page. Do symlink like in debian
ln -sf wodim.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1/netscsid.1.gz

# we don't need cdda2mp3 since we don't have any mp3 {en,de}coder
rm $RPM_BUILD_ROOT%{_bindir}/cdda2mp3

%files 
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man*/*

%changelog
