%define glib2_version 2.13.6
%define gtk3_version 3.6.0

%define po_package gtksourceview-3.0

Summary: A library for viewing source files
Name: gtksourceview
Version: 3.18.1
Release: 1
License: LGPLv2+ and GPLv2+
URL: http://gtksourceview.sourceforge.net/ 
Source0: http://download.gnome.org/sources/gtksourceview/3.6/gtksourceview-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
BuildRequires: libxml2-devel
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: intltool >= 0.35
BuildRequires: gettext 

%description
GtkSourceView is a text widget that extends the standard GTK+
GtkTextView widget. It improves GtkTextView by implementing 
syntax highlighting and other features typical of a source code editor.

%package devel
Summary: Files to compile applications that use gtksourceview2
Requires: %{name} = %{version}-%{release}
Requires: gtk3-devel >= %{gtk3_version} 
Requires: libxml2-devel
Requires: pkgconfig

%description devel
gtksourceview-devel contains the files required to compile 
applications which use GtkSourceView 

%prep
%setup -q -n gtksourceview-%{version}

%build
%configure --disable-gtk-doc --disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT DATADIRNAME=share

%find_lang %{po_package}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{po_package}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS MAINTAINERS 
%{_datadir}/gtksourceview-3.0
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gtksourceview-3.0
%{_datadir}/gtk-doc
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_libdir}/girepository-?.?/GtkSource-3.0.typelib
%{_datadir}/gir-1.0/GtkSource-3.0.gir
%{_datadir}/vala/vapi/gtksourceview-3.0.deps
%{_datadir}/vala/vapi/gtksourceview-3.0.vapi

%changelog
* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 3.18.1

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

