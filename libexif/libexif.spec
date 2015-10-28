Summary: Library for extracting extra information from image files
Name: libexif
Version: 0.6.21
Release: 2
License: LGPL
URL: http://libexif.sourceforge.net/
Source0: http://umn.dl.sourceforge.net/sourceforge/libexif/%{name}-%{version}.tar.bz2

%description
Most digital cameras produce EXIF files, which are JPEG files with
extra tags that contain information about the image. The EXIF library
allows you to parse an EXIF file and read the data from those tags.

%package devel
Summary: Files needed for libexif application development
Requires: libexif = %{version}-%{release}

%description devel
The libexif-devel package contains the static libraries and header files
for writing programs that use libexif.

%prep
%setup -q

%build
CFLAGS="-fPIC $RPM_OPT_FLAGS" %configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;
%find_lang libexif-12

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libexif-12.lang
%defattr(-,root,root,-)
%{_libdir}/libexif.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libexif
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/libexif.pc
%dir %{_docdir}/libexif
%{_docdir}/libexif/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.6.21-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

