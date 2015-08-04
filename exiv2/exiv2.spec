## enable experimental cmake build support (or not)
## still lacks some features, like visibility
#define cmake_build 1

Summary: Exif and Iptc metadata manipulation library
Name:	 exiv2
Version: 0.25
Release: 1

License: GPLv2+
URL: 	 http://www.exiv2.org/
Source0: http://www.exiv2.org/exiv2-%{version}%{?pre:-%{pre}}.tar.gz

## upstream patches

## upstreamable patches
# support LIB_SUFFIX, and avoid hard-coded rpath while we're at it
Patch50: exiv2-0.25-cmake_LIB_SUFFIX.patch
Patch51: exiv2-0.24-cmake_mandir.patch
Patch52: exiv2-0.24-doxygen_config.patch

%if 0%{?cmake_build}
BuildRequires: cmake
%endif
BuildRequires: expat-devel
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: zlib-devel
# docs
BuildRequires: doxygen graphviz libxslt

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
A command line utility to access image metadata, allowing one to:
* print the Exif metadata of Jpeg images as summary info, interpreted values,
  or the plain data for each tag
* print the Iptc metadata of Jpeg images
* print the Jpeg comment of Jpeg images
* set, add and delete Exif and Iptc metadata of Jpeg images
* adjust the Exif timestamp (that's how it all started...)
* rename Exif image files according to the Exif timestamp
* extract, insert and delete Exif metadata (including thumbnails),
  Iptc metadata and Jpeg comments

%package devel
Summary: Header files, libraries and development documentation for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package libs
Summary: Exif and Iptc metadata manipulation library
%description libs
A C++ library to access image metadata, supporting full read and write access
to the Exif and Iptc metadata, Exif MakerNote support, extract and delete 
methods for Exif thumbnails, classes to access Ifd and so on.

%package doc
Summary: Api documentation for %{name}
BuildArch: noarch
%description doc
%{summary}.


%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}

%patch50 -p1 -b .cmake_LIB_SUFFIX
%patch51 -p1 -b .cmake_mandir
%patch52 -p1 -b .doxygen_config


%build
%if 0%{?cmake_build}
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DEXIV2_ENABLE_BUILD_PO:BOOL=ON \
  -DEXIV2_ENABLE_BUILD_SAMPLES:BOOL=OFF \
  ..

make %{?_smp_mflags}
make doc -k ||:
popd
%else
%configure \
  --disable-rpath \
  --disable-static 

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
make doc -k ||:
%endif


%install
%if 0%{?cmake_build}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%else
make install DESTDIR=%{buildroot}

## fix perms on installed lib
ls -l     %{buildroot}%{_libdir}/libexiv2.so.*
chmod 755 %{buildroot}%{_libdir}/libexiv2.so.*
%endif

%find_lang exiv2

## unpackaged files
rm -fv %{buildroot}%{_libdir}/pkgconfig/exiv2.lsm
rm -fv %{buildroot}%{_libdir}/libexiv2.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion exiv2)" = "%{version}"
test -x %{buildroot}%{_libdir}/libexiv2.so


%files 
%doc COPYING README
%{_bindir}/exiv2
%{_mandir}/man1/*

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs -f exiv2.lang
%{_libdir}/libexiv2.so.14*

%files devel
%{_includedir}/exiv2/
%{_libdir}/libexiv2.so
%{_libdir}/pkgconfig/exiv2.pc

%files doc
%doc doc/html


%changelog
