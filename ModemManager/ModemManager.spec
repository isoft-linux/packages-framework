%define ppp_version 2.4.6

Summary: Mobile broadband modem management service
Name: ModemManager
Version: 1.4.10
Release: 2
Source: %{name}-%{version}.tar.xz
Patch0: modemmanager-remove-unused-var-fix-clang-build.patch

License: GPLv2+

URL:    http://www.freedesktop.org/software/ModemManager/ 

Requires: dbus-glib >= 0.86
Requires: glib2 >= 2.18
BuildRequires: glib2-devel >= 2.18
BuildRequires: dbus-glib-devel >= 0.82
BuildRequires: libgudev-devel >= 143
BuildRequires: ppp = %{ppp_version}
BuildRequires: ppp-devel = %{ppp_version}
BuildRequires: automake autoconf intltool libtool
BuildRequires: gobject-introspection-devel
BuildRequires: vala-tools

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%description
The ModemManager service provides a consistent API to operate many different
modems, including mobile broadband (3G) devices.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--enable-more-warnings=error \
	--with-udev-base-dir=/lib/udev \
	--with-tests=yes \
	--with-docs=yes \
	--disable-static \
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version} \
	--with-polkit=no \
	--with-dist-version=%{version}-%{release} \
    --without-mbim \
    --without-qmi \
    --enable-introspection \
    --enable-vala

make %{?_smp_mflags}

%check
#make check

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
%systemd_post ModemManager.service


%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi
%systemd_postun_with_restart ModemManager.service


%preun
%systemd_preun ModemManager.service

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files
%defattr(0644, root, root, 0755)
%doc COPYING README
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager1.service
%attr(0755,root,root) %{_sbindir}/ModemManager
%{_bindir}/mmcli
%dir %{_libdir}/%{name}
%attr(0755,root,root) %{_libdir}/%{name}/*.so*
/lib/udev/rules.d/*
%{_datadir}/dbus-1/interfaces/*.xml
%{_libdir}/libmm-glib.so.*
%{_libdir}/systemd/system/ModemManager.service
%{_libdir}/girepository-1.0/ModemManager-1.0.typelib

%{_datadir}/icons/hicolor/22x22/apps/ModemManager.png
%{_mandir}/man8/ModemManager.8.gz
%{_mandir}/man8/mmcli.8.gz


%files devel
%defattr(-, root, root, -)
%{_includedir}/*
%{_libdir}/libmm-glib.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/ModemManager-1.0.gir
%{_datadir}/vala/vapi/libmm-glib.deps
%{_datadir}/vala/vapi/libmm-glib.vapi

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.4.10-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

