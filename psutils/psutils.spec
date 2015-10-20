Summary: PostScript Utilities
Name:    psutils
Version: 1.23
Release: 8%{?dist}
License: psutils

# We can't follow https://fedoraproject.org/wiki/Packaging:SourceURL#Github
# and use upstream tarball for building because ./bootstrap downloads gnulib.
# wget https://github.com/rrthomas/psutils/archive/master.zip && unzip master.zip && cd psutils-master/
# ./bootstrap && autoreconf -vfi && ./configure && make dist-xz
Source: psutils-%{version}.tar.xz
URL:    https://github.com/rrthomas/psutils

# BZ#1072371
# https://github.com/rrthomas/psutils/commit/cca570c806bf4bde07f400b2bab9266e02998145
Patch0: psutils-paperconf.patch

BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

Requires: /usr/bin/paperconf

# copylib - https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)

%description
Utilities for manipulating PostScript documents.
Page selection and rearrangement are supported, including arrangement into
signatures for booklet printing, and page merging for n-up printing.

%package perl
Summary: psutils scripts requiring perl
BuildArch: noarch

%description perl
Various scripts from the psutils distribution that require perl.

%prep
%setup -q

%patch0 -p1 -b .paperconf
# Use /usr/bin/perl instead of /usr/bin/env perl
sed -i -e 's,/usr/bin/env perl,%{__perl},' \
  extractres psjoin

%build
%configure
%{__make} %{?_smp_mflags}
 
%install
%{__make} install DESTDIR=%{buildroot}

%files
%doc README LICENSE
%{_bindir}/epsffit
%{_bindir}/psbook
%{_bindir}/psnup
%{_bindir}/psresize
%{_bindir}/psselect
%{_bindir}/pstops
%{_mandir}/man1/epsffit.1*
%{_mandir}/man1/psbook.1*
%{_mandir}/man1/psnup.1*
%{_mandir}/man1/psresize.1*
%{_mandir}/man1/psselect.1*
%{_mandir}/man1/pstops.1*
%{_mandir}/man1/psutils.1*

%files perl
%doc LICENSE
%{_bindir}/extractres
%{_bindir}/includeres
%{_bindir}/psjoin
%{_mandir}/man1/extractres.1*
%{_mandir}/man1/includeres.1*
%{_mandir}/man1/psjoin.1*


%changelog
