Name: qt5-qttools 
Version: 5.6.0
Release: 2
Summary: Various tools of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qttools-opensource-src-%{version}.tar.xz 
#call qmake-qt5, not qmake directly.
Patch0: qttools-opensource-src-5.2.0-qmake-qt5.patch

BuildRequires: qt5-qtbase-devel
#>= %{version}
BuildRequires: qt5-qtwebkit-devel
#>= %{version}
BuildRequires: qt5-qtdeclarative-devel
#>= %{version}

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools-devel
#for absolute path qdoc
BuildRequires: qt5-qtbase-devel


%description
Various tools of Qt

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt5-qtbase-devel >= %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qttools-opensource-src-%{version}
%patch0 -p1

%build
qmake-qt5
make %{?_smp_mflags}
#make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}

# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
 case "${i}" in
 assistant|designer|lconvert|linguist|lrelease|lupdate|pixeltool|qcollectiongenerator|qdbus|qdbusviewer|qhelpconverter|qhelpgenerator)
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
for lib in libQt*.a ; do
 ln -s $lib $(basename $lib .a)_debug.a
done
popd

if [ -d "examples/" ]; then
 mkdir -p %{buildroot}%{_libdir}/qt5/examples
 cp -r examples/* %{buildroot}%{_libdir}/qt5/examples/
 rm -rf %{buildroot}%{_libdir}/qt5/examples/*.pro
fi


%files
%{_bindir}/qdbus*
%{_bindir}/qtplugininfo
%{_libdir}/qt5/bin/qtplugininfo
%{_libdir}/qt5/bin/qdbus*
%{_libdir}/qt5/bin/qdbusviewer*
%{_libdir}/*.so.*
%{_libdir}/qt5/plugins/designer/*.so
%{_datadir}/qt5/phrasebooks/*.qph

%files devel
%{_bindir}/*
%{_libdir}/qt5/bin/assistant*
%{_libdir}/qt5/bin/designer*
%{_libdir}/qt5/bin/lconvert*
%{_libdir}/qt5/bin/linguist*
%{_libdir}/qt5/bin/lrelease*
%{_libdir}/qt5/bin/lupdate*
%{_libdir}/qt5/bin/pixeltool*
%{_libdir}/qt5/bin/qcollectiongenerator*
%{_libdir}/qt5/bin/qhelpconverter*
%{_libdir}/qt5/bin/qhelpgenerator*
%{_libdir}/qt5/bin/qtdiag
%{_libdir}/qt5/bin/qtpaths
%{_libdir}/cmake/*
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_libdir}/qt5/examples/*
%{_libdir}/qt5/include/*
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_docdir}/qt5/*
%exclude %{_bindir}/qdbus*

%changelog
* Thu Mar 24 2016 <sulit> <sulitsrc@gmail.com> - 5.6.0-2
- modify buildrequire and comment the make doc

* Thu Mar 24 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-1
- Release 5.6.0

* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

