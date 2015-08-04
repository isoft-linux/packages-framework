Name:	    qt5-qtimageformats
Version:	5.5.0
Release:	1
Summary:    Image Format Plugin of Qt

Group:	    Extra/Runtime/Library	
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qtimageformats-opensource-src-%{version}.tar.xz	

BuildRequires:  mesa-libGLESv2-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  jasper-devel libtiff-devel libwebp-devel

Requires:   qt5-qtbase = %{version}-%{release}	


#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires:  qt5-qttools
#for absolute path qdoc
BuildRequires:  qt5-qtbase


%description
Image Format Plugin of Qt

%package        devel
Summary:        Development files for %{name}
Group:          Extra/Development/Library
Requires:       %{name} = %{version}-%{release}
Requires:       qt5-qtbase-devel = %{version}-%{release}	

%description    devel
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
