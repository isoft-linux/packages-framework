Summary: Library of functions for manipulating TIFF format image files
Name: libtiff
Version: 4.0.3
Release: 1
License: libtiff
Group: System Environment/Libraries
URL: http://www.libtiff.org/

Source: ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{version}.tar.gz
Patch0: libtiff-CVE-2012-4447.patch
Patch1: libtiff-CVE-2012-4564.patch
Patch2: libtiff-CVE-2013-1960.patch
Patch3: libtiff-CVE-2013-1961.patch
Patch4: tiff-4.0.3-CVE-2013-4231.patch
Patch5: tiff-4.0.3-CVE-2013-4232.patch
Patch6: libtiff-CVE-2013-4243.patch
Patch7: libtiff-CVE-2013-4244.patch

BuildRequires: zlib-devel libjpeg-devel
%define LIBVER %(echo %{version} | cut -f 1-2 -d .)

%description
The libtiff package contains a library of functions for manipulating
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

%package devel
Summary: Development tools for programs which will use the libtiff library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and documentation necessary for
developing programs which will manipulate TIFF format image files
using the libtiff library.

If you need to develop programs which will manipulate TIFF format
image files, you should install this package.  You'll also need to
install the libtiff package.

%package static
Summary: Static TIFF image format file library
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The libtiff-static package contains the statically linkable version of libtiff.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%prep
%setup -q -n tiff-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
#%patch6 -p1
%patch7 -p1

%build
%configure
make %{?_smp_mflags}

LD_LIBRARY_PATH=$PWD:$LD_LIBRARY_PATH make check

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

# remove what we didn't want installed
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/

# no libGL dependency, please
rm -f $RPM_BUILD_ROOT%{_bindir}/tiffgt
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/tiffgt.1
rm -f html/man/tiffgt.1.html

# no sgi2tiff or tiffsv, either
rm -f $RPM_BUILD_ROOT%{_bindir}/sgi2tiff
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/sgi2tiff.1
rm -f html/man/sgi2tiff.1.html
rm -f $RPM_BUILD_ROOT%{_bindir}/tiffsv
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/tiffsv.1
rm -f html/man/tiffsv.1.html

# multilib header hack
# we only apply this to known Red Hat multilib arches, per bug #233091
case `uname -i` in
  i386 | ppc | s390)
    wordsize="32"
    ;;
  x86_64 | ppc64 | s390x)
    wordsize="64"
    ;;
  *)
    wordsize=""
    ;;
esac

if test -n "$wordsize"
then
  mv $RPM_BUILD_ROOT%{_includedir}/tiffconf.h \
     $RPM_BUILD_ROOT%{_includedir}/tiffconf-$wordsize.h

  cat >$RPM_BUILD_ROOT%{_includedir}/tiffconf.h <<EOF
#ifndef TIFFCONF_H_MULTILIB
#define TIFFCONF_H_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "tiffconf-32.h"
#elif __WORDSIZE == 64
# include "tiffconf-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

fi

# don't include documentation Makefiles, they are a multilib hazard
find html -name 'Makefile*' | xargs rm
rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc COPYRIGHT README RELEASE-DATE VERSION
%{_bindir}/*
%{_libdir}/libtiff.so.*
%{_libdir}/libtiffxx.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,0755)
%doc TODO ChangeLog html
%{_includedir}/*
%{_libdir}/libtiff.so
%{_libdir}/libtiffxx.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%files static
%defattr(-,root,root)
%{_libdir}/*.a

%changelog
