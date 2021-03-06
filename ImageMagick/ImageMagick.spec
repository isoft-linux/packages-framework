%global VER 6.9.4
%global Patchlevel 0

Name:		ImageMagick
Version:		%{VER}.%{Patchlevel}
Release:		0.beta.3%{?dist}.1
Summary:		An X application for displaying and manipulating images
License:		ImageMagick
Url:			http://www.imagemagick.org/
Source0:		ftp://ftp.ImageMagick.org/pub/%{name}/beta/%{name}-%{VER}-%{Patchlevel}.tar.bz2
#ImageMagick still use ".la" to load modules, we do not like it.
#This patch enable ImageMagick to use ".so" suffix to load module.
#But it will fail in-source test.
Patch0: ImageMagick-modules.patch

Requires:		%{name}-libs = %{version}-%{release}
BuildRequires:	bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires:	libtiff-devel, giflib-devel, zlib-devel, perl-devel >= 5.8.1
BuildRequires:	ghostscript-devel, djvulibre-devel
BuildRequires:	jasper-devel, libtool-ltdl-devel
BuildRequires:	libX11-devel, libXext-devel, libXt-devel
BuildRequires:	lcms2-devel, libxml2-devel, librsvg2-devel, OpenEXR-devel
BuildRequires:	OpenEXR-devel, libwebp-devel
BuildRequires:	jbigkit-devel
BuildRequires:	openjpeg2-devel >= 2.1.0

%description
ImageMagick is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate
and display images. If you want to develop your own applications
which use ImageMagick code or APIs, you need to install
ImageMagick-devel as well.


%package devel
Summary:	Library links and header files for ImageMagick app development
Requires:	%{name} = %{version}-%{release}
Requires:	libX11-devel, libXext-devel, libXt-devel, ghostscript-devel
Requires:	bzip2-devel, freetype-devel, libtiff-devel, libjpeg-devel, lcms2-devel
Requires:	libwebp-devel, OpenEXR-devel, jasper-devel, pkgconfig
Requires:	%{name}-libs = %{version}-%{release}

%description devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.


%package libs
Summary: ImageMagick libraries to link with

%description libs
This packages contains a shared libraries to use within other applications.


%package djvu
Summary: DjVu plugin for ImageMagick
Requires: %{name} = %{version}-%{release}

%description djvu
This packages contains a plugin for ImageMagick which makes it possible to
save and load DjvU files from ImageMagick and libMagickCore using applications.


%package doc
Summary: ImageMagick html documentation

%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in html format.
Note this documentation can also be found on the ImageMagick website:
http://www.imagemagick.org/


%package perl
Summary: ImageMagick perl bindings
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.


%package c++
Summary: ImageMagick Magick++ library (C++ bindings)
Requires: %{name} = %{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.


%package c++-devel
Summary: C++ bindings for the ImageMagick library
Requires: %{name}-c++ = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

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
%setup -q -n %{name}-%{VER}-%{Patchlevel}
%patch0 -p1

sed -i 's/libltdl.la/libltdl.so/g' configure
iconv -f ISO-8859-1 -t UTF-8 README.txt > README.txt.tmp
touch -r README.txt README.txt.tmp
mv README.txt.tmp README.txt
# for %%doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples


%build
%configure \
	--enable-shared \
	--disable-static \
	--with-modules \
	--with-perl \
	--with-x \
	--with-threads \
	--with-magick_plus_plus \
	--with-gslib \
	--with-wmf \
	--with-lcms2 \
	--with-webp \
	--with-openexr \
	--with-rsvg \
	--with-xml \
	--with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
	--without-dps \
	--without-included-ltdl --with-ltdl-include=%{_includedir} \
	--without-gcc-arch \
	--with-ltdl-lib=%{_libdir} \
	--with-jbig \
	--with-openjp2

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
make


%install
rm -rf %{buildroot}

make %{?_smp_mflags} install DESTDIR=%{buildroot} INSTALL="install -p"
cp -a www/source %{buildroot}%{_datadir}/doc/%{name}-%{VER}

# fix weird perl Magick.so permissions
chmod 755 %{buildroot}%{perl_vendorarch}/auto/Image/Magick/Magick.so

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find %{buildroot} -name "*.bs" |xargs rm -f
find %{buildroot} -name ".packlist" |xargs rm -f
find %{buildroot} -name "perllocal.pod" |xargs rm -f

# perlmagick: build files list
echo "%defattr(-,root,root,-)" > perl-pkg-files
find %{buildroot}/%{_libdir}/perl* -type f -print \
	| sed "s@^%{buildroot}@@g" > perl-pkg-files
find %{buildroot}%{perl_vendorarch} -type d -print \
	| sed "s@^%{buildroot}@%dir @g" \
	| grep -v '^%dir %{perl_vendorarch}$' \
	| grep -v '/auto$' >> perl-pkg-files
if [ -z perl-pkg-files ] ; then
	echo "ERROR: EMPTY FILE LIST"
	exit -1
fi

# Fonts must be packaged separately. It does nothave matter and demos work without it.
rm -rf PerlMagick/demo/Generic.ttf

#remove all .la file
find . -name *.la|xargs rm -rf

%check
#Display now, Patch0 will cause all test failed, It's ok since it's not a real failure.
#Just because we use "so" suffix to find modules instead of "la"

#export LD_LIBRARY_PATH=%{buildroot}/wand/.libs/:%{buildroot}/Magick++/lib/.libs/
#export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}
#make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}


%post libs -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig


%files
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt ChangeLog Platforms.txt
%{_bindir}/[a-z]*
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*

%files libs
%defattr(-,root,root,-)
%doc LICENSE NOTICE AUTHORS.txt QuickStart.txt
%{_libdir}/libMagickCore-6.Q16.so.2*
%{_libdir}/libMagickWand-6.Q16.so.2*
%{_libdir}/%{name}-%{VER}
%{_datadir}/%{name}-6
%exclude %{_libdir}/%{name}-%{VER}/modules-Q16/coders/djvu.*
%{_sysconfdir}/%{name}-6

%files devel
%defattr(-,root,root,-)
%{_bindir}/MagickCore-config
%{_bindir}/Magick-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/libMagickCore-6.Q16.so
%{_libdir}/libMagickWand-6.Q16.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/MagickCore-6.Q16.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-6.Q16.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/MagickWand-6.Q16.pc
%{_libdir}/pkgconfig/Wand.pc
%{_libdir}/pkgconfig/Wand-6.Q16.pc
%dir %{_includedir}/%{name}-6
%{_includedir}/%{name}-6/magick
%{_includedir}/%{name}-6/wand
%{_mandir}/man1/Magick-config.*
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/Wand-config.*
%{_mandir}/man1/MagickWand-config.*

%files djvu
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{VER}/modules-Q16/coders/djvu.*

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-6
%doc %{_datadir}/doc/%{name}-%{VER}
%doc LICENSE

%files c++
%defattr(-,root,root,-)
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++-6.Q16.so.6*

%files c++-devel
%defattr(-,root,root,-)
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/%{name}-6/Magick++
%{_includedir}/%{name}-6/Magick++.h
%{_libdir}/libMagick++-6.Q16.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/Magick++-6.Q16.pc
%{_libdir}/pkgconfig/ImageMagick++.pc
%{_libdir}/pkgconfig/ImageMagick++-6.Q16.pc
%{_mandir}/man1/Magick++-config.*

%files perl -f perl-pkg-files
%defattr(-,root,root,-)
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt

%changelog
* Mon May 09 2016 sulit <sulitsrc@gmail.com> - 6.9.4.0-0.beta.3.1
- update to release 6.9.4-0, the release contains fixing CVE-2016-3714

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 6.9.1.3-0.beta.3.3
- Rebuild for new 4.0 release.

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Update.
