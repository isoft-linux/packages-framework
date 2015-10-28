Summary:        A graphics library for quick creation of PNG or JPEG images
Name:           gd
Version:        2.1.1
Release:        3
License:        BSD-style
URL:            http://libgd.github.io/ 
Source0:        https://github.com/libgd/libgd/archive/gd-%{version}.tar.gz
Patch0:         gd-2.1.1-libvpx-1.4.0.patch
BuildRequires:  freetype-devel, fontconfig-devel
BuildRequires:  libjpeg-devel, libpng-devel, zlib-devel
BuildRequires:  libvpx-devel
%description
The gd graphics library allows your code to quickly draw images
complete with lines, arcs, text, multiple colors, cut and paste from
other images, and flood fills, and to write out the result as a PNG or
JPEG file. This is particularly useful in Web applications, where PNG
and JPEG are two of the formats accepted for inline images by most
browsers. Note that gd is not a paint program.


%package progs
Requires:       gd = %{version}-%{release}
Summary:        Utility programs that use libgd

%description progs
The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images. If you install
these, you must also install gd.


%package devel
Summary:        The development libraries and header files for gd
Requires:       gd = %{version}-%{release}
Requires:       libjpeg-devel, freetype-devel, libpng-devel, zlib-devel

%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.


%prep
%setup -q -n libgd-gd-%{version}
%patch0 -p1

%build
./bootstrap.sh
%configure --disable-rpath
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.la

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files progs
%defattr(-,root,root,-)
%{_bindir}/*
%exclude %{_bindir}/gdlib-config

%files devel
%defattr(-,root,root,-)
%{_bindir}/gdlib-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc



%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.1.1-3
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

