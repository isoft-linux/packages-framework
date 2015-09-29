Name:           fonts-Cantarell
Version:        0.0.16
Release:        3 
Summary:        Gnome cantarell font
License:        GPL
Source:	        cantarell-fonts-%{version}.tar.xz
Provides:       abattis-cantarell-fonts

%description
Gnome cantarell TrueType font

%prep
%setup -q -n cantarell-fonts-%{version}
%Build
%configure --with-fontdir=%{buildroot}%{_datadir}/fonts

%install
%makeinstall

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_datadir}/fontconfig/conf.avail/31-cantarell.conf .
popd

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*.conf
%{_datadir}/fonts/*.otf

