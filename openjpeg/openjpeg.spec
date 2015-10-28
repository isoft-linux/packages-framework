%define cmake_build 1

Name:    openjpeg
Version: 1.5.2
Release: 7 
Summary: JPEG 2000 command line tools

License: BSD
URL:     http://www.openjpeg.org
Source0: http://openjpeg.googlecode.com/files/openjpeg-version.%{version}.tar.gz
%if 0%{?runcheck}
# svn checkout http://openjpeg.googlecode.com/svn/data
Source1: data.tar.xz
%endif

# revert soname bump compared to 1.5.0 release (for now)
Patch1: openjpeg-1.5.1-soname.patch

## upstreamable patches
Patch50: openjpeg-1.5.1-cmake_libdir.patch

%if 0%{?cmake_build}
BuildRequires: cmake 
%else
BuildRequires: automake libtool 
%endif
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(zlib)

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
OpenJPEG is an open-source JPEG 2000 codec written in C. It has been
developed in order to promote the use of JPEG 2000, the new still-image
compression standard from the Joint Photographic Experts Group (JPEG).

%package libs
Summary: JPEG 2000 codec runtime library
%description libs
The %{name}-libs package contains runtime libraries for applications that use
OpenJPEG.

%package  devel
Summary:  Development files for %{name} 
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use OpenJPEG.

%package  devel-docs
Summary:  Developer documentation for %{name}
BuildArch: noarch
%description devel-docs
%{summary}.


%prep
%setup -q -n openjpeg-version.%{version} %{?runcheck:-a 1}

%patch1 -p1 -b .soname
%if 0%{?cmake_build}
%patch50 -p1 -b .cmake_libdir
%else
autoreconf -i -f
%endif

%build

%{?runcheck:export OPJ_DATA_ROOT=$(pwd)/data}

%if 0%{?cmake_build}
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DBUILD_DOC:BOOL=OFF \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  %{?runcheck:-DBUILD_TESTING:BOOL=ON} \
  -DCMAKE_BUILD_TYPE=Release \
  -DOPENJPEG_INSTALL_LIB_DIR:PATH=%{_lib} \
   ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%else
%configure \
  --enable-shared \
  --disable-static

make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

%if 0%{?cmake_build}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%else
make install DESTDIR=%{buildroot}
%endif

# continue to ship compat header symlink
ln -s openjpeg-1.5/openjpeg.h %{buildroot}%{_includedir}/openjpeg.h

## unpackaged files
# we use %%doc in -libs below instead
rm -rfv %{buildroot}%{_docdir}/openjpeg-1.5/
rm -fv  %{buildroot}%{_libdir}/lib*.la

%check
test -f %{buildroot}%{_includedir}/openjpeg.h
## known failures (on rex's f16/x86_64 box anyway)
%if 0%{?runcheck}
make test -C %{_target_platform}
%endif


%files
%{_bindir}/image_to_j2k
%{_bindir}/j2k_dump
%{_bindir}/j2k_to_image
%{_mandir}/man1/*image_to_j2k.1*
%{_mandir}/man1/*j2k_dump.1*
%{_mandir}/man1/*j2k_to_image.1*

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%doc CHANGES LICENSE 
%{_libdir}/libopenjpeg.so.1*
%{_mandir}/man3/*libopenjpeg.3*

%files devel
%{_includedir}/openjpeg-1.5/
%{_includedir}/openjpeg.h
%{_libdir}/libopenjpeg.so
%{_libdir}/pkgconfig/libopenjpeg.pc
%{_libdir}/pkgconfig/libopenjpeg1.pc
%if 0%{?cmake_build}
%{_libdir}/openjpeg-1.5/
%endif

#files devel-docs
#%doc %{?cmake_build:%{_target_platform}/}doc/html/


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.5.2-7
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

