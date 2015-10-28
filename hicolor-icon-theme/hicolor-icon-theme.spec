Summary: Basic requirement for icon themes
Name: hicolor-icon-theme
Version: 0.15
Release: 5
License: GPL+
URL: http://freedesktop.org/Software/icon-theme
Source: http://icon-theme.freedesktop.org/releases/%{name}-%{version}.tar.xz
BuildArch: noarch
Requires(post): coreutils
Requires(postun): coreutils

%description
Contains the basic directories and files needed for icon theme support.

%prep
%setup -q

# for some reason this file is executable in the tarball
chmod 0644 COPYING

%build
%configure

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

touch $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk3-update-icon-cache ]; then
  gtk3-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi
exit 0

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk3-update-icon-cache ]; then
  gtk3-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING
%{_datadir}/icons/hicolor
%ghost %{_datadir}/icons/hicolor/icon-theme.cache

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.15-5
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

