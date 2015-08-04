Name:	    qt5-qtgraphicaleffects
Version:	5.5.0
Release:	1
Summary:    QtGraphicaleffects component

Group:	    Extra/Runtime/Library	
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qtgraphicaleffects-opensource-src-%{version}.tar.xz	

BuildRequires:  qt5-qtbase-devel
Requires:   qt5-qtbase = %{version}-%{release}	

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires:  qt5-qttools
#for absolute path qdoc
BuildRequires:  qt5-qtbase

%description
QtGraphicaleffects component

%package        devel
Summary:        Development files for %{name}
Group:          Extra/Development/Library
Requires:       %{name} = %{version}-%{release}
Requires:       qt5-qtbase-devel = %{version}-%{release}	

%description    devel
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
