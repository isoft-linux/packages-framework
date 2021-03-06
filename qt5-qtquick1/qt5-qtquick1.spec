Name: qt5-qtquick1
Version: 5.5.1
Release: 3 
Summary: QtQuick1 component

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtquick1-opensource-src-%{version}.tar.xz 

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtscript-devel >= %{version}
BuildRequires: qt5-qttools-devel >= %{version}
BuildRequires: qt5-qtxmlpatterns-devel >= %{version}
BuildRequires: qt5-qtwebkit-devel >= %{version}


#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools-devel
#for absolute path qdoc
BuildRequires: qt5-qtbase-devel

%description
QtQuick1 component

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt5-qtbase-devel >= %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtquick1-opensource-src-%{version}

%build
qmake-qt5

make %{?_smp_mflags}
make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}


# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
 case "${i}" in
 # qt4 conflicts
 qmlviewer)
 ln -v ${i} %{buildroot}%{_bindir}/${i}-qt5
 ln -sv ${i} ${i}-qt5
 ;;
 # stuff handled by qtchooser
 qml1plugindump)
 ln -v ${i} %{buildroot}%{_bindir}/${i}
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
%{_libdir}/qt5/imports/*
%{_libdir}/qt5/plugins/*

%files devel
%{_libdir}/cmake/*
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/qt5/examples/*
%{_libdir}/qt5/include/*
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_libdir}/qt5/bin/qml1plugindump*
%{_libdir}/qt5/bin/qmlviewer*
%{_bindir}/qml1plugindump*
%{_bindir}/qmlviewer*

#%{_docdir}/qt5/*

%changelog
* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

