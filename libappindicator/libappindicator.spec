Name:		libappindicator
Version:	12.10.0
Release:	10%{?dist}
Summary:	Application indicators library

Group:		System Environment/Libraries
License:	LGPLv2 and LGPLv3
URL:		https://launchpad.net/libappindicator
Source0:	https://launchpad.net/libappindicator/12.10/%{version}/+download/%{name}-%{version}.tar.gz
Patch0:		0001_Fix_mono_dir.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc
BuildRequires:	vala-tools
BuildRequires:	dbus-glib-devel
BuildRequires:	libdbusmenu-devel
BuildRequires:	libdbusmenu-gtk2-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	python2-devel
BuildRequires:	pygtk2-devel

%description
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.


%package -n python-appindicator
Summary:	Python 2 bindings for %{name}
Group:		System Environment/Libraries

Requires:	%{name} = %{version}-%{release}

%description -n python-appindicator
This package contains the Python 2 bindings for the appindicator library.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	libdbusmenu-devel

%description devel
This package contains the development files for the appindicator library.


%package gtk3
Summary:	Application indicators library - GTK 3
Group:		System Environment/Libraries

%description gtk3
A library to allow applications to export a menu into the Unity Menu bar. Based
on KSNI it also works in KDE and will fallback to generic Systray support if
none of those are available.

This package contains the GTK 3 version of this library.


%package gtk3-devel
Summary:	Development files for %{name}-gtk3
Group:		Development/Libraries

Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	libdbusmenu-devel

%description gtk3-devel
This package contains the development files for the appindicator-gtk3 library.


%package docs
Summary:	Documentation for %{name} and %{name}-gtk3
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the appindicator and
appindicator-gtk3 libraries.


%prep
%setup -q

#disable mono bindings in main package.
sed -i 's/SUBDIRS += mono//g' bindings/Makefile.am

autoreconf -ivf 

%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
export CFLAGS="%{optflags} $CFLAGS -Wno-deprecated-declarations"
%configure --with-gtk=2 --enable-gtk-doc --disable-static --disable-mono-test
# Parallel make, crash the build
make -j1 V=1
popd

pushd build-gtk3
export CFLAGS="%{optflags} $CFLAGS -Wno-deprecated-declarations"
%configure --with-gtk=3 --enable-gtk-doc --disable-static --disable-mono-test
# Parallel make, crash the build
make -j1 V=1
popd


%install
pushd build-gtk2
make install DESTDIR=%{buildroot}
popd

pushd build-gtk3
make install DESTDIR=%{buildroot}
popd

find %{buildroot} -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post gtk3 -p /sbin/ldconfig

%postun gtk3 -p /sbin/ldconfig


%files
%doc AUTHORS README COPYING COPYING.LGPL.2.1
%{_libdir}/libappindicator.so.*
%{_libdir}/girepository-1.0/AppIndicator-0.1.typelib


%files -n python-appindicator
%dir %{python_sitearch}/appindicator/
%{python_sitearch}/appindicator/__init__.py*
%{python_sitearch}/appindicator/_appindicator.so
%dir %{_datadir}/pygtk/
%dir %{_datadir}/pygtk/2.0/
%dir %{_datadir}/pygtk/2.0/defs/
%{_datadir}/pygtk/2.0/defs/appindicator.defs


%files devel
%dir %{_includedir}/libappindicator-0.1/
%dir %{_includedir}/libappindicator-0.1/libappindicator/
%{_includedir}/libappindicator-0.1/libappindicator/*.h
%{_libdir}/libappindicator.so
%{_libdir}/pkgconfig/appindicator-0.1.pc
%{_datadir}/gir-1.0/AppIndicator-0.1.gir
%{_datadir}/vala/vapi/appindicator-0.1.vapi
%{_datadir}/vala/vapi/appindicator-0.1.deps


%files gtk3
%doc AUTHORS README COPYING COPYING.LGPL.2.1
%{_libdir}/libappindicator3.so.*
%{_libdir}/girepository-1.0/AppIndicator3-0.1.typelib


%files gtk3-devel
%dir %{_includedir}/libappindicator3-0.1/
%dir %{_includedir}/libappindicator3-0.1/libappindicator/
%{_includedir}/libappindicator3-0.1/libappindicator/*.h
%{_libdir}/libappindicator3.so
%{_libdir}/pkgconfig/appindicator3-0.1.pc
%{_datadir}/gir-1.0/AppIndicator3-0.1.gir
%{_datadir}/vala/vapi/appindicator3-0.1.vapi
%{_datadir}/vala/vapi/appindicator3-0.1.deps


%files docs
%doc %{_datadir}/gtk-doc/html/libappindicator/

%changelog
