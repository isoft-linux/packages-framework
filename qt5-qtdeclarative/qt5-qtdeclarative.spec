Name: qt5-qtdeclarative
Version: 5.7.0
Release: 6
Summary: QtDeclarative component

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtdeclarative-opensource-src-%{version}.tar.xz 

# QTBUG-52340
# https://codereview.qt-project.org/#/c/157520/
Patch0: qtdeclarative-fix-QTBUG-52340.patch

# QTBUG-52057
Patch1: qt5-declarative-gcc6.patch

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtxmlpatterns-devel >= %{version}

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools-devel
#for absolute path qdoc
BuildRequires: qt5-qtbase


%description
QtDeclarative component

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt5-qtbase-devel >= %{version}
Requires: qt5-qtxmlpatterns-devel >= %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtdeclarative-opensource-src-%{version}
%patch0 -p1
%patch1 -p1

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
 qmlplugindump|qmlprofiler)
 ln -v ${i} %{buildroot}%{_bindir}/${i}-qt5
 ln -sv ${i} ${i}-qt5
 ;;
 # qtchooser stuff
 qml|qmlbundle|qmlmin|qmlscene)
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
for lib in libQt*.a ; do
 ln -s $lib $(basename $lib .a)_debug.a
done
popd


if [ -d "examples/" ]; then
 mkdir -p %{buildroot}%{_libdir}/qt5/examples
 cp -r examples/* %{buildroot}%{_libdir}/qt5/examples/
 rm -rf %{buildroot}%{_libdir}/qt5/examples/*.pro
 rm -rf %{buildroot}%{_libdir}/qt5/examples/README
fi


%files
%{_libdir}/lib*.so.*
%{_libdir}/qt5/qml
%{_libdir}/qt5/plugins/qmltooling/*.so

%files devel
%{_libdir}/qt5/bin/*
%{_bindir}/*
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/qt5/examples/*
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_libdir}/qt5/include/*
%{_docdir}/qt5/*

%changelog
* Fri Jul 08 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-6
- Fix QTBUG-52340.

* Fri Jul 1 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-5
- Rebuild for gcc-6.1.0

* Thu Jun 30 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-4
- Fix QTBUG-52057.

* Wed Jun 29 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-2
- Try to fix crash when trying to call a property of the scope or context object.

* Tue Jun 21 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-1
- 5.7.0

* Thu Mar 24 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-1
- Release 5.6.0

* Thu Dec 03 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-5
- Fix QTBUG-48799, memleak issue

* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-4
- fix QTBUG-45991, QTBUG-48856, QTBUG-47229

* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

