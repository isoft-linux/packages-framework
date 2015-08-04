Name: fonts-Ethopic
Version:    4.1 
Release:    1 
Summary:    ethopic fonts
Group:      User Interface/X
License:    OFL 
URL:        http://www.senamirmir.org/projects/typography/typeface.html
Source0:    washra_fonts-4.1.zip 
%description
This file provides detailed information on the WashRa fonts. This information
should be distributed along with the WashRa fonts and any derivative works.

Basic Font Information
+------------------------------+
Ethiopic WashRa SemiBold: Latin-1, Ethiopic
Ethiopic WashRa Bold: Latin-1, Ethiopic
Ethiopia Jiret: Latin-1, Ethiopic
Ethiopic Zelan: Latin-1, Ethiopic
Ethiopic Hiwua: Latin-1, Ethiopic
Ethiopic Wookianos: Latin-1, Ethiopic
Ethiopic Fantuwua: Latin-1, Ethiopic
Ethiopic Tint: Latin-1, Ethiopic
Ethiopic Yebse: Latin-1, Ethiopic
Ethiopic Yigezu Bisrat Goffer: Latin-1, Ethiopic
Ethiopic Yigezu Bisrat Gothic: Latin-1, Ethiopic


%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts
cp *.ttf $RPM_BUILD_ROOT%{_datadir}/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/fonts/*.ttf

