Summary: Tool for decoding raw image data from digital cameras
Name: dcraw
Version: 9.25.0
Release: 3%{?dist}
Group: Applications/Multimedia
License: GPLv2+
URL: http://cybercom.net/~dcoffin/dcraw
Source0: http://cybercom.net/~dcoffin/dcraw/archive/dcraw-%{version}.tar.gz
Patch0: dcraw-9.25.0-CVE-2013-1438.patch
Patch1: dcraw-9.21-lcms2-error-reporting.patch
Patch2: dcraw-9.25.0-CVE-2015-3885.patch
BuildRequires: gettext
BuildRequires: libjpeg-devel
BuildRequires: lcms2-devel
BuildRequires: jasper-devel
Provides: bundled(dcraw)

%description
This package contains dcraw, a command line tool to decode raw image data
downloaded from digital cameras.

%prep
%setup -q -n dcraw
%patch0 -p1 -b .CVE-2013-1438
%patch1 -p1 -b .lcms2-error-reporting
%patch2 -p1 -b .CVE-2015-3885

%build
gcc %optflags \
    -lm -ljpeg -llcms2 -ljasper \
    -DLOCALEDIR="\"%{_datadir}/locale\"" \
    -o dcraw dcraw.c
# build language catalogs
for catsrc in dcraw_*.po; do
    lang="${catsrc%.po}"
    lang="${lang#dcraw_}"
    msgfmt -o "dcraw_${lang}.mo" "$catsrc"
done

%install
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 dcraw %{buildroot}%{_bindir}

# install language catalogs
for catalog in dcraw_*.mo; do
    lang="${catalog%.mo}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES"
    install -m 0644 "$catalog" "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/dcraw.mo"
done

install -d -m 0755 %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
install -m 0644 dcraw.1 %{buildroot}%{_mandir}/man1/dcraw.1
# localized manpages
rm -f %{name}-man-files
touch %{name}-man-files
for manpage in dcraw_*.1; do
    lang="${manpage%.1}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_mandir}/${lang}/man1"
    install -m 0644 "${manpage}" "%{buildroot}%{_mandir}/${lang}/man1/dcraw.1"
    echo "%%lang($lang) %%{_mandir}/${lang}/man1/*" >> %{name}-man-files
done

%find_lang %{name}

%files -f %{name}.lang -f %{name}-man-files
%defattr(-, root, root)
%{_bindir}/dcraw
%{_mandir}/man1/*

%changelog
