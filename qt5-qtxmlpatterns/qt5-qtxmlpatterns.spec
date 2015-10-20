Name: qt5-qtxmlpatterns
Version: 5.5.1
Release: 2 
Summary: QtXmlpatterns component

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtxmlpatterns-opensource-src-%{version}.tar.xz 

BuildRequires: qt5-qtbase-devel >= %{version}

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools
#for absolute path qdoc
BuildRequires: qt5-qtbase


%description
QtXmlpatterns component

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt5-qtbase-devel >= %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtxmlpatterns-opensource-src-%{version}

%build
qmake-qt5

make %{?_smp_mflags}
make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}


# put non-conflicting binaries with -qt5 postfix in %{_bindir}
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
 case "${i}" in
 xmlpatterns|xmlpatternsvalidator)
 ln -v ${i} %{buildroot}%{_bindir}/${i}-qt5
 ln -sv ${i} ${i}-qt5
 ;;
 *)
 ln -v ${i} %{buildroot}%{_bindir}/${i}
 ;;
 esac
done
popd


#fake debug library
pushd %{buildroot}%{_qt5_libdir}
for lib in libQt*.so ; do
 ln -s $lib $(basename $lib .so)_debug.so
done
popd

if [ -d "examples/" ]; then
 mkdir -p %{buildroot}%{_libdir}/qt5/examples
 cp -r examples/* %{buildroot}%{_libdir}/qt5/examples/
 rm -rf %{buildroot}%{_libdir}/qt5/examples/*.pro
fi


%files
%{_libdir}/*.so.*

%files devel
%{_libdir}/cmake/Qt5XmlPatterns
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/pkgconfig/Qt5XmlPatterns.pc
%{_libdir}/qt5/bin/xmlpatterns*
%{_bindir}/xmlpatterns*
%{_libdir}/qt5/examples/xmlpatterns
%{_libdir}/qt5/include/QtXmlPatterns
%{_libdir}/qt5/mkspecs/modules/qt_lib_xmlpatterns.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_xmlpatterns_private.pri
%{_docdir}/qt5/*

%changelog
* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

