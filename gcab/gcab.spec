Name:           gcab
Version:        0.6
Release:        2
Summary:        Cabinet file library and tool

License:        LGPLv2+
URL:            http://ftp.gnome.org/pub/GNOME/sources/gcab
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gcab/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  intltool
BuildRequires:  vala-tools
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  zlib-devel

%description
gcab is a tool to manipulate Cabinet archive.

%package -n libgcab
Summary:        Library to create Cabinet archives

%description -n libgcab
libgcab is a library to manipulate Cabinet archive using GIO/GObject.

%package -n libgcab-devel
Summary:        Development files to create Cabinet archives
Requires:       libgcab%{?_isa} = %{version}-%{release}
Requires:       glib2-devel
Requires:       pkgconfig

%description -n libgcab-devel
libgcab is a library to manipulate Cabinet archive.

Libraries, includes, etc. to compile with the gcab library.

%prep
%setup -q

%build
# --enable-fast-install is needed to fix libtool "cannot relink `gcab'"
%configure --disable-silent-rules --disable-static --enable-fast-install
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la

%find_lang %{name}

rpmclean
%post -n libgcab -p /sbin/ldconfig
%postun -n libgcab -p /sbin/ldconfig

%files
%doc COPYING NEWS
%{_bindir}/gcab
%{_mandir}/man1/gcab.1*

%files -n libgcab -f %{name}.lang
%doc COPYING NEWS
%{_libdir}/girepository-1.0/GCab-1.0.typelib
%{_libdir}/libgcab-1.0.so.*

%files -n libgcab-devel
%{_datadir}/gir-1.0/GCab-1.0.gir
%{_datadir}/gtk-doc/html/gcab/*
%{_datadir}/vala/vapi/libgcab-1.0.vapi
%{_includedir}/libgcab-1.0/*
%{_libdir}/libgcab-1.0.so
%{_libdir}/pkgconfig/libgcab-1.0.pc

%changelog
