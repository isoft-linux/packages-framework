Name:           cmocka
Version:        1.0.1
Release:        2%{?dist}

License:        ASL 2.0
Group:          Development/Tools
Summary:        Lightweight library to simplify and generalize unit tests for C
Url:            http://cmocka.org

Source0:        https://open.cryptomilk.org/attachments/download/54/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  glibc-devel


%description
There are a variety of C unit testing frameworks available however many of them
are fairly complex and require the latest compiler technology. Some development
requires the use of old compilers which makes it difficult to use some unit
testing frameworks. In addition many unit testing frameworks assume the code
being tested is an application or module that is targeted to the same platform
that will ultimately execute the test. Because of this assumption many
frameworks require the inclusion of standard C library headers in the code
module being tested which may collide with the custom or incomplete
implementation of the C library utilized by the code under test.

Cmocka only requires a test application is linked with the standard C library
which minimizes conflicts with standard C library headers. Also, CMocka tries
to avoid the use of some of the newer features of C compilers.

This results in CMocka being a relatively small library that can be used to
test a variety of exotic code. If a developer wishes to simply test an
application with the latest compiler then other unit testing frameworks may be
preferable.

This is the successor of Google's Cmockery.

%package -n libcmocka
Group:          Development/Libraries
Summary:        Lightweight library to simplify and generalize unit tests for C

Conflicts: cmockery2

%description -n libcmocka
There are a variety of C unit testing frameworks available however many of them
are fairly complex and require the latest compiler technology. Some development
requires the use of old compilers which makes it difficult to use some unit
testing frameworks. In addition many unit testing frameworks assume the code
being tested is an application or module that is targeted to the same platform
that will ultimately execute the test. Because of this assumption many
frameworks require the inclusion of standard C library headers in the code
module being tested which may collide with the custom or incomplete
implementation of the C library utilized by the code under test.

CMocka only requires a test application is linked with the standard C library
which minimizes conflicts with standard C library headers. Also, CMocka tries
to avoid the use of some of the newer features of C compilers.

This results in CMocka being a relatively small library that can be used to
test a variety of exotic code. If a developer wishes to simply test an
application with the latest compiler then other unit testing frameworks may be
preferable.

This is the successor of Google's Cmockery.

%package -n libcmocka-static
Group:          Development/Libraries
Summary:        Lightweight library to simplify and generalize unit tests for C

%description -n libcmocka-static
Static version of the cmocka library.

%package -n libcmocka-devel
Group:          Development/Libraries
Summary:        Development headers for the cmocka library
Requires:       libcmocka = %{version}-%{release}

Conflicts: cmockery2-devel

%description -n libcmocka-devel
Development headers for the cmocka unit testing library.

%prep
%setup -q

%build
if test ! -e "obj"; then
  mkdir obj
fi
pushd obj
%cmake \
  -DWITH_STATIC_LIB=ON \
  -DWITH_CMOCKERY_SUPPORT=ON \
  -DUNIT_TESTING=ON \
  %{_builddir}/%{name}-%{version}

make %{?_smp_mflags} VERBOSE=1
make doc
popd

%install
pushd obj
make DESTDIR=%{buildroot} install
popd
ln -s libcmocka.so %{buildroot}%{_libdir}/libcmockery.so

%post -n libcmocka -p /sbin/ldconfig

%postun -n libcmocka -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%check
pushd obj
make test || cat Testing/Temporary/LastTest.log
popd

%files -n libcmocka
%doc AUTHORS README ChangeLog COPYING
%{_libdir}/libcmocka.so.*

%files -n libcmocka-static
%{_libdir}/libcmocka.a

%files -n libcmocka-devel
%doc obj/doc/html
%{_includedir}/cmocka.h
%{_includedir}/cmocka_pbc.h
%{_includedir}/cmockery/cmockery.h
%{_includedir}/cmockery/pbc.h
%{_libdir}/libcmocka.so
%{_libdir}/libcmockery.so
%{_libdir}/pkgconfig/cmocka.pc
%{_libdir}/cmake/cmocka/cmocka-config-version.cmake
%{_libdir}/cmake/cmocka/cmocka-config.cmake

%changelog
