Name:    fonts-Sazanami
Version: 20040629 
Release: 3 
Summary: Sazanami Janpanese TrueType fonts
License: BSD 

URL:     http://efont.sourceforge.jp/
Source0: http://globalbase.dl.sourceforge.jp/efont/10087/sazanami-20040629.tar.bz2
Source1: 65-4-sazanami-gothic.conf  
Source2: 65-4-sazanami-mincho.conf

Source10: sazanami-gothic.ttf  
Source11: sazanami-mincho.ttf

%description
Sazanami Japanese TrueType fonts

#build these fonts need some external tools, such as fontforge/perl TTF/fonttool and so on.
#we directly provide final TrueType files.
#but keep the source here.

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/
install -m 644 %{SOURCE10} %{SOURCE11} $RPM_BUILD_ROOT/%{_datadir}/fonts/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/65-4-sazanami-gothic.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-4-sazanami-mincho.conf .
popd


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttf
