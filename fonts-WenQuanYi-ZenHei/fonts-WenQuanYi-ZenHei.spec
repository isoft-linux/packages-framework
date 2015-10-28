Name:    fonts-WenQuanYi-ZenHei
Version: 0.9.45
Release: 2
Summary: Wen Quan Yi Zen Hei TrueType fonts 
License: GPL
URL:     http://wenq.org 
Source0: wqy-zenhei-%{version}.tar.gz
Patch0:  wqy-zenhei-fix-fontconfig-warning.patch
Provides: wqy-zenhei-fonts = %{version}

BuildArch: noarch

%description
Wen Quan Yi Zen Hei TrueType fonts

%prep
%setup -q -n wqy-zenhei 
%patch0 -p1

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/
install -m 644 *.ttc $RPM_BUILD_ROOT/%{_datadir}/fonts/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 43-wqy-zenhei-sharp.conf $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 44-wqy-zenhei.conf $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
#pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
#ln -sf %{_datadir}/fontconfig/conf.avail/44-wqy-zenhei.conf .
#ln -sf %{_datadir}/fontconfig/conf.avail/43-wqy-zenhei-sharp.conf .
#popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
#%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttc

%changelog
* Sat Oct 24 2015 builder - 0.9.45-2
- Rebuild for new 4.0 release.

