Summary: OpenPrinting CUPS filters and backends
Name:    cups-filters
Version: 1.0.71
Release: 3%{?dist}

# For a breakdown of the licensing, see COPYING file
# GPLv2:   filters: commandto*, imagetoraster, pdftops, rasterto*,
#                   imagetopdf, pstopdf, texttopdf
#         backends: parallel, serial
# GPLv2+:  filters: gstopxl, textonly, texttops, imagetops, foomatic-rip
# GPLv3:   filters: bannertopdf
# GPLv3+:  filters: urftopdf, rastertopdf
# LGPLv2+:   utils: cups-browsed
# MIT:     filters: gstoraster, pdftoijs, pdftoopvp, pdftopdf, pdftoraster
License: GPLv2 and GPLv2+ and GPLv3 and GPLv3+ and LGPLv2+ and MIT

Url:     http://www.linuxfoundation.org/collaborate/workgroups/openprinting/cups-filters
Source0: http://www.openprinting.org/download/cups-filters/cups-filters-%{version}.tar.xz
# Upstream patch for poppler 0.34 support
# http://bzr.linuxfoundation.org/loggerhead/openprinting/cups-filters/revision/7371
Patch0:  cups-filters-poppler34.patch

Requires: cups-filters-libs%{?_isa} = %{version}-%{release}

# Obsolete cups-php (bug #971741)
Obsoletes: cups-php < 1:1.6.0-1
# Don't Provide it because we don't build the php module
#Provides: cups-php = 1:1.6.0-1

BuildRequires: cups-devel
BuildRequires: pkgconfig
# pdftopdf
BuildRequires: pkgconfig(libqpdf)
# pdftops
BuildRequires: poppler-utils
# pdftoijs, pdftoopvp, pdftoraster, gstoraster
BuildRequires: pkgconfig(poppler)
BuildRequires: poppler-cpp-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(dbus-1)
# libijs
BuildRequires: pkgconfig(ijs)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(lcms2)
# cups-browsed
BuildRequires: avahi-devel
BuildRequires: pkgconfig(avahi-glib)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: systemd

# Make sure we get postscriptdriver tags.
BuildRequires: python-cups

# Testing font for test scripts.
BuildRequires: fonts-DejaVu

# autogen.sh
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

Requires: cups-filesystem
Requires: poppler-utils

# texttopdf
Requires: fonts-liberation

# pstopdf
Requires: bc grep sed

# cups-browsed
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# Ghostscript CUPS filters live here since Ghostscript 9.08.
Provides: ghostscript-cups = 9.08
Obsoletes: ghostscript-cups < 9.08

# foomatic-rip's upstream moved from foomatic-filters to cups-filters-1.0.42
Provides: foomatic-filters = 4.0.9-8
Obsoletes: foomatic-filters < 4.0.9-8

%package libs
Summary: OpenPrinting CUPS filters and backends - cupsfilters and fontembed libraries
Group:   System Environment/Libraries
# LGPLv2: libcupsfilters
# MIT:    libfontembed
License: LGPLv2 and MIT

%package devel
Summary: OpenPrinting CUPS filters and backends - development environment
Group:   Development/Libraries
License: LGPLv2 and MIT
Requires: cups-filters-libs%{?_isa} = %{version}-%{release}

%description
Contains backends, filters, and other software that was
once part of the core CUPS distribution but is no longer maintained by
Apple Inc. In addition it contains additional filters developed
independently of Apple, especially filters for the PDF-centric printing
workflow introduced by OpenPrinting.

%description libs
This package provides cupsfilters and fontembed libraries.

%description devel
This is the development package for OpenPrinting CUPS filters and backends.

%prep
%setup -q
%patch0 -p0 -b .poppler34

%build
# work-around Rpath
./autogen.sh

# --with-pdftops=hybrid - use Poppler's pdftops instead of Ghostscript for
#                         Brother, Minolta, and Konica Minolta to work around
#                         bugs in the printer's PS interpreters
# --with-rcdir=no - don't install SysV init script
%configure --disable-static \
           --disable-silent-rules \
           --with-pdftops=hybrid \
           --enable-dbus \
           --with-rcdir=no \
	   --with-test-font-path="/usr/share/fonts/DejaVuSans.ttf"

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Don't ship libtool la files.
rm -f %{buildroot}%{_libdir}/lib*.la

# Not sure what is this good for.
rm -f %{buildroot}%{_bindir}/ttfread

rm -f %{buildroot}%{_defaultdocdir}/cups-filters/INSTALL
mkdir -p %{buildroot}%{_defaultdocdir}/cups-filters/fontembed/
cp -p fontembed/README %{buildroot}%{_defaultdocdir}/cups-filters/fontembed/

# systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 utils/cups-browsed.service %{buildroot}%{_unitdir}

# LSB3.2 requires /usr/bin/foomatic-rip,
# create it temporarily as a relative symlink
ln -sf ../lib/cups/filter/foomatic-rip %{buildroot}%{_bindir}/foomatic-rip

# Don't ship urftopdf for now (bug #1002947).
rm -f %{buildroot}%{_cups_serverbin}/filter/urftopdf
sed -i '/urftopdf/d' %{buildroot}%{_datadir}/cups/mime/cupsfilters.convs

# Don't ship pdftoopvp for now (bug #1027557).
rm -f %{buildroot}%{_cups_serverbin}/filter/pdftoopvp
rm -f %{buildroot}%{_sysconfdir}/fonts/conf.d/99pdftoopvp.conf


%check
make check

%post
%systemd_post cups-browsed.service

# Initial installation
if [ $1 -eq 1 ] ; then
    IN=%{_sysconfdir}/cups/cupsd.conf
    OUT=%{_sysconfdir}/cups/cups-browsed.conf
    keyword=BrowsePoll

    # We can remove this after few releases, it's just for the introduction of cups-browsed.
    if [ -f "$OUT" ]; then
        echo -e "\n# NOTE: This file is not part of CUPS.\n# You need to enable cups-browsed service\n# and allow ipp-client service in firewall." >> "$OUT"
    fi

    # move BrowsePoll from cupsd.conf to cups-browsed.conf
    if [ -f "$IN" ] && grep -iq ^$keyword "$IN"; then
        if ! grep -iq ^$keyword "$OUT"; then
            (cat >> "$OUT" <<EOF

# Settings automatically moved from cupsd.conf by RPM package:
EOF
            ) || :
            (grep -i ^$keyword "$IN" >> "$OUT") || :
            #systemctl enable cups-browsed.service >/dev/null 2>&1 || :
        fi
        sed -i -e "s,^$keyword,#$keyword directive moved to cups-browsed.conf\n#$keyword,i" "$IN" || :
    fi
fi

%preun
%systemd_preun cups-browsed.service

%postun
%systemd_postun_with_restart cups-browsed.service 

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%{_defaultdocdir}/cups-filters/README
%{_defaultdocdir}/cups-filters/AUTHORS
%{_defaultdocdir}/cups-filters/NEWS
%config(noreplace) %{_sysconfdir}/cups/cups-browsed.conf
%attr(0755,root,root) %{_cups_serverbin}/filter/*
%attr(0755,root,root) %{_cups_serverbin}/backend/parallel
# Serial backend needs to run as root (bug #212577#c4).
%attr(0700,root,root) %{_cups_serverbin}/backend/serial
%{_datadir}/cups/banners
%{_datadir}/cups/charsets
%{_datadir}/cups/data/*
# this needs to be in the main package because of cupsfilters.drv
%{_datadir}/cups/ppdc/pcl.h
%{_datadir}/cups/drv/cupsfilters.drv
%{_datadir}/cups/mime/cupsfilters.types
%{_datadir}/cups/mime/cupsfilters.convs
%{_datadir}/ppd/cupsfilters
%{_sbindir}/cups-browsed
%{_unitdir}/cups-browsed.service
%{_mandir}/man8/cups-browsed.8.gz
%{_mandir}/man5/cups-browsed.conf.5.gz
%{_mandir}/man1/foomatic-rip.1.gz
%{_bindir}/foomatic-rip

%files libs
%dir %{_defaultdocdir}/cups-filters/
%{_defaultdocdir}/cups-filters/COPYING
%{_defaultdocdir}/cups-filters/fontembed/README
%{_libdir}/libcupsfilters.so.*
%{_libdir}/libfontembed.so.*

%files devel
%{_includedir}/cupsfilters
%{_includedir}/fontembed
%{_datadir}/cups/ppdc/escp.h
%{_libdir}/pkgconfig/libcupsfilters.pc
%{_libdir}/pkgconfig/libfontembed.pc
%{_libdir}/libcupsfilters.so
%{_libdir}/libfontembed.so

%changelog
