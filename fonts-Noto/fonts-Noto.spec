Name:    fonts-Noto
Version: 20151115
Release: 2 
Summary: Google Noto TrueType fonts
License: OFL 
URL: https://www.google.com/get/noto
#Fonts download from here: https://noto-website-2.storage.googleapis.com/pkgs/Noto-hinted.zip
#We use Adobe SourceHanSans as default fonts and the zip archive is too large, 
#so we strip all otf(CJK) fonts and make a small tarball.
Source0: Noto-hinted.tar.gz 

BuildArch: noarch

%description
Google Noto TrueType fonts

%prep
%setup -q -c 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/
install -m 644 *.ttf $RPM_BUILD_ROOT/%{_datadir}/fonts/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/fonts/*

%changelog
* Sun Nov 15 2015 Cjacker <cjacker@foxmail.com> - 20151115-2
- Update

* Sat Oct 24 2015 builder - 20150630-2
- Rebuild for new 4.0 release.

