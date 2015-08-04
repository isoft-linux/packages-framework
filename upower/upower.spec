Summary:        Power Management Service
Name:           upower
Version:        0.99.3
Release:        1
License:        GPLv2+
Group:          Framework/Runtime/Utility 
URL:            http://upower.freedesktop.org/
Source0:        http://upower.freedesktop.org/releases/upower-%{version}.tar.xz
BuildRequires:  sqlite-devel
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  gettext
%ifnarch s390 s390x
BuildRequires:  libusb1-devel
#BuildRequires:  libimobiledevice-devel
%endif
BuildRequires:  glib2-devel >= 2.6.0
BuildRequires:  dbus-devel  >= 1.2
BuildRequires:  dbus-glib-devel >= 0.82
BuildRequires:  polkit-devel >= 0.92
BuildRequires:  libgudev-devel
Requires:       polkit >= 0.92
Requires:       udev
Requires:       pm-utils >= 1.2.2.1

%description
UPower (formerly DeviceKit-power) provides a daemon, API and command
line tools for managing power devices attached to the system.

%package devel
Summary: Headers and libraries for UPower
Group:  Framwork/Development/Library
Requires: %{name} = %{version}-%{release}
Obsoletes: DeviceKit-power-devel < 1:0.9.0-2

%description devel
Headers and libraries for UPower.

%prep
%setup -q

%build
%configure \
        --disable-gtk-doc \
        --disable-static \
        --enable-deprecated \
        --enable-introspection

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT DATADIRNAME=share
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang upower
rpmclean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f upower.lang
%defattr(-,root,root,-)
%doc NEWS COPYING AUTHORS HACKING README
%{_libdir}/libupower-glib.so.*
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_libdir}/udev/rules.d/*.rules
%dir %{_localstatedir}/lib/upower
%dir %{_sysconfdir}/UPower
%config %{_sysconfdir}/UPower/UPower.conf
%{_bindir}/*
%{_libexecdir}/*
#%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service
%{_libdir}/systemd/system/*.service
%{_libdir}/girepository-1.0/*
%{_datadir}/man/man1/upower.1.gz
%{_datadir}/man/man8/upowerd.8.gz
%files devel
%defattr(-,root,root,-)
%{_datadir}/dbus-1/interfaces/*.xml
%{_libdir}/libupower-glib.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libupower-glib
%{_includedir}/libupower-glib/up-*.h
%{_includedir}/libupower-glib/upower.h
%{_datadir}/gir-1.0/*
%{_datadir}/man/man7/UPower.7.gz
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

