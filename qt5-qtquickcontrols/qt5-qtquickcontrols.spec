Name: qt5-qtquickcontrols 
Version: 5.5.1
Release: 4 
Summary: QucikControls Component of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtquickcontrols-opensource-src-%{version}.tar.xz 
Patch0: qtquickcontrols-Avoid_real_rounding_glitches_near_ends_of_slider_range-qtbug-42358.patch
Patch1: qtquickcontrols-manually-edit-to-fix-broken-inheritance-qtbug-49189.patch

BuildRequires: qt5-qtdeclarative-devel >= %{version}
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
%setup -q -n qtquickcontrols-opensource-src-%{version}
%patch0 -p1
%patch1 -p1

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


%files
%{_libdir}/qt5/qml/*

%files devel
%{_libdir}/qt5/examples/*
%{_docdir}/qt5/*

%changelog
* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-4
- Fix QTBUG-42358, QTBUG-49189

* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

