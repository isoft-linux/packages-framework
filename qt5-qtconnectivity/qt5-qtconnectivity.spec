Name: qt5-qtconnectivity 
Version: 5.5.1
Release: 4 
Summary: Connectivity Component of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtconnectivity-opensource-src-%{version}.tar.xz 
#QTBUG-48481
Patch0: qtconnectivity-bluetooth-prevent-null.patch

BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: bluez-libs-devel

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools-devel
#for absolute path qdoc
BuildRequires: qt5-qtbase


%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt5-qtbase-devel >= %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtconnectivity-opensource-src-%{version}
%patch0 -p1

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
%{_bindir}/*
%{_libdir}/qt5/bin/*
%{_libdir}/*.so.*
%{_libdir}/qt5/qml/QtBluetooth/libdeclarative_bluetooth.so
%{_libdir}/qt5/qml/QtBluetooth/plugins.qmltypes
%{_libdir}/qt5/qml/QtBluetooth/qmldir
%{_libdir}/qt5/qml/QtNfc/libdeclarative_nfc.so
%{_libdir}/qt5/qml/QtNfc/plugins.qmltypes
%{_libdir}/qt5/qml/QtNfc/qmldir

%files devel
%{_libdir}/cmake/*
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/qt5/examples/*
%{_libdir}/qt5/include/*
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_docdir}/qt5/*

%changelog
* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-4
- fix QTBUG 48481

* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

