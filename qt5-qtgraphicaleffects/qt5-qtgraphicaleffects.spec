Name: qt5-qtgraphicaleffects
Version: 5.5.1
Release: 2 
Summary: QtGraphicaleffects component

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtgraphicaleffects-opensource-src-%{version}.tar.xz 

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: libmng-devel
BuildRequires: libtiff-devel

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools
#for absolute path qdoc
BuildRequires: qt5-qtbase

%description
QtGraphicaleffects component

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtgraphicaleffects-opensource-src-%{version}

%build
qmake-qt5

make %{?_smp_mflags}
make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}



%files
%{_libdir}/qt5/qml/QtGraphicalEffects

%files devel
%{_docdir}/qt5/*

%changelog
* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

