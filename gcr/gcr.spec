Name:           gcr
Version:        3.16.0
Release:        1
Summary:        A library for bits of crypto UI and parsing

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://live.gnome.org/CryptoGlue/
Source0:        http://download.gnome.org/sources/gcr/3.10/gcr-%{version}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk3-devel
BuildRequires:  p11-kit-devel
BuildRequires:  gnupg
BuildRequires:  libgcrypt-devel
BuildRequires:  libtasn1-tools
BuildRequires:  libtasn1-devel
BuildRequires:  chrpath
BuildRequires:  vala-devel
BuildRequires:  vala-tools

Conflicts: gnome-keyring < 3.3.0

%description
gcr is a library for displaying certificates, and crypto UI, accessing
key stores. It also provides a viewer for crypto files on the GNOME
desktop.

gck is a library for accessing PKCS#11 modules like smart cards.

%package devel
Summary: Development files for gcr
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The gcr-devel package includes the header files for the gcr library.


%prep
%setup -q


%build
%configure --enable-introspection
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libmock-test-module.*
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/gcr-viewer.desktop
%find_lang %{name}

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/lib*.so.*
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gcr-viewer
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/gcr-prompter

%post
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc COPYING
%{_bindir}/gcr-viewer
%{_datadir}/applications/gcr-viewer.desktop
%dir %{_datadir}/GConf
%dir %{_datadir}/GConf/gsettings
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp.convert
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp_keyservers.convert
%{_datadir}/glib-2.0/schemas/org.gnome.crypto.pgp.gschema.xml
%{_libdir}/girepository-1.0
%{_libdir}/libgck-1.so.*
%{_libdir}/libgcr-3.so.*
%{_libdir}/libgcr-base-3.so.*
%{_libdir}/libgcr-ui-3.so.*
%{_datadir}/gcr-3
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/gcr-crypto-types.xml
%{_libexecdir}/gcr-prompter
%{_datadir}/dbus-1/services/org.gnome.keyring.PrivatePrompter.service
%{_datadir}/dbus-1/services/org.gnome.keyring.SystemPrompter.service
%{_datadir}/applications/gcr-prompter.desktop

%files devel
%{_includedir}/gck-1
%{_includedir}/gcr-3
%{_libdir}/libgck-1.so
%{_libdir}/libgcr-3.so
%{_libdir}/libgcr-base-3.so
%{_libdir}/libgcr-ui-3.so
%{_libdir}/pkgconfig/gck-1.pc
%{_libdir}/pkgconfig/gcr-3.pc
%{_libdir}/pkgconfig/gcr-base-3.pc
%{_libdir}/pkgconfig/gcr-ui-3.pc
%{_datadir}/gir-1.0
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/gck
%{_datadir}/gtk-doc/html/gcr-3
%{_datadir}/vala/*


%changelog
