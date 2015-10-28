Name: fonts-Tibetan
Version:    1.901
Release:    2 
Summary:    Tibetan Machine Uni font for Tibetan, Dzongkha and Ladakhi
License:    GPLv3+ with exceptions
URL:        http://www.thlib.org/tools/#wiki=/access/wiki/site/26a34146-33a6-48ce-001e-f16ce7908a6a/tibetan%20machine%20uni.html
Source0:    https://collab.itc.virginia.edu/access/content/group/26a34146-33a6-48ce-001e-f16ce7908a6a/Tibetan%20fonts/Tibetan%20Unicode%20Fonts/TibetanMachineUnicodeFont.zip

Requires: fontconfig 

BuildArch: noarch

%description
Tibetan Machine Uni is an TrueType OpenType, Unicode font released by THDL
project. The font supports Tibetan, Dzongkha and Ladakhi in dbu-can script
with full support for the Sanskrit combinations found in chos skad text.

%prep
%setup -q -c 

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts
install -m 0644 -p */*.ttf $RPM_BUILD_ROOT%{_datadir}/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/fonts/*.ttf

%changelog
* Sat Oct 24 2015 builder - 1.901-2
- Rebuild for new 4.0 release.

