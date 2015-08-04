Name: cvs
Version: 1.11.23
Release: 39%{?dist}
Summary: Concurrent Versions System
Group: Development/Tools
URL: http://cvs.nongnu.org/
# Source files in zlib/ directory are licensed under zlib/libpng
# Other files are mostly GPL+, some of them are GPLv2+ or
# LGPLv2+ and there is vms/pathnames.h BSD licensed
# lib/md5.c is Public Domain.
License: BSD and GPL+ and GPLv2+ and LGPLv2+ and zlib and Public Domain
Source0: ftp://ftp.gnu.org/non-gnu/cvs/source/stable/%{version}/cvs-%{version}.tar.bz2
Source3: cvs.sh
Source8: cvs.sh.5
Requires: vim
BuildRequires: autoconf >= 2.58, automake >= 1.7.9, libtool, zlib-devel
BuildRequires: vim

# Fix up initial cvs login, bug #47457
Patch0: cvs-1.11.23-cvspass.patch
# Build against system zlib
Patch1: cvs-1.11.19-extzlib.patch
# Aadd 't' as a loginfo format specifier (print tag or branch name)
Patch2: cvs-1.11.19-netbsd-tag.patch
# Deregister SIGABRT handler in clean-up to prevent loop, bug #66019
Patch3: cvs-1.11.19-abortabort.patch
# Disable lengthy tests at build-time
Patch4: cvs-1.11.1p1-bs.patch
# Improve proxy support, bug #144297
Patch5: cvs-1.11.21-proxy.patch
# Do not accumulate new lines when reusing commit message, bug #64182
Patch7: cvs-1.11.19-logmsg.patch
# Disable slashes in tag name, bug #56162
Patch8: cvs-1.11.19-tagname.patch
# Fix NULL dereference, bug #63365
Patch9: cvs-1.11.19-comp.patch
# Fix insecure temporary file handling in cvsbug, bug #166366
Patch11: cvs-1.11.19-tmp.patch
# Add PAM support, bug #48937
Patch12: cvs-1.11.21-pam.patch
# Report unknown file when calling cvs diff with two -r options, bug #18161
Patch13: cvs-1.11.21-diff.patch
# Fix cvs diff -kk, bug #150031
Patch14: cvs-1.11.21-diff-kk.patch
# Enable obsolete sort option called by rcs2log, bug #190009
Patch15: cvs-1.11.21-sort.patch
# Add IPv6 support, bug #199404
Patch17: cvs-1.11.22-ipv6-proxy.patch
# getline(3) returns ssize_t, bug #449424
Patch19: cvs-1.11.23-getline64.patch
# Add support for passing arguments through standard input, bug #501942
Patch20: cvs-1.11.22-stdinargs.patch
# CVE-2010-3864, bug #645386
Patch21: cvs-1.11.23-cve-2010-3846.patch
# Remove undefinded date from cvs(1) header, bug #225672
Patch22: cvs-1.11.23-remove_undefined_date_from_cvs_1_header.patch
# Adjust tests to accept new style getopt argument quotation and SELinux label
# notation from ls(1)
Patch23: cvs-1.11.23-sanity.patch
# Run tests verbosely
Patch24: cvs-1.11.23-make_make_check_sanity_testing_verbose.patch
# Add KeywordExpand configuration keyword
Patch26: cvs-1.11.23-Back-port-KeywordExpand-configuration-keyword.patch
# bug #722972
Patch27: cvs-1.11.23-Allow-CVS-server-to-use-any-Kerberos-key-with-cvs-se.patch
# CVE-2012-0804, bug #787683
Patch28: cvs-1.11.23-Fix-proxy-response-parser.patch
# Pass compilation with -Wformat-security, bug #1037029, submitted to upstream
# as bug #40787
Patch31: cvs-1.11.23-Pass-compilation-with-Wformat-security.patch

%description
CVS (Concurrent Versions System) is a version control system that can
record the history of your files (usually, but not always, source
code). CVS only stores the differences between versions, instead of
every version of every file you have ever created. CVS also keeps a log
of who, when, and why changes occurred.

CVS is very helpful for managing releases and controlling the
concurrent editing of source files among multiple authors. Instead of
providing version control for a collection of files in a single
directory, CVS provides version control for a hierarchical collection
of directories consisting of revision controlled files. These
directories and files can then be combined together to form a software
release.


%prep
%setup -q
%patch0 -p1 -b .cvspass
%patch1 -p1 -b .extzlib
%patch2 -p1 -b .netbsd-tag
%patch3 -p1 -b .abortabort
%patch4 -p1 -b .bs
%patch5 -p1 -b .proxy
%patch7 -p1 -b .log
%patch8 -p1 -b .tagname
%patch9 -p1 -b .comp
%patch11 -p1 -b .tmp

%patch13 -p1 -b .diff
%patch14 -p1 -b .diff-kk
%patch15 -p1 -b .env
%patch17 -p1 -b .ipv6
%patch19 -p1 -b .getline64
%patch20 -p1 -b .stdinargs
%patch21 -p1 -b .cve-2010-3846
%patch22 -p1 -b .undefined_date
%patch23 -p1 -b .sanity
%patch24 -p1 -b .verbose_sanity
%patch26 -p1 -b .keywordexpand
%patch27 -p1 -b .krb_no_hostname
%patch28 -p1 -b .proxy_response_parser
%patch31 -p1 -b .format

# Apply a patch to the generated files, OR
# run autoreconf and require autoconf >= 2.58, automake >= 1.7.9
for F in FAQ; do
    iconv -f ISO-8859-1 -t UTF-8 < "$F" > "${F}.UTF8"
    touch -r "$F"{,.UTF8}
    mv "$F"{.UTF8,}
done

%build
#use MAKEINFO=true skip info build
autoreconf --install

%configure CFLAGS="$CFLAGS $RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE" 

make %{?_smp_mflags} MAKEINFO=true

%check
if [ $(id -u) -ne 0 ] ; then
	make check MAKEINFO=true
fi

%install
make install DESTDIR="$RPM_BUILD_ROOT" INSTALL="install -p" MAKEINFO=true

rm -rf $RPM_BUILD_ROOT/%{_infodir}
#we only ship cvs binary to end user.
#cvs was dead.
rm -rf %{buildroot}%{_bindir}/rcs2log
rm -rf %{buildroot}%{_datadir}/cvs/


install -D -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/cvs.sh
install -D -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_mandir}/man5/cvs.sh.5


%files
%{_bindir}/cvs*
%{_mandir}/*/*
%config(noreplace) %{_sysconfdir}/profile.d/*
#contrib files.
#%{_bindir}/rcs2log
#%{_datadir}/cvs/

%changelog
