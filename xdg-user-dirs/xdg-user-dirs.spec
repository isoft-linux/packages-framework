Name:		xdg-user-dirs
Version:	0.15
Release:	5
Summary:	Handles user special directories

License:	GPLv2+ and MIT
URL:		http://freedesktop.org/wiki/Software/xdg-user-dirs
Source0:	http://user-dirs.freedesktop.org/releases/%{name}-%{version}.tar.gz
#always force to create dirs.
Source1:	xdg-user-dirs.sh
Patch0:		use-fuzzy.patch

BuildRequires:	gettext
Requires:	%{_sysconfdir}/X11/xinit/xinitrc.d

%description
Contains xdg-user-dirs-update that updates folders in a users
homedirectory based on the defaults configured by the administrator.

%prep
%setup -q
%patch0 -p1 -b .use-fuzzy

%build
%configure
make %{?_smp_mflags}

cd po
touch *.po
make update-gmo

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -m 0755 xdg-user-dir-lookup $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d

install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/xdg/user-dirs.conf
%config(noreplace) %{_sysconfdir}/xdg/user-dirs.defaults
%{_sysconfdir}/X11/xinit/xinitrc.d/*
%{_mandir}/man1/xdg-user-dir.1.gz
%{_mandir}/man1/xdg-user-dirs-update.1.gz
%{_mandir}/man5/user-dirs.conf.5.gz
%{_mandir}/man5/user-dirs.defaults.5.gz
%{_mandir}/man5/user-dirs.dirs.5.gz

%changelog
* Sat Oct 24 2015 builder - 0.15-5
- Rebuild for new 4.0 release.

* Wed Oct 14 2015 Cjacker <cjacker@foxmail.com>
- change xinitrc.d/xdg-user-dirs.sh, force create dirs everytime.
