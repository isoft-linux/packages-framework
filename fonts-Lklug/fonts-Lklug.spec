Name:    fonts-Lklug
Version: 0.6
Release: 1
License: GPL
Source0:  lklug-20090803.tar.gz
Source1:  lklug.ttf
Summary: Unicode Sinhala font by Lanka Linux User Group
URL:    http://sinhala.sourceforge.net/
%description
Unicode Sinhala font by Lanka Linux User Group
%prep
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/fonts/*.ttf

