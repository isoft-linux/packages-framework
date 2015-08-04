Summary: Adwaita icon theme
Name: adwaita-icon-theme
Version: 3.16.2.1
Release: 2 
Source0: %{name}-%{version}.tar.xz
License: GPL
BuildArch: noarch
Group: User Interface/Desktops
BuildRoot: %{_tmppath}/%{name}-root
#BuildRequires: icon-naming-utils >= 0.7.2
#BuildRequires: perl-XML-Parser
BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: icon-naming-utils
BuildRequires: /usr/bin/gtk3-update-icon-cache
BuildRequires: librsvg2
Requires(pre): gtk3
Requires(pre): hicolor-icon-theme
%description
Contains the base icons needed by the Gnome desktop environment.

%prep
%setup -q
%build
export GTK_UPDATE_ICON_CACHE=/usr/bin/gtk3-update-icon-cache 
%configure --disable-hicolor-check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT DATADIRNAME=share

%clean
rm -rf $RPM_BUILD_ROOT

%post 
for dir in /usr/share/icons/*; do 
  if test -d "$dir"; then
    if test -f "$dir/index.theme"; then
      /usr/bin/gtk3-update-icon-cache --quiet "$dir" 
    fi
  fi
done

%files
%defattr(-,root,root)
%{_datadir}/icons/Adwaita
%{_datadir}/pkgconfig/adwaita-icon-theme.pc

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

