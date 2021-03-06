Name:          ideviceinstaller
Version:       1.1.0
Release:       6
Summary:       tool to allow to install, upgrade, uninstall, archive, restore, and enumerate installed or archived apps of iOS device.

License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
BuildRequires: libxml2-devel
BuildRequires: python-devel
BuildRequires: libplist-devel, libimobiledevice-devel
BuildRequires: libzip-devel

%description
ideviceinstaller is a tool to interact with the installation_proxy
of an iOS device allowing to install, upgrade, uninstall, archive, restore,
and enumerate installed or archived apps.

%prep
%setup -q

sed -i 's/-Werror//g' configure.ac
%build
autoreconf -ivf
%configure

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/ideviceinstaller
%{_mandir}/man1/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.1.0-6
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

