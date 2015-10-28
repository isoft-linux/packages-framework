%define glib2_version 2.16.0
%define dbus_version 1.0
%define gcrypt_version 1.2.2

Summary: Framework for managing passwords and other secrets
Name: libgnome-keyring
Version: 3.12.0
Release: 6%{?dist}
License: GPLv2+ and LGPLv2+
#VCS: git:git://git.gnome.org/libgnome-keyring
Source: http://download.gnome.org/sources/libgnome-keyring/3.12/libgnome-keyring-%{version}.tar.xz
URL: http://live.gnome.org/GnomeKeyring


BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: libgcrypt-devel >= %{gcrypt_version}
BuildRequires: intltool
BuildRequires: gobject-introspection-devel
BuildRequires: vala-devel
BuildRequires: vala-tools

Conflicts: gnome-keyring < 2.29.4


%description
gnome-keyring is a program that keep password and other secrets for
users. The library libgnome-keyring is used by applications to integrate
with the gnome-keyring system.

%package devel
Summary: Development files for libgnome-keyring
License: LGPLv2+
Requires: %name = %{version}-%{release}
Requires: glib2-devel
Conflicts: gnome-keyring-devel < 2.29.4

%description devel
The libgnome-keyring-devel package contains the libraries and
header files needed to develop applications that use libgnome-keyring.


%prep
%setup -q -n libgnome-keyring-%{version}


%build
%configure --disable-gtk-doc --enable-introspection=yes

# avoid unneeded direct dependencies
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang libgnome-keyring


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f libgnome-keyring.lang
%doc AUTHORS NEWS README COPYING HACKING
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gir-1.0
%{_datadir}/vala/
%doc %{_datadir}/gtk-doc/


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.12.0-6
- Rebuild for new 4.0 release.

