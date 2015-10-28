Name: qt5-qtenginio 
Version: 5.5.1
Release: 4 
Summary: Enginio Component of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtenginio-opensource-src-%{version}.tar.xz 

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools
#for absolute path qdoc
BuildRequires: qt5-qtbase


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
%setup -q -n qtenginio-opensource-src-%{version}

%build
qmake-qt5

make %{?_smp_mflags}

make docs
%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}

if [ -d "examples/" ]; then
 mkdir -p %{buildroot}%{_libdir}/qt5/examples
 cp -r examples/* %{buildroot}%{_libdir}/qt5/examples/
 rm -rf %{buildroot}%{_libdir}/qt5/examples/*.pro
fi


%files
%{_libdir}/*.so.*
%{_libdir}/qt5/qml/Enginio/libenginioplugin.so
%{_libdir}/qt5/qml/Enginio/plugins.qmltypes
%{_libdir}/qt5/qml/Enginio/qmldir

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
* Sat Oct 24 2015 builder - 5.5.1-4
- Rebuild for new 4.0 release.

* Fri Oct 23 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-3
- Fix wrong libQt*debug links

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

