Name: qt5-qtquickcontrols 
Version: 5.7.0
Release: 2
Summary: QucikControls Component of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qtquickcontrols-opensource-src-%{version}.tar.xz 
 
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
* Thu Nov 24 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-2
- 5.7.0-2

* Tue Jun 21 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-1
- 5.7.0

* Wed Apr 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-1
- Release 5.6.0

* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-6
- Fix QTBUG-45984

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-5
- Revert some commit to fix kcmshell5 kwineffects popup menu position issue.

* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 5.5.1-4
- Fix QTBUG-42358, QTBUG-49189

* Sat Oct 24 2015 builder - 5.5.1-3
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1

