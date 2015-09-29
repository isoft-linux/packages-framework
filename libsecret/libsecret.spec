Name:           libsecret
Version:        0.18.3
Release:        1
Summary:        Library for storing and retrieving passwords and other secrets
Group:          System Environment/Libraries 
License:        LGPLv2+
URL:            https://live.gnome.org/Libsecret
Source0:        libsecret-%{version}.tar.xz
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  intltool
BuildRequires:  libgcrypt-devel >= 1.2.2
BuildRequires:  gtk-doc
BuildRequires:  libxslt-devel
BuildRequires:  docbook-style-xsl
BuildRequires:  vala-tools
Provides:       bundled(egglib)

%description
libsecret is a library for storing and retrieving passwords and other secrets.
It communicates with the "Secret Service" using DBus. gnome-keyring and
KSecretService are both implementations of a Secret Service.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries 
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rpmclean

%find_lang libsecret


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f libsecret.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/secret-tool
%{_libdir}/libsecret-1.so.*
%{_libdir}/girepository-1.0/Secret-1.typelib
%doc %{_mandir}/man1/secret-tool.1.gz

%files devel
%{_includedir}/libsecret-1/
%{_libdir}/libsecret-1.so
%{_libdir}/pkgconfig/libsecret-1.pc
%{_datadir}/gir-1.0/Secret-1.gir
%doc %{_datadir}/gtk-doc/
%{_libdir}/pkgconfig/libsecret-unstable.pc
%{_datadir}/vala/vapi/libsecret-1.deps
%{_datadir}/vala/vapi/libsecret-1.vapi

%changelog
* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

