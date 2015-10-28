Name: libmng
Version: 2.0.3
Release: 3%{?dist}
URL: http://www.libmng.com/
Summary: Library for Multiple-image Network Graphics support
# This is a common zlib variant.
License: zlib
Source0: http://download.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: zlib-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: lcms2-devel
BuildRequires: libtool
BuildRequires: autoconf

%package devel
Summary: Development files for the Multiple-image Network Graphics library
Requires: %{name} = %{version}-%{release}
Requires: zlib-devel
Requires: libjpeg-devel

%description
LibMNG is a library for accessing graphics in MNG (Multi-image Network
Graphics) and JNG (JPEG Network Graphics) formats.  MNG graphics are
basically animated PNGs.  JNG graphics are basically JPEG streams
integrated into a PNG chunk.

%description devel
LibMNG is a library for accessing MNG and JNG format graphics.  The
libmng-devel package contains files needed for developing or compiling
applications which use MNG graphics.

%prep
%setup -q

%build
#cp makefiles/configure.in .
cp makefiles/Makefile.am .
#sed -i '/AM_C_PROTOTYPES/d' configure.in
autoreconf -if
%configure --enable-shared --disable-static --with-zlib --with-jpeg \
	--with-gnu-ld --with-lcms2
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc CHANGES LICENSE README*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,0755)
%doc doc/*
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_libdir}/pkgconfig/libmng.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.0.3-3
- Rebuild for new 4.0 release.

