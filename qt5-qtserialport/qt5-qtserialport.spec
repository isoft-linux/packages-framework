Name:	    qt5-qtserialport	
Version:	5.5.0
Release:	1
Summary:    Serialport Component of Qt

Group:	    Extra/Runtime/Utility
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qtserialport-opensource-src-%{version}.tar.xz	

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
%setup -q -n qtserialport-opensource-src-%{version}

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



%files
%{_libdir}/*.so.*

%files devel
%{_libdir}/cmake/*
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/qt5/include/*
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_docdir}/qt5/*
