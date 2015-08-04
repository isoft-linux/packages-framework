Name:    fonts-liberation
Version: 1.07.4
Release: 3 
Summary: Liberation TrueType fonts
License: GPL
URL:     https://fedorahosted.org/liberation-fonts/
Source0: https://fedorahosted.org/releases/l/i/liberation-fonts/liberation-fonts-ttf-1.07.4.tar.gz

Source2: liberation-fonts-mono.conf
Source3: liberation-fonts-sans.conf
Source4: liberation-fonts-serif.conf
Source5: liberation-fonts-narrow.conf

Provides: liberation-fonts = %{version}

%description
Liberation TrueType fonts

%prep
%setup -q -n liberation-fonts-ttf-%{version}

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/
install -m 644 *.ttf $RPM_BUILD_ROOT/%{_datadir}/fonts/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/liberation-fonts-mono.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/liberation-fonts-sans.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/liberation-fonts-serif.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/liberation-fonts-narrow.conf .
popd


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttf
