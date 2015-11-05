%global fontname lato
%global fontconf 61-%{fontname}.conf

Name:           fonts-lato
Version:        2.015
Release:        2%{?dist}
Summary:        A sanserif typeface family

License:        OFL
URL:            http://www.latofonts.com/
# Fonts retrieved 2015-08-07 from http://www.latofonts.com/download/Lato2OFL.zip
Source0:        lato-fonts-%{version}.zip
Source1:        61-lato.conf

BuildArch:      noarch
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem
Provides:       google-lato-fonts = %{version}-%{release}
Obsoletes:      google-lato-fonts < 1.014-1

%description
Lato is a sanserif typeface family designed in the Summer 2010 by Warsaw-based
designer Łukasz Dziedzic ("Lato" means "Summer" in Polish). In December 2010 the
Lato family was published under the open-source Open Font License by his foundry
tyPoland, with support from Google.

When working on Lato, Łukasz tried to carefully balance some potentially
conflicting priorities. He wanted to create a typeface that would seem quite
"transparent" when used in body text but would display some original treats when
used in larger sizes. He used classical proportions (particularly visible in the
uppercase) to give the letterforms familiar harmony and elegance. At the same
time, he created a sleek sanserif look, which makes evident the fact that Lato
was designed in 2010 - even though it does not follow any current trend.

The semi-rounded details of the letters give Lato a feeling of warmth, while the
strong structure provides stability and seriousness. "Male and female, serious
but friendly. With the feeling of the Summer," says Łukasz.

Lato consists of nine weights (plus corresponding italics), including a
beautiful hairline style. It covers 2300+ glyphs per style and supports 100+
Latin-based languages, 50+ Cyrillic-based languages as well as Greek and IPA
phonetics.


%prep
%setup -q -c

# Fix wrong end-of-lines encoding
sed "s/\r//" Lato2OFL/OFL.txt > Lato2OFL/OFL.txt.new
touch -r Lato2OFL/OFL.txt Lato2OFL/OFL.txt.new
mv Lato2OFL/OFL.txt.new Lato2OFL/OFL.txt

# Fix permissions
chmod 0644 Lato2OFL/{OFL.txt,README.txt}


%build


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/

install -m 0644 -p Lato2OFL/*.ttf $RPM_BUILD_ROOT%{_datadir}/fonts/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/61-lato.conf .
popd

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttf

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 2.015-2
- Initial build

