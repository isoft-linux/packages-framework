Summary: The lrz and lsz modem communications programs
Name: lrzsz
Version: 0.12.20
Release: 39%{?dist}
License: GPLv2+
Source: http://www.ohse.de/uwe/releases/%{name}-%{version}.tar.gz
Patch1: lrzsz-0.12.20-glibc21.patch
Patch2: lrzsz-0.12.20.patch
Patch3: lrzsz-0.12.20-man.patch
Patch4: lrzsz-0.12.20-aarch64.patch
Url: http://www.ohse.de/uwe/software/lrzsz.html
BuildRequires: gettext

%description
Lrzsz (consisting of lrz and lsz) is a cosmetically modified
zmodem/ymodem/xmodem package built from the public-domain version of
the rzsz package. Lrzsz was created to provide a working GNU
copylefted Zmodem solution for Linux systems.

%prep
%setup -q

%patch1 -p1 -b .glibc21
%patch2 -p1 -b .crc
%patch3 -p1 -b .man
%patch4 -p1 -b .aarch64

rm -f po/*.gmo

%build
%configure --disable-pubdir \
           --enable-syslog \
           --program-transform-name=s/l//

make %{?_smp_mflags}

%install
%makeinstall
%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.12.20-39
- Rebuild for new 4.0 release.

