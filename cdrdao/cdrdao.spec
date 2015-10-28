Summary:   Writes audio CD-Rs in disk-at-once (DAO) mode
Name:      cdrdao
Version:   1.2.3
Release:   26%{?dist}
License:   GPLv2+
URL:       http://cdrdao.sourceforge.net/
Source0:   http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:  libsigc++-devel
BuildRequires:  libvorbis-devel >= 1.0
BuildRequires:  libao-devel

# Missing includes causes failure build
Patch1: cdrdao-1.2.3-stat.patch
Patch2: cdrdao-1.2.3-helpmansync.patch
Patch3: cdrdao-1.2.3-format_security.patch

%description
Cdrdao records audio CD-Rs in disk-at-once (DAO) mode, based on a
textual description of the CD contents. Recording in DAO mode writes
the complete disc (lead-in, one or more tracks, and lead-out) in a
single step. DAO allows full control over the length and the contents
of pre-gaps, the pause areas between tracks.


%prep
%setup -q
%patch1 -p1 -b .stat
%patch2 -p1 -b .helpmansync
%patch3 -p1 -b .format_security

%build
#run autoreconf to support aarch64
#not needed when upstream moves to  new automake
#autoreconf -v -f -i -I.
%configure \
        --without-xdao \
        --without-scglib \
        --without-lame

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%files
%doc AUTHORS COPYING README CREDITS ChangeLog
%{_bindir}/cdrdao
%{_bindir}/*toc*
%{_datadir}/cdrdao
%{_mandir}/*/cdrdao*
%{_mandir}/*/cue2toc*
%{_mandir}/*/toc2cue*
%{_mandir}/*/toc2cddb*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.2.3-26
- Rebuild for new 4.0 release.

