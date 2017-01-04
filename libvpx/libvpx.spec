Name: libvpx
Summary: VP8 Video Codec SDK
Version: 1.6.0
Release: 1
License: BSD
Source0: http://webm.googlecode.com/files/%{name}-%{version}.tar.bz2
Patch0: libvpx-do-NOT-use-clang-integrated-as.patch

URL: http://www.webmproject.org/tools/
%ifarch %{ix86} x86_64
BuildRequires: yasm
%endif
BuildRequires: gcc

%description
libvpx provides the VP8 SDK, which allows you to integrate your applications 
with the VP8 video codec, a high quality, royalty free, open source codec 
deployed on millions of computers and devices worldwide. 

%package devel
Summary: Development files for libvpx
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against 
libvpx.

%package utils
Summary: VP8 utilities and tools
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
A selection of utilities and tools for VP8, including a sample encoder
and decoder.

%prep
%setup -q -n %{name}-%{version}
#clang related
#%patch0 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
./configure \
        --enable-pic \
        --enable-libs \
        --enable-runtime-cpu-detect \
        --enable-vp8 \
        --enable-vp9 \
        --enable-shared \
        --disable-install-srcs \
        --prefix=%{_prefix} --libdir=%{_libdir}

make %{?_smp_mflags} V=1
%install
make DIST_DIR=%{buildroot}%{_prefix} dist

#remove unused file.
rm -rf $RPM_BUILD_ROOT/usr/md5sums.txt
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -rf $RPM_BUILD_ROOT/usr/docs
rm -rf $RPM_BUILD_ROOT/usr/CHANGELOG
rm -rf $RPM_BUILD_ROOT/usr/README


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS CHANGELOG LICENSE README
%{_libdir}/libvpx.so.*

%files devel
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx.so

%files utils
%{_bindir}/*

%changelog
* Wed Jan 04 2017 sulit - 1.6.0-1
- upgrade libvpx to 1.6.0

* Tue Jan 03 2017 sulit - 1.6.0-0
- upgrade libvpx to 1.6.0

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.4.0-3
- Rebuild for new 4.0 release.

