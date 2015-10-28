Name:           fonts-Arphic-Uming
Version:        0.2.20080216.1
Release:        2 
Summary:        Chinese Unicode TrueType font in Ming face
License:        Arphic
URL:            http://www.freedesktop.org/wiki/Software/CJKUnifonts
Source0:        http://ftp.debian.org/debian/pool/main/t/ttf-arphic-uming/ttf-arphic-uming_%{version}.orig.tar.gz

BuildArch: noarch

%description
CJK Unifonts in Ming face.

%prep
%setup -q -c 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/
install -m 644 uming.ttc $RPM_BUILD_ROOT/%{_datadir}/fonts/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/fonts/*.ttc

%changelog
* Sat Oct 24 2015 builder - 0.2.20080216.1-2
- Rebuild for new 4.0 release.

