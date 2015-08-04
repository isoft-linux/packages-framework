Name:    fonts-DejaVu
Version: 2.35
Release: 3 
Summary: DejaVu TrueType fonts
License: GPL
URL:     http://dejavu-fonts.org
Source0: dejavu-fonts-ttf-%{version}.tar.bz2

Source1: 20-unhint-small-dejavu-sans.conf
Source2: 57-dejavu-sans.conf 

Provides: dejavu-sans-fonts = %{version}

%description
DejaVu TrueType fonts

%prep
%setup -q -n dejavu-fonts-ttf-%{version}

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/
install -m 644 ttf/*.ttf $RPM_BUILD_ROOT/%{_datadir}/fonts/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/20-unhint-small-dejavu-sans.conf .
ln -sf %{_datadir}/fontconfig/conf.avail/57-dejavu-sans.conf .
popd


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttf
