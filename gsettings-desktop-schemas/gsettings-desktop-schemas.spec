%global debug_package %{nil}

Name:           gsettings-desktop-schemas
Version:        3.18.0
Release:        2
Summary:        A collection of GSettings schemas

License:        LGPLv2+
URL:            http://bugzilla.gnome.org/enter_bug.cgi?product=gsettings-desktop-schemas
Source:         http://download.gnome.org/sources/%{name}/3.13/%{name}-%{version}.tar.xz
Patch0:         gsettings-default-desktop-font-size.patch
Patch1:         gsettings-desktop-schemas-default-wm-setting.patch

BuildRequires: glib2-devel >= 2.31.0
BuildRequires: intltool
BuildRequires: gobject-introspection-devel

Requires: glib2 >= 2.31.0

%description
gsettings-desktop-schemas contains a collection of GSettings schemas for
settings shared by various components of a desktop.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries
and header files for developing applications that use %{name}.


%prep
%setup -q
#%patch0 -p1
#%patch1 -p1
%build
%configure --disable-schemas-compile --enable-introspection=yes
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%find_lang %{name} --with-gnome

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi


%files -f %{name}.lang
%doc AUTHORS COPYING MAINTAINERS NEWS README
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/GConf/gsettings/gsettings-desktop-schemas.convert
%{_datadir}/GConf/gsettings/wm-schemas.convert
%{_libdir}/girepository-1.0/GDesktopEnums-3.0.typelib

%files devel
%doc HACKING
%{_includedir}/*
%{_datadir}/pkgconfig/*
%{_datadir}/gir-1.0/GDesktopEnums-3.0.gir

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.18.0-2
- Rebuild for new 4.0 release.

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

