Name: qt5-qtimageformats
Version: 5.5.1
Release: 2 
Summary: Image Format Plugin of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtimageformats-opensource-src-%{version}.tar.xz 

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: jasper-devel libtiff-devel libwebp-devel

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools
#for absolute path qdoc
BuildRequires: qt5-qtbase


%description
Image Format Plugin of Qt

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: qt5-qtbase-devel >= %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtimageformats-opensource-src-%{version}

%build
qmake-qt5

make %{?_smp_mflags}
make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}


%files
%{_libdir}/qt5/plugins/imageformats/*.so

%files devel
%{_libdir}/cmake/Qt5Gui/*.cmake
%{_docdir}/qt5/*

%changelog
* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

