Name:            unifont
Version:         7.0.06
Release:         3
License:         GPLv2+ and GFDL
Url:             https://savannah.gnu.org/projects/unifont
Summary:         Tools and glyph descriptions in a very simple text format

Source0:         http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:         unifont.metainfo.xml

BuildRequires:   xorg-x11-font-utils
#BuildRequires:   fontforge
BuildRequires:   fontpackages-devel

%description
A font with a glyph for every visible Unicode Basic Multilingual Plane
code point and more, with supporting utilities to modify the
font. This package contains tools and glyph descriptions.

%package fonts
BuildArch: noarch
Summary: Unicode font with a glyph for every visible BMP code point

Requires:        fontpackages-filesystem

%description fonts
A fixed-width Unicode font with a glyph for every visible Unicode 7.0
Basic Multilingual Plane code point and more. The latest version of
Unifont includes approximately 54,700 glyphs for all the visible
Unicode BMP code points.

This font strives for very wide coverage rather than beauty, so use it
only as fallback or for special purposes.

%package viewer
BuildArch: noarch
Summary: Graphical viewer for unifont

%description viewer
A graphical viewer for unifont.

%prep
%setup -q
# Disable rebuilding during installation
sed -i 's/^install: .*/install:/' Makefile
sed -i 's/install -s/install/' src/Makefile

%build
# Makefile is broken with parallel builds
make CFLAGS='%{optflags}'
make -C doc unifont.info

%install
%make_install USRDIR=/usr COMPRESS=0 TTFDEST='$(DESTDIR)/usr/share/fonts/unifont'
find %{buildroot}/usr/share/unifont/ -type f \! -name %{name}.hex -delete
rm -rv %{buildroot}/usr/share/fonts/X11
rm -v %{buildroot}%{_fontdir}/*sample*
rm -v %{buildroot}%{_fontdir}/unifont_*csur*.ttf
install -Dm0644 doc/unifont.info %{buildroot}%{_infodir}/unifont.info
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/appdata/unifont.metainfo.xml
# Remove APL font for now
rm %{buildroot}/usr/share/consolefonts/Unifont-APL8x16.psf.gz

%files
%{_bindir}/*
%{_datadir}/%{name}/
%doc NEWS README
%license COPYING
%{_mandir}/man1/*
%{_mandir}/man5/*
%exclude %{_bindir}/unifont-viewer
%exclude %{_bindir}/unihex2png
%exclude %{_bindir}/unipng2hex

%_font_pkg *.ttf
%{_datadir}/appdata/
%license COPYING

#%files viewer
#%{_bindir}/unifont-viewer
#%license COPYING

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 7.0.06-3
- Rebuild for new 4.0 release.

