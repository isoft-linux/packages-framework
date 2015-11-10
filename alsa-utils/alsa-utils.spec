Summary: 	Advanced Linux Sound Architecture (ALSA) utilities
Name: 		alsa-utils
Version: 	1.1.0
Release:  	2	
License: 	GPL
URL: 		http://www.alsa-project.org/
Source: 	ftp://ftp.alsa-project.org/pub/utils/alsa-utils-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	alsa-lib-devel 
BuildRequires:	ncurses-devel
BuildRequires:	gettext-devel
BuildRequires:  systemd-devel
Conflicts:	udev < 062

%description
This package contains command line utilities for the Advanced Linux Sound
Architecture (ALSA).

%prep
%setup -q -n %{name}-%{version}

%build
#autoreconf -f -i
%configure CFLAGS="$RPM_OPT_FLAGS -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64" --disable-xmlto  --disable-alsaconf --datadir=%{_sysconfdir} --disable-bat 
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf %{buildroot}%{_datadir}/locale/{de,fr,ja}
#own this dir. otherwise alsactl store will failed.
mkdir -p $RPM_BUILD_ROOT/var/lib/alsa


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man?/*
%{_sysconfdir}/sounds/alsa/*
%{_sysconfdir}/alsa/*
%{_libdir}/systemd/system/alsa-restore.service
%{_libdir}/systemd/system/alsa-state.service
#%{_libdir}/systemd/system/alsa-store.service
%{_libdir}/systemd/system/basic.target.wants/alsa-restore.service
%{_libdir}/systemd/system/basic.target.wants/alsa-state.service
#%{_libdir}/systemd/system/shutdown.target.wants/alsa-store.service
%{_libdir}/udev/rules.d/90-alsa-restore.rules
/var/lib/alsa

%changelog
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 1.1.0-2
- Update to 1.1.0

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.29-3
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

