%define checksum b2192680b632f344243c1a6bf224c4cf
Name:    lunar-date
Version: 2.4.2
Release: 1
Summary: Chinese Lunar Date Library 

License: LGPLv2+
URL:     https://github.com/yetist/lunar-date
Source0: http://pkgs.isoft.zhcn.cc/repo/pkgs/%{name}/%{name}-%{version}.tar.gz/%{checksum}/%{name}-%{version}.tar.gz

BuildRequires: intltool
BuildRequires: gobject-introspection-devel
BuildRequires: glib2-devel

Requires: glib2

%description
Chinese Lunar Date Library 

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so.*
%{_datadir}/locale
%{_datadir}/liblunar

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/gtk-doc
%{_libdir}/girepository-1.0/LunarDate-2.0.typelib
%{_libdir}/pkgconfig/lunar-date-2.0.pc
%{_datadir}/gir-1.0/LunarDate-2.0.gir

%changelog
* Fri Nov 20 2015 wangming <ming.wang@i-soft.com.cn> - 2.0-1
- First use.
