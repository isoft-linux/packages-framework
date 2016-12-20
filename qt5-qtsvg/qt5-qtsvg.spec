Name: qt5-qtsvg 
Version: 5.7.1
Release: 1
Summary: SVG component of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtsvg-opensource-src-%{version}.tar.xz 

BuildRequires: qt5-qtbase-devel >= %{version} 

BuildRequires: pkgconfig(zlib)

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools-devel
#for absolute path qdoc
BuildRequires: qt5-qtbase-devel


%description
SVG component of Qt

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt5-qtbase >= %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtsvg-opensource-src-%{version}

%build
qmake-qt5

make %{?_smp_mflags}
make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}

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
%{_libdir}/qt5/plugins/iconengines/libqsvgicon.so
%{_libdir}/qt5/plugins/imageformats/libqsvg.so

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
* Tue Dec 20 2016 sulit - 5.7.1-1
- upgrade qt5-qtsvg to 5.7.1

* Tue Jun 21 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-1
- 5.7.0

* Wed Apr 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-1
- Release 5.6.0

* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

