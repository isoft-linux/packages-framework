#NOTE, gstreamer-0.10 support is disabled, since we do not ship old gstreamer

Name: qt5-qtmultimedia 
Version: 5.5.1
Release: 4 
Summary: Multimedia Component of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtmultimedia-opensource-src-%{version}.tar.xz

Patch0: qtmultimedia-fix-QTBUG-49461.patch

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version} 
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-app-1.0)
BuildRequires: pkgconfig(gstreamer-audio-1.0)
BuildRequires: pkgconfig(gstreamer-base-1.0)
BuildRequires: pkgconfig(gstreamer-pbutils-1.0)
BuildRequires: pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires: pkgconfig(gstreamer-video-1.0)
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
BuildRequires: pkgconfig(openal)
BuildRequires: pkgconfig(xv)

#for the first time to build qt5, qhelpgenerator will missing, the doc build will fail.
#after qtbase build, then buld qttools, we can generate docs.
#for qhelpgenerator
BuildRequires: qt5-qttools-devel
#for absolute path qdoc
BuildRequires: qt5-qtbase-devel

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
%setup -q -n qtmultimedia-opensource-src-%{version}
%patch0 -p1

%build
#without git_build, some private header will have problems.
qmake-qt5 CONFIG+=git_build

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
%{_libdir}/*.so.*
%{_libdir}/qt5/qml/*
%{_libdir}/qt5/plugins/*

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
* Mon Nov 23 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-4
- Fix QTBUG 49461

* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

