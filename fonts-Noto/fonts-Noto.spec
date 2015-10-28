Name:    fonts-Noto
Version: 20150630 
Release: 2
Summary: Google Noto TrueType fonts
License: Apache 
URL:     https://github.com/googlei18n/noto-fonts
Source0: noto-fonts-2015-06-30.tar.gz 

BuildArch: noarch

%description
Google Noto TrueType fonts

%prep
%setup -q -n noto-fonts-2015-06-30

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/
install -m 644 hinted/*.ttf $RPM_BUILD_ROOT/%{_datadir}/fonts/
install -m 644 hinted/*.ttc $RPM_BUILD_ROOT/%{_datadir}/fonts/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/fonts/*

%changelog
* Sat Oct 24 2015 builder - 20150630-2
- Rebuild for new 4.0 release.

