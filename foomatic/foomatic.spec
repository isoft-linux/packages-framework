Summary: Tools for using the foomatic database of printers and printer drivers
Name:       foomatic
Version:    4.0.12
Release:    5%{?dist}
License:    GPLv2+

# printer-filters package has gone (bug #967316, bug #1035450).
Obsoletes: printer-filters < 1.1-8
Provides: printer-filters = 1.1-8

# The database engine.
Source0: http://www.openprinting.org/download/foomatic/foomatic-db-engine-%{version}.tar.gz

## PATCHES FOR FOOMATIC-DB-ENGINE (PATCHES 101 TO 200)
Patch101:       foomatic-manpages.patch

## PATCHES FOR FOOMATIC-DB-HPIJS (PATCHES 201 TO 300)

Url:            http://www.linuxfoundation.org/collaborate/workgroups/openprinting/database/foomatic
BuildRequires:  perl >= 3:5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  libxml2-devel
BuildRequires:  autoconf, automake
BuildRequires:  cups-devel
BuildRequires:  dbus-devel
Requires:       dbus
Requires:       cups-filters >= 1.0.42
Requires:       perl >= 3:5.8.1
Requires:       %(eval `perl -V:version`; echo "perl(:MODULE_COMPAT_$version)")

# Make sure we get postscriptdriver tags.  Safe to comment out when
# bootstrapping a new architecture.
BuildRequires: python-cups, cups
%if 0%{!?perl_bootstrap:1}
BuildRequires: foomatic, foomatic-db
%endif

Requires: foomatic-db
Requires: cups
Requires: ghostscript
Requires: colord

%description
Foomatic is a comprehensive, spooler-independent database of printers,
printer drivers, and driver descriptions. This package contains
utilities to generate driver description files and printer queues for
CUPS, LPD, LPRng, and PDQ using the database (packaged separately).
There is also the possibility to read the PJL options out of PJL-capable
laser printers and take them into account at the driver description
file generation.

There are spooler-independent command line interfaces to manipulate
queues (foomatic-configure) and to print files/manipulate jobs
(foomatic printjob).

The site http://www.linuxprinting.org/ is based on this database.

%prep
%setup -q -n foomatic-db-engine-%{version}

# Ship more manpages.
%patch101 -p1 -b .manpages

chmod a+x mkinstalldirs

%build
export LIB_CUPS=%{_cups_serverbin}
export CUPS_BACKENDS=%{_cups_serverbin}/backend
export CUPS_FILTERS=%{_cups_serverbin}/filter
export CUPS_PPDS=%{_datadir}/cups/model

aclocal
autoconf
%configure --disable-xmltest
make PREFIX=%{_prefix} CFLAGS="$RPM_OPT_FLAGS"

%install
make    DESTDIR=%buildroot PREFIX=%{_prefix} \
        INSTALLSITELIB=%{perl_vendorlib} \
        INSTALLSITEARCH=%{perl_vendorarch} \
        install

# Use relative, not absolute, symlink for CUPS driver.
ln -sf ../../../bin/foomatic-ppdfile %{buildroot}%{_cups_serverbin}/driver/foomatic

mkdir -p %{buildroot}%{_var}/cache/foomatic

echo cups > %{buildroot}%{_sysconfdir}/foomatic/defaultspooler

# Remove things we don't ship.
rm -rf  \
        %{buildroot}%{_libdir}/ppr \
        %{buildroot}%{_sysconfdir}/foomatic/filter.conf.sample \
        %{buildroot}%{_datadir}/foomatic/templates
#%{buildroot}%%{_libdir}/perl5/site_perl
find %{buildroot} -name .packlist | xargs rm -f

%post
/bin/rm -rf /var/cache/foomatic/* ||:
exit 0


%files
%doc COPYING
%dir %{_sysconfdir}/foomatic
%config(noreplace) %{_sysconfdir}/foomatic/defaultspooler
%{_bindir}/foomatic-combo-xml
%{_bindir}/foomatic-compiledb
%{_bindir}/foomatic-configure
%{_bindir}/foomatic-datafile
%{_bindir}/foomatic-perl-data
%{_bindir}/foomatic-ppd-options
%{_bindir}/foomatic-ppd-to-xml
%{_bindir}/foomatic-ppdfile
%{_bindir}/foomatic-printjob
%{_bindir}/foomatic-searchprinter
%{_sbindir}/*
%{perl_vendorlib}/Foomatic
%{_cups_serverbin}/driver/*
%{_mandir}/man1/foomatic-cleanupdrivers.1*
%{_mandir}/man1/foomatic-combo-xml.1*
%{_mandir}/man1/foomatic-compiledb.1*
%{_mandir}/man1/foomatic-configure.1*
%{_mandir}/man1/foomatic-datafile.1*
%{_mandir}/man1/foomatic-extract-text.1*
%{_mandir}/man1/foomatic-fix-xml.1*
%{_mandir}/man1/foomatic-nonumericalids.1*
%{_mandir}/man1/foomatic-perl-data.1*
%{_mandir}/man1/foomatic-ppd-options.1*
%{_mandir}/man1/foomatic-ppd-to-xml.1*
%{_mandir}/man1/foomatic-ppdfile.1*
%{_mandir}/man1/foomatic-printermap-to-gutenprint-xml.1*
%{_mandir}/man1/foomatic-printjob.1*
%{_mandir}/man1/foomatic-replaceoldprinterids.1*
%{_mandir}/man1/foomatic-searchprinter.1*
%{_mandir}/man8/*
%{_var}/cache/foomatic

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.0.12-5
- Rebuild for new 4.0 release.

