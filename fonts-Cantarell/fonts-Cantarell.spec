Name:           fonts-Cantarell
Version:        0.0.17.2
Release:        2 
Summary:        Gnome cantarell font
License:        GPL
Source:	        cantarell-fonts-%{version}.tar.xz
Provides:       abattis-cantarell-fonts

BuildArch: noarch

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*.conf
%{_datadir}/fonts/*.otf

%changelog
* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 0.0.17.2-2
- Update

* Sat Oct 24 2015 builder - 0.0.17.2-4
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 0.0.17.2
