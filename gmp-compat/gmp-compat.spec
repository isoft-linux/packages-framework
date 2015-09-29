Name: gmp-compat 
Version: 4.3.2
Release: 1
Summary: Compatible gmp library 

License: LGPL 
URL: http://gmplib.org/
Source0: https://gmplib.org/download/gmp/gmp-%{version}.tar.xz
#https://gmplib.org/repo/gmp/rev/966737bd91ed
Patch0: gmp-fix-t-scan-test.patch

BuildRequires: gcc glibc-devel	

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

This is the compatible library package.

%prep
%setup -q -n gmp-%{version}
%patch0 -p1

%build
if as --help | grep -q execstack; then
  # the object files do not require an executable stack
  export CCAS="gcc -c -Wa,--noexecstack"
fi

mkdir base
cd base
ln -s ../configure .
%configure
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
cd base
export LD_LIBRARY_PATH=`pwd`/.libs
make install DESTDIR=$RPM_BUILD_ROOT
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{gmp,mp,gmpxx}.la
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
cd ..

#it's a compatible package, do not ship headers and devel libraries.
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}/*.so
rm -rf %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_infodir}

%check
%ifnarch ppc
cd base
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags} check
cd ..
%endif


%files
%{_libdir}/libgmp.so.*

%changelog
* Wed Aug 05 2015 Cjacker <cjacker@foxmail.com>
- initial build.
