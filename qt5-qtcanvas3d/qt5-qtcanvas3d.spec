Name:	    qt5-qtcanvas3d	
Version:	5.5.0
Release:	1
Summary:    Canvas3d Component of Qt

Group:	    Extra/Runtime/Utility
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qtcanvas3d-opensource-src-%{version}.tar.xz	

BuildRequires:  qt5-qtbase-devel
BuildRequires:  bluez-libs-devel

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires:  qt5-qttools
#for absolute path qdoc
BuildRequires:  qt5-qtbase


%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Extra/Development/Library
Requires:       %{name} = %{version}-%{release}

%description    devel
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
