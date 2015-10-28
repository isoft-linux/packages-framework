Name:           media-player-info
Version:        22
Release:        2
Summary:        Data files describing media player capabilities

License:        BSD
URL:            http://www.freedesktop.org/wiki/Software/media-player-info
Source0:        http://www.freedesktop.org/software/media-player-info/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  libudev-devel
BuildRequires:  python3
Requires:       udev

%description
media-player-info is a repository of data files describing media player
(mostly USB Mass Storage ones) capabilities. These files contain information
about the directory layout to use to add music to these devices, about the
supported file formats, etc.

The package also installs a udev rule to identify media player devices.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README NEWS AUTHORS
/usr/share/media-player-info
/usr/lib/udev/rules.d/*
/usr/lib/udev/hwdb.d/20-usb-media-players.hwdb


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 22-2
- Rebuild for new 4.0 release.

