Name:       fonts-Arundina
Version:    0.2.0
Release:    1 
Summary:    Variable-width sans-serif Thai Arundina fonts
License:    Bitstream Vera
URL:        http://linux.thai.net/projects/thaifonts-arundina
Source0:    thai-arundina.tar.gz
Source1:    67-thai-arundina-sans.conf       
Source2:    67-thai-arundina-sans-mono.conf  
Source3:    67-thai-arundina-serif.conf
 
%description
Arundina fonts were created aiming at Bitstream Vera / Dejavu
compatibility, under SIPA's initiation.  They were then further
modified by TLWG for certain aspects, such as Latin glyph size
compatibility and OpenType conformance.

This package consists of the Thai Arundina sans-serif variable-width
font faces.

%prep
%setup -q -n thai-arundina

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts
cp *.ttf $RPM_BUILD_ROOT%{_datadir}/fonts

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/67-thai-arundina-sans.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/67-thai-arundina-sans-mono.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/67-thai-arundina-serif.conf .
popd


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttf
