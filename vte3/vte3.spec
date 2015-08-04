%define api_version 2.91
Name: vte3
Version: 0.40.2
Release: 1
Summary: A terminal emulator
License: LGPLv2+
Group: User Interface/X
Source: http://download.gnome.org/sources/vte/0.28/vte-%{version}.tar.xz
Patch0: allow_alt_in_terminal.patch 
BuildRequires: gtk3-devel >= 2.99.3
BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: gobject-introspection-devel
BuildRequires: vala-tools

%description
VTE is a terminal emulator widget for use with GTK+.

%package devel
Summary: Files needed for developing applications which use vte
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: ncurses-devel

%description devel
The vte-devel package includes the header files and developer docs
for the vte package.

Install vte-devel if you want to develop programs which will use
vte.

%prep
%setup -q -n vte-%{version}
%patch0 -p1

%build
export CFLAGS="$CFLAGS -D_GNU_SOURCE"
%configure \
        --enable-shared \
        --disable-static \
        --with-gtk=3.0 \
        --enable-introspection
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang vte-%{api_version}
rpmclean
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f vte-%{api_version}.lang
%defattr(-,root,root)
%doc COPYING HACKING NEWS README
%doc src/iso2022.txt
%doc doc/utmpwtmp.txt doc/boxes.txt doc/openi18n/UTF-8.txt doc/openi18n/wrap.txt
%{_sysconfdir}/profile.d/vte.sh
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/Vte-%{api_version}.typelib

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_bindir}/vte*
%doc %{_datadir}/gtk-doc/html/vte-*
%{_datadir}/gir-1.0/Vte-%{api_version}.gir
%{_datadir}/vala/vapi/vte-%{api_version}.vapi

%changelog
