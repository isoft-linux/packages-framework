Name: libicns
Version: 0.8.1
Release: 7%{?dist}
Summary: Library for manipulating Macintosh icns files

# libicns, icns2png and icontainer2icns are under LGPLv2+
# png2icns is under GPLv2+
License: LGPLv2+ and GPLv2+
URL: http://icns.sourceforge.net/
Source0: http://downloads.sourceforge.net/icns/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libpng-devel
BuildRequires: jasper-devel

%description
libicns is a library providing functionality for easily reading and 
writing Macintosh icns files


%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package utils
Summary: Utilities for %{name}
Requires: %{name} = %{version}-%{release}

%description utils
icns2png - convert Mac OS icns files to png images
png2icns - convert png images to Mac OS icns files
icontainer2icns - extract icns files from icontainers 

%prep
%setup -q


%build
%configure --disable-static

# disable rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LGPL-2 COPYING.LGPL-2.1 NEWS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc src/apidocs.*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%doc README


%changelog
* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- initial build.
