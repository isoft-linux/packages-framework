%define glib2_version 2.48
%define gtk3_version 3.20

%define po_package gtksourceview-3.0

Summary: A library for viewing source files
Name: gtksourceview
Version: 3.21.2
Release: 1
License: LGPLv2+ and GPLv2+
URL: http://gtksourceview.sourceforge.net/ 
Source0: http://download.gnome.org/sources/gtksourceview/3.6/gtksourceview-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
BuildRequires: gettext 
BuildRequires: pkgconfig(gdk-pixbuf-2.0)
BuildRequires: pkgconfig(gladeui-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(pango)
BuildRequires: itstool
BuildRequires: vala-tools

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
%configure --disable-gtk-doc --disable-static --enable-glade-catalog

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT DATADIRNAME=share
# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

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
%{_libdir}/girepository-1.0/GtkSource-3.0.typelib

%files devel
%defattr(-,root,root,-)
%{_includedir}/gtksourceview-3.0
%{_datadir}/gtk-doc
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkSource-3.0.gir
%dir %{_datadir}/glade
%dir %{_datadir}/glade/catalogs
%{_datadir}/glade/catalogs/gtksourceview.xml

%changelog
* Fri Jul 08 2016 zhouyang <yang.zhou@i-soft.com.cn> - 3.21.2-1
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.18.1-2
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 3.18.1

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

