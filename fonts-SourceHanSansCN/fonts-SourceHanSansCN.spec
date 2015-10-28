Name:          fonts-SourceHanSansCN
Summary:       Adobe OpenType Pan-CJK font family for Simplified Chinese
Version:       1.002 
Release:       2
License:       GPL 
URL:            https://github.com/adobe-fonts/source-han-sans/
Source0:        https://github.com/adobe-fonts/source-han-sans/raw/release/SubsetOTF/SourceHanSansCN.zip
Source1:        65-0-adobe-source-han-sans-cn.conf

BuildArch: noarch

%description
Adobe OpenType Pan-CJK font family for Simplified Chinese

%prep
%setup -n SourceHanSansCN

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/fonts
install -m 0644 *.otf $RPM_BUILD_ROOT/%{_datadir}/fonts


mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-adobe-source-han-sans-cn.conf .
popd


%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.otf

%changelog
* Sat Oct 24 2015 builder - 1.002-2
- Rebuild for new 4.0 release.

