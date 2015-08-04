Name:       fonts-VLGothic
Summary:    VL Gothic Japanese fonts
Version:    20141206 
Release:    1
License:    mplus and BSD
Source0:    http://osdn.dl.sourceforge.jp/vlgothic/62375/VLGothic-20141206.tar.bz2
Source1:    65-0-vlgothic-pgothic.conf  
Source2:    65-1-vlgothic-gothic.conf
%description
VL Gothic Japanese fonts
%prep
%setup -n VLGothic 
%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/fonts
install -m 0644 *.ttf $RPM_BUILD_ROOT/%{_datadir}/fonts

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-vlgothic-pgothic.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-1-vlgothic-gothic.conf .
popd


%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttf
