Name: qt5-qtcanvas3d 
Version: 5.6.0
Release: 1
Summary: Canvas3d Component of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtcanvas3d-opensource-src-%{version}.tar.xz 

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version}

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools-devel
#for absolute path qdoc
BuildRequires: qt5-qtbase-devel


%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt5-qtbase-devel >= %{version}
Requires: qt5-qtdeclarative-devel >= %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtcanvas3d-opensource-src-%{version}

%build
qmake-qt5

make %{?_smp_mflags}
make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}


#canvas3d example need examples.pri file.
#we create a new folder to hold examples.
if [ -d "examples/" ]; then
 mkdir -p %{buildroot}%{_libdir}/qt5/examples/canvas3d
 cp -r examples/* %{buildroot}%{_libdir}/qt5/examples/canvas3d
 rm -rf %{buildroot}%{_libdir}/qt5/examples/canvas3d/*.pro
fi

%files
%{_libdir}/qt5/qml/QtCanvas3D

%files devel
%{_libdir}/qt5/examples/canvas3d
%{_docdir}/qt5/*

%changelog
* Wed Apr 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-1
- Release 5.6.0

* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

