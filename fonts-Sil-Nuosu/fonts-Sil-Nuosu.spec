Name:       fonts-Sil-Nuosu
Version:    1.200
Release:    2 
Summary:    Unicode font for Yi (a script used in southwestern China)
License:    OFL 
Source0:    NuosuSIL2.1.1.zip

BuildArch: noarch

%description
The Nuosu SIL Font is a single Unicode font for the standardized Yi script
used by a large ethnic group in southwestern China.
Until this version, the font was called SIL Yi.


%prep
%setup -q -n NuosuSIL 

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts
install -m 0644 *.ttf $RPM_BUILD_ROOT%{_datadir}/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/fonts/*.ttf


%changelog
* Sat Oct 24 2015 builder - 1.200-2
- Rebuild for new 4.0 release.

