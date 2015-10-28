Name:           atlas
Version:        3.10.2
Release:        9%{?dist}
Summary:        Automatically Tuned Linear Algebra Software

License:        BSD
URL:            http://math-atlas.sourceforge.net/
Source0:        http://downloads.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
# Properly pass -melf_* to the linker with -Wl, fixes FTBFS bug 817552
# https://sourceforge.net/tracker/?func=detail&atid=379484&aid=3555789&group_id=23725
Patch3:		atlas-melf.patch
Patch4:		atlas-throttling.patch
#credits Lukas Slebodnik
Patch5:		atlas-shared_libraries.patch
Patch6:         atlas-affinity.patch
Patch8:         atlas-genparse.patch
Patch9:         atlas.3.10.1-unbundle.patch

BuildRequires:  gcc-gfortran, lapack-static

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

The performance improvements in ATLAS are obtained largely via
compile-time optimizations and tend to be specific to a given hardware
configuration. In order to package ATLAS some compromises
are necessary so that good performance can be obtained on a variety
of hardware. This set of ATLAS binary packages is therefore not
necessarily optimal for any specific hardware configuration.  However,
the source package can be used to compile customized ATLAS packages;
see the documentation for information.

%package devel
Summary:        Development libraries for ATLAS
Requires:       %{name} = %{version}-%{release}
Obsoletes:	%name-header <= %version-%release

%description devel
This package contains headers for development with ATLAS
(Automatically Tuned Linear Algebra Software).

%package static
Summary:        Static libraries for ATLAS
Requires:       %{name}-devel = %{version}-%{release}

%description static
This package contains static version of ATLAS (Automatically Tuned
Linear Algebra Software).

%define types base

%define threads_option -t 4

%ifarch x86_64
%define arch_option -b 64 -A x86SSE2 -V 448
%endif

%ifarch i686
%define arch_option -b 32 -A x86x87 -V 384
%endif

%prep
%setup -q -n ATLAS
%patch3 -p1 -b .melf
%patch4 -p1 -b .thrott
%patch5 -p2 -b .sharedlib
%patch6 -p1
%patch8 -p1
%patch9 -p1

# Generate lapack library
mkdir lapacklib
cd lapacklib
ar x %{_libdir}/liblapack_pic.a
# Remove functions that have ATLAS implementations
rm cgelqf.o cgels.o cgeqlf.o cgeqrf.o cgerqf.o cgesv.o cgetrf.o cgetri.o cgetrs.o clarfb.o clarft.o clauum.o cposv.o cpotrf.o cpotri.o cpotrs.o ctrtri.o dgelqf.o dgels.o dgeqlf.o dgeqrf.o dgerqf.o dgesv.o dgetrf.o dgetri.o dgetrs.o dlamch.o dlarfb.o dlarft.o dlauum.o dposv.o dpotrf.o dpotri.o dpotrs.o dtrtri.o ieeeck.o ilaenv.o lsame.o sgelqf.o sgels.o sgeqlf.o sgeqrf.o sgerqf.o sgesv.o sgetrf.o sgetri.o sgetrs.o slamch.o slarfb.o slarft.o slauum.o sposv.o spotrf.o spotri.o spotrs.o strtri.o xerbla.o zgelqf.o zgels.o zgeqlf.o zgeqrf.o zgerqf.o zgesv.o zgetrf.o zgetri.o zgetrs.o zlarfb.o zlarft.o zlauum.o zposv.o zpotrf.o zpotri.o zpotrs.o ztrtri.o
# Create new library
ar rcs ../liblapack_pic_pruned.a *.o
cd ..

%build
mkdir -p build
pushd build
../configure  %{?arch_option} \
     %{?threads_option} \
     -Fa alg -fPIC -D c -DWALL \
     --prefix=%{buildroot}%{_prefix} \
     --incdir=%{buildroot}%{_includedir} \
     --libdir=%{buildroot}%{_libdir}/atlas
     sed -i "s#SLAPACKlib.*#SLAPACKlib = $(pwd)/../liblapack_pic_pruned.a#" Make.inc

make build

cd lib
make shared
make ptshared
popd

%install
pushd build
make DESTDIR=%{buildroot} install
cp -pr lib/*.so* %{buildroot}%{_libdir}/atlas/
rm -f %{buildroot}%{_libdir}/atlas/*.a
cp -pr lib/libcblas.a lib/libatlas.a lib/libf77blas.a lib/liblapack.a %{buildroot}%{_libdir}/atlas/
popd

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/atlas" > %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}.conf

#create pkgconfig file
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/atlas.pc << DATA
Name: %{name}
Version: %{version}
Description: %{summary}
Cflags: -I%{_includedir}/atlas/
Libs: -L%{_libdir}/atlas/ -lsatlas
DATA

%check
pushd build
make check ptcheck
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%dir %{_libdir}/atlas
%{_libdir}/atlas/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}.conf

%files devel
%{_libdir}/atlas/*.so
%{_includedir}/atlas
%{_includedir}/*.h
%{_libdir}/pkgconfig/atlas.pc

%files static
%{_libdir}/atlas/*.a

%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 3.10.2-9
- Rebuild

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.10.2-8
- Rebuild

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.10.2-7
- Rebuild for new 4.0 release.

