%define VER 6.8.9
%define Patchlevel 1 
Summary: An X application for displaying and manipulating images.
Name: ImageMagick
%if "%{Patchlevel}" != ""
Version: %{VER}.%{Patchlevel}
%else
Version: %{VER}
%endif
Release: 3
License: freeware
Group: Applications/Multimedia
%if "%{Patchlevel}" != ""
Source: ftp://ftp.ImageMagick.org/pub/ImageMagick/ImageMagick-%{VER}-%{Patchlevel}.tar.gz
%else
Source: ftp://ftp.ImageMagick.org/pub/ImageMagick/ImageMagick-%{version}.tar.gz
%endif
Source1: magick_small.png

Patch0: ImageMagick-modules.patch
Url: http://www.imagemagick.org/
BuildRequires: bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires: libtiff-devel, libungif-devel, zlib-devel, perl
BuildRequires: freetype-devel >= 2.1
BuildRequires: automake >= 1.7 autoconf >= 2.58 libtool >= 1.5
BuildRequires: ghostscript-devel
BuildRequires: perl-devel
BuildRequires: lcms2-devel, libxml2-devel, librsvg2-devel

%description
ImageMagick(TM) is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate
and dis play images. If you want to develop your own applications
which use ImageMagick code or APIs, you need to install
ImageMagick-devel as well.

%package devel
Summary: Static libraries and header files for ImageMagick app development.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: ghostscript-devel
Requires: bzip2-devel
Requires: freetype-devel
Requires: libtiff-devel
Requires: libjpeg-devel
Requires: lcms2-devel
Requires: pkgconfig

%description devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.

%package perl
Summary: ImageMagick perl bindings
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: perl >= 5.6.0

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.

%package c++
Summary: ImageMagick Magick++ library (C++ bindings)
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.

%package c++-devel
Summary: C++ bindings for the ImageMagick library
Group: Development/Libraries
Requires: %{name}-c++ = %{version}
Requires: %{name}-devel = %{version}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.
You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.

%prep
%if "%{Patchlevel}" != ""
%setup -q -n %{name}-%{VER}-%{Patchlevel}
%else
%setup -q -n %{name}-%{VER}
%endif
%patch0 -p1
%build
export CC=clang
export CXX=clang++

%configure --enable-shared \
            --with-modules \
            --with-perl \
	        --without-x \
            --with-threads \
            --with-magick_plus_plus \
	        --with-gslib \
            --with-lcms2 \
            --without-lcms \
            --with-rsvg \
	        --with-xml \
            --without-openexr \
            --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
            --with-windows-font-dir=%{_datadir}/fonts/default/TrueType \
	        --without-dps

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

find $RPM_BUILD_ROOT -name "*.bs" |xargs rm -f
find $RPM_BUILD_ROOT -name ".packlist" |xargs rm -f
find $RPM_BUILD_ROOT -name "perllocal.pod" |xargs rm -f

# perlmagick: build files list
echo "%defattr(-,root,root)" > perl-pkg-files
find $RPM_BUILD_ROOT/%{_libdir}/perl* -type f -print \
	| sed "s@^$RPM_BUILD_ROOT@@g" > perl-pkg-files 
find $RPM_BUILD_ROOT%{perl_vendorarch} -type d -print \
	| sed "s@^$RPM_BUILD_ROOT@%dir @g" \
 	| grep -v '^%dir %{perl_vendorarch}$' \
	| grep -v '/auto$' >> perl-pkg-files 
if [ -z perl-pkg-files ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

rm -rf $RPM_BUILD_ROOT%{_libdir}/ImageMagick
# Keep config
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}-%{VER}/[a-b,d-z,A-Z]*
rm -rf $RPM_BUILD_ROOT%{_libdir}/libltdl.*
rm -f  $RPM_BUILD_ROOT%{_libdir}/ImageMagick-*/modules*/*/*.a
rm -f  $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/libMagickCore-6*.so.*
%{_libdir}/libMagickWand-6*.so.*
%{_bindir}/[a-z]*
%{_libdir}/ImageMagick-6*
%{_datadir}/ImageMagick-6
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/ImageMagick.*
%{_datadir}/doc/ImageMagick-6
%dir %{_sysconfdir}/ImageMagick-6
%{_sysconfdir}/ImageMagick-6/*

%files devel
%defattr(-,root,root)
%{_bindir}/*-config
%{_libdir}/libMagickCore-6*.so
%{_libdir}/libMagickWand-6*.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/MagickCore-6*.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/MagickWand-6*.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-6*.pc
%{_libdir}/pkgconfig/Wand.pc
%{_libdir}/pkgconfig/Wand-6*.pc
%{_includedir}/ImageMagick-6/magick
%{_includedir}/ImageMagick-6/wand
%{_mandir}/man1/*-config.*

%files c++
%defattr(-,root,root)
%{_libdir}/libMagick++-6*.so.*

%files c++-devel
%defattr(-,root,root)
%{_bindir}/Magick++-config
%{_includedir}/ImageMagick-6/Magick++.h
%{_includedir}/ImageMagick-6/Magick++
%{_libdir}/libMagick++-6*.so
%{_libdir}/pkgconfig/Magick++*.pc
%{_libdir}/pkgconfig/ImageMagick++*.pc
%{_mandir}/man1/Magick++-config.*

%files perl -f perl-pkg-files
%defattr(-,root,root)
%{_mandir}/man3/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.
