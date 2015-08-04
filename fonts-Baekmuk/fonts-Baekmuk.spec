Name:       fonts-Baekmuk
Version:    2.2
Release:    1 
Summary:    Free Korean TrueType fonts
License:    Baekmuk
URL:        http://kldp.net/projects/baekmuk/
Source0:    http://kldp.net/frs/download.php/1429/baekmuk-ttf-%{version}.tar.gz

Source1:    65-2-baekmuk-ttf-batang.conf  
Source2:    65-2-baekmuk-ttf-dotum.conf   
Source3:    65-2-baekmuk-ttf-gulim.conf   
Source4:    65-2-baekmuk-ttf-hline.conf 

%description
This package provides the free Korean TrueType fonts.
Batang is Korean TrueType font in Serif typeface.
Dotum is Korean TrueType font in Sans typeface.

%prep
%setup -n baekmuk-ttf-%{version} 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts
install -m 0644 ttf/*.ttf $RPM_BUILD_ROOT%{_datadir}/fonts

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/65-2-baekmuk-ttf-batang.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-2-baekmuk-ttf-dotum.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-2-baekmuk-ttf-gulim.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-2-baekmuk-ttf-hline.conf .
popd


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttf


