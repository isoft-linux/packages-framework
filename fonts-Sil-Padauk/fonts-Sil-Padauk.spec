Name:       fonts-Sil-Padauk
Version:    2.8
Release:    2 
Summary:    A font for Burmese and the Myanmar script
License:    OFL
URL:        http://scripts.sil.org/Padauk
Source0:    padauk-2.8.zip

BuildArch: noarch

%description
Padauk is a Myanmar font covering all currently used characters
in the Myanmar block. The font aims to cover all minority language needs.
At the moment, these do not extend to stylistic variation needs.
The font is a smart font using a Graphite description.

%prep
%setup -q -n padauk-2.80

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
* Sat Oct 24 2015 builder - 2.8-2
- Rebuild for new 4.0 release.

