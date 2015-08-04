Name:		libindicator
Version:	12.10.1
Release:	5%{?dist}
Summary:	Shared functions for Ayatana indicators

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://launchpad.net/libindicator
Source0:	https://launchpad.net/libindicator/12.10/12.10.1/+download/%{name}-%{version}.tar.gz

BuildRequires:	chrpath
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	pkgconfig

BuildRequires:	dbus-glib-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel


%description
A set of symbols and convenience functions that all Ayatana indicators are
likely to use.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package tools
Summary:	Shared functions for Ayatana indicators - Tools
Group:		Development/Tools
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description tools
This package contains tools used by the %{name} package, the
Ayatana indicators system.


%package gtk3
Summary:	GTK+3 build of %{name}
Group:		System Environment/Libraries

%description gtk3
A set of symbols and convenience functions that all Ayatana indicators
are likely to use. This is the GTK+ 3 build of %{name}, for use
by GTK+ 3 apps.


%package gtk3-devel
Summary:	Development files for %{name}-gtk3
Group:		Development/Libraries

Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description gtk3-devel
The %{name}-gtk3-devel package contains libraries and header files for
developing applications that use %{name}-gtk3.


%package gtk3-tools
Summary:	Shared functions for Ayatana indicators - GTK3 Tools
Group:		Development/Tools

Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description gtk3-tools
This package contains tools used by the %{name}-gtk3 package, the
Ayatana indicators system. This package contains the builds of the
tools for the GTK+3 build of %{name}.


%prep
%setup -q

%build
%global _configure ../configure
rm -rf build-gtk2 build-gtk3
mkdir build-gtk2 build-gtk3

pushd build-gtk2
export CFLAGS="%{optflags} -Wno-error=deprecated-declarations"
%configure --with-gtk=2 --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
popd

pushd build-gtk3
export CFLAGS="%{optflags} -Wno-error=deprecated-declarations"
%configure --with-gtk=3 --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
popd


%install
pushd build-gtk2
make install DESTDIR=%{buildroot}
popd

pushd build-gtk3
make install DESTDIR=%{buildroot}
popd


# Ubuntu doesn't package the dummy indicator
rm -f %{buildroot}%{_libdir}/libdummy-indicator*.so

# Remove libtool files
find %{buildroot} -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post gtk3 -p /sbin/ldconfig

%postun gtk3 -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS ChangeLog
%{_libdir}/libindicator.so.*


%files devel
%dir %{_includedir}/libindicator-0.4/
%dir %{_includedir}/libindicator-0.4/libindicator/
%{_includedir}/libindicator-0.4/libindicator/*.h
%{_libdir}/libindicator.so
%{_libdir}/pkgconfig/indicator-0.4.pc


%files tools
%{_libexecdir}/indicator-loader
%dir %{_datadir}/libindicator/
%{_datadir}/libindicator/80indicator-debugging


%files gtk3
%doc AUTHORS COPYING NEWS ChangeLog
%{_libdir}/libindicator3.so.*


%files gtk3-devel
%dir %{_includedir}/libindicator3-0.4/
%dir %{_includedir}/libindicator3-0.4/libindicator/
%{_includedir}/libindicator3-0.4/libindicator/*.h
%{_libdir}/libindicator3.so
%{_libdir}/pkgconfig/indicator3-0.4.pc


%files gtk3-tools
%{_libexecdir}/indicator-loader3

%changelog
