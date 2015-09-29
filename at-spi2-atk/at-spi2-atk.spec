Name:           at-spi2-atk
Version:        2.18.0
Release:        2
Summary:        A GTK+ module that bridges ATK to D-Bus at-spi

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:        http://download.gnome.org/sources/at-spi2-atk/2.4/%{name}-%{version}.tar.xz

BuildRequires:  at-spi2-core-devel
BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  atk-devel
BuildRequires:  intltool
Requires:       at-spi2-core

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

This package includes a gtk-module that bridges ATK to the new
D-Bus based at-spi.

%package gtk2
Summary: at-spi2-atk gtk2 module
Group:   System Environment/Libraries 
Requires: %{name} = %{version}-%{release}
Requires: at-spi2-core

%description gtk2 
at-spi2-atk gtk2 module

%package devel
Summary: Development files and headers for at-spi2-atk
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: at-spi2-core-devel 
Requires: atk-devel

%description devel
The package includes the header files and
API documentation for at-spi2-atk 


%prep
%setup -q

%build
%configure --disable-relocate
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/libatk-bridge.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/modules/libatk-bridge.la

#%find_lang %{name}

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files
%doc COPYING AUTHORS README
%{_libdir}/gnome-settings-daemon-?.?/gtk-modules/at-spi2-atk.desktop
%{_libdir}/*.so.*

%files gtk2
%dir %{_libdir}/gtk-2.0/modules
%{_libdir}/gtk-2.0/modules/libatk-bridge.so

%files devel
%dir %{_includedir}/at-spi2-atk
%{_includedir}/at-spi2-atk/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

