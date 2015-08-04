Summary: Mail processing program
Name: procmail
Version: 3.22
Release: 38
License: GPLv2+ or Artistic
Group: Applications/Internet
# Source: ftp://ftp.procmail.org/pub/procmail/procmail-%{version}.tar.gz
# The original source doesn't seem to be available anymore, using mirror
Source: ftp://ftp.ucsb.edu/pub/mirrors/procmail/procmail-%{version}.tar.gz
# Source2: http://www.linux.org.uk/~telsa/BitsAndPieces/procmailrc
# The Telsa config file doesn't seem to be available anymore, using local copy
Source2: procmailrc
URL: http://www.procmail.org
Patch0: procmail-3.22-rhconfig.patch
Patch1: procmail-3.15.1-man.patch
Patch2: procmail_3.22-8.debian.patch
Patch4: procmail-3.22-truncate.patch
Patch5: procmail-3.22-ipv6.patch
Patch6: procmail-3.22-getline.patch
Patch7: procmail-3.22-CVE-2014-3618.patch
Patch8: procmail-3.22-crash-fix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Procmail can be used to create mail-servers, mailing lists, sort your
incoming mail into separate folders/files (real convenient when subscribing
to one or more mailing lists or for prioritising your mail), preprocess
your mail, start any programs upon mail arrival (e.g. to generate different
chimes on your workstation for different types of mail) or selectively
forward certain incoming mail automatically to someone.

%prep
%setup -q
%patch0 -p1 -b .rhconfig
%patch1 -p1
%patch2 -p1
%patch4 -p1 -b .truncate
%patch5 -p1 -b .ipv6
%patch6 -p1 -b .getline
%patch7 -p1 -b .CVE-2014-3618
%patch8 -p1 -b .crash-fix

find examples -type f | xargs chmod 644

%build
make RPM_OPT_FLAGS="$(getconf LFS_CFLAGS)" autoconf.h
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS %{?hardened_flags} -Wno-comments $(getconf LFS_CFLAGS)"

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,5}

make \
    BASENAME=${RPM_BUILD_ROOT}%{_prefix} MANDIR=${RPM_BUILD_ROOT}%{_mandir} \
    install

cp debian/mailstat.1 ${RPM_BUILD_ROOT}%{_mandir}/man1
cp -p %{SOURCE2} telsas_procmailrc


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_bindir}/formail
%attr(2755,root,mail) %{_bindir}/lockfile
%{_bindir}/mailstat
%attr(0755,root,mail) %{_bindir}/procmail

%{_mandir}/man[15]/*

%changelog
