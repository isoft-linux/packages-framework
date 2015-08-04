%define ver 58
%define sonamever 9 
Name: boost
Summary: The Boost C++ Libraries
Version: 1.%{ver}.0 
Release: 2 
License: Boost
URL: http://www.boost.org/
Group: System Environment/Libraries
Source: boost_1_%{ver}_0.tar.gz

Provides: boost-doc = %{version}-%{release}

BuildRequires: libcxx-devel
BuildRequires: bzip2-libs
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
BuildRequires: python-devel
BuildRequires: libicu-devel
BuildRequires: chrpath


Patch1: boost-graph-compile.patch
Patch2: boost-1.41.0-mapnik.patch
Patch3: boost-1.41.0-shared_ptr_serialization.patch

%bcond_with tests
%bcond_with docs_generated

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been proposed for inclusion in the C++
Standards Committee's upcoming C++ Standard Library Technical Report.)

%package devel
Summary: The Boost C++ headers and shared development libraries
Group: Development/Libraries
Requires: boost = %{version}-%{release}
Provides: boost-python-devel = %{version}-%{release}

%description devel
Headers and shared object symlinks for the Boost C++ libraries.

%package static
Summary: The Boost C++ static development libraries
Group: Development/Libraries
Requires: boost-devel = %{version}-%{release}
Obsoletes: boost-devel-static < 1.34.1-14
Provides: boost-devel-static = %{version}-%{release}

%description static
Static Boost C++ libraries.

%package doc
Summary: The Boost C++ html docs
Group: Documentation
Provides: boost-python-docs = %{version}-%{release}

%description doc
HTML documentation files for Boost C++ libraries.

%prep
%setup -q -n %{name}_1_%{ver}_0
%build
export CC=clang
export CXX=clang++

BOOST_ROOT=`pwd`
export BOOST_ROOT

./bootstrap.sh --with-toolset=clang
BJAM=./bjam

CONFIGURE_FLAGS="--with-toolset=clang"
PYTHON_VERSION=$(python -c 'import sys; print sys.version[:3]')
PYTHON_FLAGS="--with-python-root=/usr --with-python-version=$PYTHON_VERSION"
REGEX_FLAGS="--with-icu"
./bootstrap.sh $CONFIGURE_FLAGS $PYTHON_FLAGS $REGEX_FLAGS

BUILD_VARIANTS="variant=release threading=single,multi debug-symbols=on"
BUILD_FLAGS="-d2 --layout=tagged $BUILD_VARIANTS --without-mpi cflags=-fno-strict-aliasing"
$BJAM $BUILD_FLAGS %{?_smp_mflags} stage 

# build docs, requires a network connection for docbook XSLT stylesheets
%if %{with docs_generated}
cd ./doc
chmod +x ../tools/boostbook/setup_boostbook.sh
../tools/boostbook/setup_boostbook.sh
USER_CFG=$BOOST_ROOT/tools/build/v2/user-config.jam
$BOOST_ROOT/$BJAM --v2 -sICU_PATH=/usr --user-config=$USER_CFG html
cd ..
%endif

#%check
#%if %{with tests}
#echo "<p>" `uname -a` "</p>" > status/regression_comment.html
#echo "" >> status/regression_comment.html
#echo "<p>" `g++ --version` "</p>" >> status/regression_comment.html
#echo "" >> status/regression_comment.html
#
#cd tools/regression/build
##$BOOST_ROOT/$BJAM
#cd ../test
##python ./test.py
#cd ../../..
#
#results1=status/cs-`uname`.html
#results2=status/cs-`uname`-links.html
#email=benjamin.kosnik@gmail.com
#if [ -f $results1 ] && [ -f $results2 ]; then
#  echo "sending results starting"
#  testdate=`date +%Y%m%d`
#  testarch=`uname -m`
#  results=boost-results-$testdate-$testarch.tar.bz2
#  tar -cvf boost-results-$testdate-$testarch.tar $results1 $results2
#  bzip2 -f boost-results-$testdate-$testarch.tar 
#  echo | mutt -s "$testdate boost regression $testarch" -a $results $email 
#  echo "sending results finished"
#else
#  echo "error sending results"
#fi
#%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# install lib
for i in `find stage -type f -name \*.a`; do
  NAME=`basename $i`;
  install -p -m 0644 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
done;


for i in `find stage -type f -name \*.so.*`; do
    NAME=`basename $i .%{version}`;
    mv $i stage/lib/$NAME;
done

for i in `find stage -type f -name \*.so`; do
  NAME=$i;
  SONAME=$i.%{sonamever};
  VNAME=$i.%{version};
  base=`basename $i`;
  NAMEbase=$base;
  SONAMEbase=$base.%{sonamever};
  VNAMEbase=$base.%{version};
  mv $i $VNAME;

  # remove rpath
  chrpath --delete $VNAME;

  ln -s $VNAMEbase $SONAME;
  ln -s $VNAMEbase $NAME;
  install -p -m 755 $VNAME $RPM_BUILD_ROOT%{_libdir}/$VNAMEbase; 

  mv $SONAME $RPM_BUILD_ROOT%{_libdir}/$SONAMEbase;
  mv $NAME $RPM_BUILD_ROOT%{_libdir}/$NAMEbase;
done;

# install include files
find %{name} -type d | while read a; do
  mkdir -p $RPM_BUILD_ROOT%{_includedir}/$a
  find $a -mindepth 1 -maxdepth 1 -type f \
  | xargs -r install -m 644 -p -t $RPM_BUILD_ROOT%{_includedir}/$a
done

# install doc files
DOCPATH=$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
find libs doc more -type f \( -name \*.htm -o -name \*.html \) \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories
sed "s:^:$DOCPATH:" tmp-doc-directories | xargs -r mkdir -p
cat tmp-doc-directories | while read a; do
    find $a -mindepth 1 -maxdepth 1 -name \*.htm\* \
    | xargs install -m 644 -p -t $DOCPATH$a
done
rm tmp-doc-directories
install -p -m 644 -t $DOCPATH LICENSE_1_0.txt index.htm

# remove scripts used to generate include files
find $RPM_BUILD_ROOT%{_includedir}/ \( -name '*.pl' -o -name '*.sh' \) -exec rm {} \;

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%{_libdir}/*.so.*

#%files date-time
#%defattr(-, root, root, -)
#%{_libdir}/libboost_date_time*.so.%{version}
#%{_libdir}/libboost_date_time*.so.%{sonamever}
#
#%files filesystem
#%defattr(-, root, root, -)
#%{_libdir}/libboost_filesystem*.so.%{version}
#%{_libdir}/libboost_filesystem*.so.%{sonamever}
#
#%files graph
#%defattr(-, root, root, -)
#%{_libdir}/libboost_graph*.so.%{version}
#%{_libdir}/libboost_graph*.so.%{sonamever}
#
#%files iostreams
#%defattr(-, root, root, -)
#%{_libdir}/libboost_iostreams*.so.%{version}
#%{_libdir}/libboost_iostreams*.so.%{sonamever}
#
#%files math
#%defattr(-, root, root, -)
#%{_libdir}/libboost_math*.so.%{version}
#%{_libdir}/libboost_math*.so.%{sonamever}
#
#%files test
#%defattr(-, root, root, -)
#%{_libdir}/libboost_prg_exec_monitor*.so.%{version}
#%{_libdir}/libboost_prg_exec_monitor*.so.%{sonamever}
#%{_libdir}/libboost_unit_test_framework*.so.%{version}
#%{_libdir}/libboost_unit_test_framework*.so.%{sonamever}
#
#%files program-options
#%defattr(-, root, root, -)
#%{_libdir}/libboost_program_options*.so.%{version}
#%{_libdir}/libboost_program_options*.so.%{sonamever}
#
#%files python
#%defattr(-, root, root, -)
#%{_libdir}/libboost_python*.so.%{version}
#%{_libdir}/libboost_python*.so.%{sonamever}
#
#%files regex
#%defattr(-, root, root, -)
#%{_libdir}/libboost_regex*.so.%{version}
#%{_libdir}/libboost_regex*.so.%{sonamever}
#
#%files serialization
#%defattr(-, root, root, -)
#%{_libdir}/libboost_serialization*.so.%{version}
#%{_libdir}/libboost_serialization*.so.%{sonamever}
#%{_libdir}/libboost_wserialization*.so.%{version}
#%{_libdir}/libboost_wserialization*.so.%{sonamever}
#
#%files signals
#%defattr(-, root, root, -)
#%{_libdir}/libboost_signals*.so.%{version}
#%{_libdir}/libboost_signals*.so.%{sonamever}
#
#%files random 
#%defattr(-, root, root, -)
#%{_libdir}/libboost_random*.so.%{version}
#%{_libdir}/libboost_random*.so.%{sonamever}
#
#%files system
#%defattr(-, root, root, -)
#%{_libdir}/libboost_system*.so.%{version}
#%{_libdir}/libboost_system*.so.%{sonamever}
#
#%files thread
#%defattr(-, root, root, -)
#%{_libdir}/libboost_thread*.so.%{version}
#%{_libdir}/libboost_thread*.so.%{sonamever}
#
#%files wave
#%defattr(-, root, root, -)
#%{_libdir}/libboost_wave*.so.%{version}
#%{_libdir}/libboost_wave*.so.%{sonamever}

%files doc
%defattr(-, root, root, -)
%doc %{_docdir}/%{name}-%{version}

%files devel
%defattr(-, root, root, -)
%{_includedir}/boost
%{_libdir}/*.so

%files static
%defattr(-, root, root, -)
%{_libdir}/*.a

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

