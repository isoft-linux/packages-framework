Name:	    qt5-qtdoc
Version:	5.5.0
Release:	1
Summary:    Main Qt Reference Documentation 

Group:	    Extra/Runtime/Library	
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qtdoc-opensource-src-%{version}.tar.xz	

BuildRequires:  qt5-qtbase-devel
Requires:   qt5-qtbase = %{version}-%{release}	

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires:  qt5-qttools
#for absolute path qdoc
BuildRequires:  qt5-qtbase


%description
qtdoc contains the main Qt Reference Documentation, which includes
overviews, Qt topics, and examples not specific to any Qt module.The
configuration files are located in qtdoc/doc/config and the articles in
qtdoc/doc/src.

%package        devel
Summary:        Development files for %{name}
Group:          Extra/Development/Library
Requires:       qt5-qtbase-devel = %{version}-%{release}	
Requires:       qt5-qtdeclarative-devel = %{version}-%{release}	

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtdoc-opensource-src-%{version}

%build
qmake-qt5

make %{?_smp_mflags}
make docs

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}


%files devel
%{_docdir}/qt5/*
