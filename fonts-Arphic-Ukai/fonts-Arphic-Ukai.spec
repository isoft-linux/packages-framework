Name:           fonts-Arphic-Ukai
Version:        0.2.20080216.1
Release:        1
Summary:        Chinese Unicode TrueType font in Kai face

Group:          User Interface/X
License:        Arphic
URL:            http://www.freedesktop.org/wiki/Software/CJKUnifonts
Source0:        http://ftp.debian.org/debian/pool/main/t/ttf-arphic-ukai/ttf-arphic-ukai_%{version}.orig.tar.gz


%description
Chinese Unicode TrueType font in Kai face

%prep
%setup -q -c

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/
install -m 644 *.ttc $RPM_BUILD_ROOT/%{_datadir}/fonts/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/fonts/*.ttc
