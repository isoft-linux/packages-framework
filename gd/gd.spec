Summary: A graphics library for quick creation of PNG or JPEG images
Name: gd
Version: 2.2.3
Release: 1
License: BSD-style
URL: http://libgd.github.io/ 
Source0: https://github.com/libgd/libgd/releases/download/gd-%{version}/libgd-%{version}.tar.xz

Source1: getver.pl

Patch2:        gd-2.2.3-tests.patch
Patch3:        gd-2.2.3-overflow-in-gdImageWebpCtx.patch
Patch4:        gd-2.2.3-dynamicGetbuf-negative-rlen.patch
# TODO - created by one of upstream maintainers, but not in upstream yet
# https://github.com/libgd/libgd/pull/353
Patch5:        gd-2.2.x-fix-invalid-read-in-gdImageCreateFromTiffPtr.patch

BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: gettext-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libvpx-devel
BuildRequires: libX11-devel
BuildRequires: libXpm-devel
BuildRequires: zlib-devel
BuildRequires: pkgconfig
BuildRequires: libtool
BuildRequires: perl

%description
The gd graphics library allows your code to quickly draw images
complete with lines, arcs, text, multiple colors, cut and paste from
other images, and flood fills, and to write out the result as a PNG or
JPEG file. This is particularly useful in Web applications, where PNG
and JPEG are two of the formats accepted for inline images by most
browsers. Note that gd is not a paint program.


%package progs
Requires: gd = %{version}-%{release}
Summary: Utility programs that use libgd

%description progs
The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images. If you install
these, you must also install gd.


%package devel
Summary: The development libraries and header files for gd
Requires: gd = %{version}-%{release}
Requires: freetype-devel%{?_isa}
Requires: fontconfig-devel%{?_isa}
Requires: libjpeg-turbo-devel%{?_isa}
Requires: libpng-devel%{?_isa}
Requires: libtiff-devel%{?_isa}
Requires: libvpx-devel%{?_isa}
Requires: libX11-devel%{?_isa}
Requires: libXpm-devel%{?_isa}
Requires: zlib-devel%{?_isa}

%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.


%prep
%setup -q -n libgd-%{version}
%patch2 -p1 -b .build
%patch3 -p1 -b .gdImageWebpCtx
%patch4 -p1 -b .dynamicGetbuf
# Patch5 adds some non-text files (.tiff)
patch -p1 --binary < %{PATCH5}

# TODO - tests using freetype 2.7 are failing
# https://github.com/libgd/libgd/issues/302
# https://github.com/libgd/libgd/issues/217
sed -i -e "s|libgd_test_programs +=|libgd_freetype_test_program =|" tests/freetype/Makemodule.am
sed -i -e "s|libgd_test_programs +=|libgd_freetype_test_program +=|" tests/gdimagestringft/Makemodule.am

#missing getver.pl
cp %{SOURCE1} config

%build
./bootstrap.sh
CFLAGS="$RPM_OPT_FLAGS -DDEFAULT_FONTPATH='\"/usr/share/fonts\"'"
%configure \
    --disable-rpath \
    --with-tiff \
    --with-vpx

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.la

%check
#the test failed, it's related to font rendering, not a real failure.
export XFAIL_TESTS=gdimagestringft/gdimagestringft_bbox
make check

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
* Wed Jan 04 2017 sulit - 2.2.3-1
- upgrade gd to 2.2.3

* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 2.1.1-4
- Rebuild

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.1.1-3
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

