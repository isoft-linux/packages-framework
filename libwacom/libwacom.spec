%global udevdir %(pkg-config --variable=udevdir udev)

Name:           libwacom
Version:        0.15
Release:        2%{?dist}
Summary:        Tablet Information Client Library
Requires:       %{name}-data

License:        MIT
URL:            http://linuxwacom.sourceforge.net

Source0:        http://prdownloads.sourceforge.net/linuxwacom/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:  autoconf automake libtool doxygen
BuildRequires:  glib2-devel libgudev-devel
BuildRequires:  systemd-devel

%description
%{name} is a library that provides information about Wacom tablets and
tools. This information can then be used by drivers or applications to tweak
the UI or general settings to match the physical tablet.

%package devel
Summary:        Tablet Information Client Library Library Development Package
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Tablet information client library library development package.

%package data
Summary:        Tablet Information Client Library Library Data Files
BuildArch:      noarch

%description data
Tablet information client library library data files.

%prep
%setup -q -n %{name}-%{version}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
install -d ${RPM_BUILD_ROOT}/%{udevdir}/rules.d
# auto-generate the udev rule from the database entries
pushd tools
./generate-udev-rules > ${RPM_BUILD_ROOT}/%{udevdir}/rules.d/65-libwacom.rules
popd

# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README 
%{_libdir}/libwacom.so.*
%{udevdir}/rules.d/65-libwacom.rules
%{_bindir}/libwacom-list-local-devices

%files devel
%doc COPYING
%dir %{_includedir}/libwacom-1.0/
%dir %{_includedir}/libwacom-1.0/libwacom
%{_includedir}/libwacom-1.0/libwacom/libwacom.h
%{_libdir}/libwacom.so
%{_libdir}/pkgconfig/libwacom.pc

%files data
%doc COPYING
%dir %{_datadir}/libwacom
%{_datadir}/libwacom/*.tablet
%{_datadir}/libwacom/*.stylus
%dir %{_datadir}/libwacom/layouts
%{_datadir}/libwacom/layouts/*.svg

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.15-2
- Rebuild for new 4.0 release.

