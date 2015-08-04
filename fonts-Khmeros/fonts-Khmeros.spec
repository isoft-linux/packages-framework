Name: fonts-Khmeros
Version: 5.0 
Release: 1
License:        LGPLv2+
URL:            http://www.khmeros.info/en/fonts
Source0:        http://downloads.sourceforge.net/khmer/All_KhmerOS_5.0.zip
Source1:        65-0-khmeros-battambang.conf
Source2:        65-0-khmeros-bokor.conf
Source3:        65-0-khmeros-handwritten.conf
Source4:        65-0-khmeros-base.conf
Source5:        65-0-khmeros-metal-chrieng.conf
Source6:        65-0-khmeros-muol.conf
Source7:        65-0-khmeros-siemreap.conf
Summary: Khmer font set created by Danh Hong of the Cambodian Open Institute 

%description
The Khmer OS fonts include Khmer and Latin alphabets, and they have equivalent 
sizes for Khmer and English alphabets, so that when texts mix both it is not 
necessary to have different point sizes for the text in each language. 

They were created by Danh Hong of the Cambodian Open Institute.

%prep
%setup -q -n All_KhmerOS_5.0 

%install
rm -rf $RPM_BUILD_ROOT
mv 'KhmerOS .ttf' KhmerOS.ttf

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts
install -m0644 *.ttf $RPM_BUILD_ROOT%{_datadir}/fonts

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-khmeros-battambang.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-khmeros-bokor.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-khmeros-handwritten.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-khmeros-base.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-khmeros-metal-chrieng.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-khmeros-muol.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-khmeros-siemreap.conf .
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttf

