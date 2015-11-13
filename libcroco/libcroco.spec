Name:             libcroco
Summary:          A CSS2 parsing library
Version:          0.6.9
Release:          2%{?dist}
License:          LGPLv2
Source:           http://download.gnome.org/sources/libcroco/0.6/%{name}-%{version}.tar.xz

BuildRequires:    pkgconfig
BuildRequires:    glib2-devel
BuildRequires:    libxml2-devel

%description
CSS2 parsing and manipulation library for GNOME

%package devel
Summary:          Libraries and include files for developing with libcroco
Requires:         %{name} = %{version}-%{release}
Requires:         glib2-devel
Requires:         libxml2-devel

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with libcroco.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/csslint-0.6
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/libcroco-0.6
%{_bindir}/croco-0.6-config
%{_libdir}/pkgconfig/libcroco-0.6.pc
%{_datadir}/gtk-doc/html/libcroco

%changelog
* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 0.6.9-2
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.6.8-4
- Rebuild for new 4.0 release.

