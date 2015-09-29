%define         clutter_version 1.0

Name:           clutter-gtk
Version:        1.6.4
Release:        1 
Summary:        A basic GTK clutter widget

Group:          Development/Languages
License:        LGPLv2+
URL:            http://www.clutter-project.org
Source0:        http://www.clutter-project.org/sources/%{name}/1.1/%{name}-%{version}.tar.xz
Patch0:         clutter-gtk-fixdso.patch

BuildRequires:  gtk3-devel >= 3.0.0
BuildRequires:  clutter-devel >= 1.9
BuildRequires:  gobject-introspection-devel

%description
clutter-gtk is a library which allows the embedding of a Clutter
canvas (or "stage") into a GTK+ application, as well as embedding
GTK+ widgets inside the stage.

%package devel
Summary:        Clutter-gtk development environment
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk3-devel clutter-devel

%description devel
Header files and libraries for building a extension library for the
clutter-gtk.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang cluttergtk-1.0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f cluttergtk-1.0.lang
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GtkClutter-%{clutter_version}.typelib

%files devel
%{_includedir}/clutter-gtk-%{clutter_version}/
%{_libdir}/pkgconfig/clutter-gtk-%{clutter_version}.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkClutter-%{clutter_version}.gir
%{_datadir}/gtk-doc/html/clutter-gtk-1.0

%changelog
