Name: qt5-qtwayland 
Version: 5.5.1
Release: 3 
Summary: Wayland backend of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtwayland-opensource-src-%{version}.tar.xz 

BuildRequires:  qt5-qtbase-devel >= %{version} 
BuildRequires:  qt5-qtdeclarative-devel >= %{version}
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libinput)

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
Requires: pkgconfig(xkbcommon)
Requires:  pkgconfig(wayland-client)

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtwayland-opensource-src-%{version}

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


if [ -d "examples/" ]; then
 mkdir -p %{buildroot}%{_libdir}/qt5/examples
 cp -r examples/* %{buildroot}%{_libdir}/qt5/examples/
 rm -rf %{buildroot}%{_libdir}/qt5/examples/*.pro
fi



%files
%{_libdir}/qt5/bin/qtwaylandscanner
%{_libdir}/*.so.*
%{_libdir}/qt5/plugins/platforms/libqwayland-egl.so
%{_libdir}/qt5/plugins/platforms/libqwayland-generic.so
%{_libdir}/qt5/plugins/wayland-decoration-client/*
%{_libdir}/qt5/plugins/wayland-graphics-integration-client/*


%files devel
%{_libdir}/cmake/*
%{_libdir}/*.prl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/qt5/examples/*
%{_libdir}/qt5/include/*
%{_libdir}/qt5/mkspecs/modules/*.pri

%changelog
* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

