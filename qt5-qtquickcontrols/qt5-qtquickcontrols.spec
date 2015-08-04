Name:	    qt5-qtquickcontrols	
Version:	5.5.0
Release:	1
Summary:    QucikControls Component of Qt

Group:	    Extra/Runtime/Library
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qtquickcontrols-opensource-src-%{version}.tar.xz	

BuildRequires:  qt5-qtbase-devel

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
%setup -q -n qtquickcontrols-opensource-src-%{version}

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

rpmclean

%files
%{_libdir}/qt5/qml/*

%files devel
%{_libdir}/qt5/examples/*
%{_docdir}/qt5/*
