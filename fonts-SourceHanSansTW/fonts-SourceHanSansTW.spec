Name:          fonts-SourceHanSansTW
Summary:       Adobe OpenType Pan-CJK font family for Traditional Chinese
Version:       1.002 
Release:       1
License:       GPL 
URL:            https://github.com/adobe-fonts/source-han-sans/
Source0:        https://github.com/adobe-fonts/source-han-sans/raw/release/SubsetOTF/SourceHanSansTW.zip
Source1:        65-0-adobe-source-han-sans-tw.conf
%description
Adobe OpenType Pan-CJK font family for Traditional Chinese

%prep
%setup -n SourceHanSansTW

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/fonts
install -m 0644 *.otf $RPM_BUILD_ROOT/%{_datadir}/fonts


mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/65-0-adobe-source-han-sans-tw.conf .
popd


%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.otf
