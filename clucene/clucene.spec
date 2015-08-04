Summary:	A C++ port of Lucene
Name:		clucene
Version:	2.3.3.4
Release:	10
License:	LGPLv2+ or ASL 2.0
Group:		Development/System
URL:		http://www.sourceforge.net/projects/clucene
Source0:	http://downloads.sourceforge.net/clucene/clucene-core-%{version}.tar.gz
BuildRequires:	gawk cmake zlib-devel boost-devel

Patch50: clucene-core-2.3.3.4-pkgconfig.patch
Patch51: clucene-core-2.3.3.4-install_contribs_lib.patch  
Patch100: clucene-core-test-build.patch
%description
CLucene is a C++ port of the popular Apache Lucene search engine
(http://lucene.apache.org/java). 
CLucene aims to be a high-speed alternative to Java Lucene, its API is very
similar to that of the Java version. CLucene has recently been brought up to
date with Lucene 2.3.2. It contains most of the same functionality as the Java version.

%package core
Summary:	Core clucene module
Group:		Development/System
Provides:	clucene = %{version}-%{release}
#Requires: %{name} = %{version}-%{release}
%description core
CLucene is a C++ port of the popular Apache Lucene search engine
(http://lucene.apache.org/java).
CLucene aims to be a high-speed alternative to Java Lucene, its API is very
similar to that of the Java version. CLucene has recently been brought up to
date with Lucene 2.3.2. It contains most of the same functionality as the Java version.

%package core-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Libraries
Requires:	%{name}-core = %{version}-%{release}
Requires:	%{name}-contribs-lib = %{version}-%{release}
%description core-devel
This package contains the libraries and header files needed for
developing with clucene

%package contribs-lib
Summary:	Language specific text analyzers for %{name}
Group:  	Development/System
Requires:	%{name}-core = %{version}-%{release}
%description contribs-lib
%{summary}.


%prep
%setup -n %{name}-core-%{version}

%patch50 -p1 -b .pkgconfig
%patch51 -p1 -b .install_contribs_lib
%patch100 -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DBUILD_CONTRIBS_LIB=BOOL:ON \
  -DLIB_DESTINATION:PATH=%{_libdir} \
  -DLUCENE_SYS_INCLUDES:PATH=%{_libdir} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

rm -rf %{buildroot}%{_libdir}/CLuceneConfig.cmake


%check
# FIXME: do not run tests for ppc and s390 (big endian 32 bit archs) until
# we have a proper fix
#%ifnarch ppc s390
# Fails on all arches at the moment so temporaily disable
#make cl_test -C %{_target_platform}
#make test -C %{_target_platform}
#%endif


%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%files core
%defattr(-, root, root, -)
%doc APACHE.license AUTHORS ChangeLog COPYING LGPL.license README
%{_libdir}/libclucene-core.so.1*
%{_libdir}/libclucene-core.so.%{version}
%{_libdir}/libclucene-shared.so.1*
%{_libdir}/libclucene-shared.so.%{version}

%post contribs-lib -p /sbin/ldconfig
%postun contribs-lib -p /sbin/ldconfig

%files contribs-lib
%defattr(-, root, root, -)
%{_libdir}/libclucene-contribs-lib.so.1*
%{_libdir}/libclucene-contribs-lib.so.%{version}

%files core-devel
%defattr(-, root, root, -)
%dir %{_libdir}/CLucene
%{_includedir}/CLucene/
%{_includedir}/CLucene.h
%{_libdir}/libclucene*.so
%{_libdir}/CLucene/clucene-config.h
%{_libdir}/CLucene/CLuceneConfig.cmake
%{_libdir}/pkgconfig/libclucene-core.pc


%changelog
