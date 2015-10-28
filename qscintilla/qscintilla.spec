
%global scintilla_ver 3.5.4

# bootstrapping -python
# undef python macros if you'd like to build qscintilla sans -python subpkg (which requires PyQt4)
%global python 1
%global python3 1
# experimental qt5 support
%global qt5 1

Summary: A Scintilla port to Qt
Name:    qscintilla
Version: 2.9
Release: 5%{?dist}

License: GPLv3
Url:     http://www.riverbankcomputing.com/software/qscintilla/
%if 0%{?snap:1}
Source0: http://www.riverbankcomputing.com/static/Downloads/QScintilla2/QScintilla-gpl-%{version}-snapshot-%{snap}.tar.gz
%else
Source0: http://downloads.sf.net/pyqt/QScintilla-gpl-%{version}.tar.gz
%endif

## Upstreamable patches
# fix qt5 mkspecs install path
Patch1: QScintilla-gpl-2.9-qt5_mkspecs.patch
# make qt5 build parallel-installable
Patch2: QScintilla-gpl-2.9-qt5.patch

BuildRequires: pkgconfig(QtDesigner) pkgconfig(QtGui) pkgconfig(QtScript) pkgconfig(QtXml)
%if 0%{?qt5}
BuildRequires: pkgconfig(Qt5Designer) pkgconfig(Qt5Gui) pkgconfig(Qt5Widgets)
%endif

Provides: bundled(scintilla) = %{scintilla_ver}

%description
QScintilla is a port of Scintilla to the Qt GUI toolkit.

%{?scintilla_ver:This version of QScintilla is based on Scintilla v%{scintilla_ver}.}

%package devel
Summary:  QScintilla Development Files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel 
%description devel
%{summary}.

%if 0%{?python}
%package python
Summary:  QScintilla python bindings
BuildRequires: PyQt4-devel
BuildRequires: sip-devel >= 3.16
Provides: python-qscintilla = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: PyQt4
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}
%description python
%{summary}.

%package python-devel
Summary:  Development files for QScintilla python bindings
Provides: python-qscintilla-devel = %{version}-%{release}
Requires: PyQt4-devel
BuildArch: noarch
%description python-devel
%{summary}.
%endif

%if 0%{?python3}
%package -n python3-qscintilla
Summary:  QScintilla python3 bindings
BuildRequires: python3-PyQt4-devel
BuildRequires: sip-devel >= 3.16
Provides: %{name}-python3 = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python3-PyQt4
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}
%description -n python3-qscintilla
%{summary}.

%package -n python3-qscintilla-devel
Summary:  Development files for QScintilla python3 bindings
Provides: %{name}-python3-devel = %{version}-%{release}
Requires: python3-PyQt4-devel
BuildArch: noarch
%description -n python3-qscintilla-devel
%{summary}.
%endif

%if 0%{?qt5}
%package qt5
Summary: A Scintilla port to Qt5
%description qt5
%{summary}.

%package qt5-devel
Summary:  QScintilla Development Files
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel
%description qt5-devel
%{summary}.

%if 0%{?python3}
%package -n python3-qscintilla-qt5
Summary:  QScintilla-qt5 python3 bindings
BuildRequires: python3-qt5
BuildRequires: python-qt5-devel
BuildRequires: sip-devel >= 3.16
Provides: %{name}-qt5-python3 = %{version}-%{release}
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
Requires: python3-qt5
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}
%description -n python3-qscintilla-qt5
%{summary}.

%package -n python3-qscintilla-qt5-devel
Summary:  Development files for QScintilla-qt5 python3 bindings
Provides: %{name}-qt5-python3-devel = %{version}-%{release}
Requires: python-qt5-devel
BuildArch: noarch
%description -n python3-qscintilla-qt5-devel
%{summary}.

%endif
%endif


%prep
%setup -q -n QScintilla-gpl-%{version}%{?snap:-snapshot-%{snap}}

%patch1 -p1 -b .qt5_mkspecs
%patch2 -p1 -b .qt5


%build
PATH=%{_qt4_bindir}:$PATH; export PATH

cp -a Qt4Qt5 Qt4/
pushd Qt4
%{qmake_qt4} qscintilla.pro
make %{?_smp_mflags}
popd

# set QMAKEFEATURES to ensure just built lib/feature is found
QMAKEFEATURES=`pwd`/Qt4/features; export QMAKEFEATURES

cp -a designer-Qt4Qt5 designer-Qt4/
pushd designer-Qt4
%{qmake_qt4} designer.pro INCLUDEPATH+=../Qt4 LIBS+=-L../Qt4
make %{?_smp_mflags}
popd

%if 0%{?python}
cp -a Python Python2-qt4
pushd Python2-qt4
%{__python2} \
  configure.py \
    --no-timestamp \
    --qsci-incdir=../Qt4 --qsci-libdir=../Qt4

make %{?_smp_mflags}
popd
%endif

%if 0%{?python3}
cp -a Python Python3-qt4
pushd Python3-qt4
%{__python3} \
  configure.py \
    --no-timestamp \
    --pyqt-sipdir=/usr/share/python3-sip/PyQt4 \
    --qsci-incdir=../Qt4 --qsci-libdir=../Qt4 \
    --sip=/usr/bin/python3-sip

make %{?_smp_mflags}
popd
%endif

%if 0%{?qt5}
PATH=%{_qt5_bindir}:$PATH; export PATH

cp -a Qt4Qt5 Qt5/
pushd Qt5
%{qmake_qt5} qscintilla.pro
make %{?_smp_mflags}
popd

# set QMAKEFEATURES to ensure just built lib/feature is found
QMAKEFEATURES=`pwd`/Qt5/features; export QMAKEFEATURES

cp -a designer-Qt4Qt5 designer-Qt5/
pushd designer-Qt5
%{qmake_qt5} designer.pro INCLUDEPATH+=../Qt5 LIBS+=-L../Qt5
make %{?_smp_mflags}
popd

%if 0%{?python3}
cp -a Python Python3-qt5
pushd Python3-qt5
%{__python3} \
  configure.py \
    --no-timestamp \
    --pyqt=PyQt5 --qsci-incdir=../Qt5 --qsci-libdir=../Qt5

make %{?_smp_mflags}
popd
%endif

%endif


%install
make -C Qt4 install INSTALL_ROOT=%{buildroot}
make -C designer-Qt4 install INSTALL_ROOT=%{buildroot}
%if 0%{?python}
make -C Python2-qt4 install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}
test -x   %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so || \
chmod a+x %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so
%endif
%if 0%{?python3}
make -C Python3-qt4 install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}
test -x   %{buildroot}%{python3_sitearch}/PyQt4/Qsci.so || \
chmod a+x %{buildroot}%{python3_sitearch}/PyQt4/Qsci.so
%endif

%if 0%{?qt5}
make -C Qt5 install INSTALL_ROOT=%{buildroot}
make -C designer-Qt5 install INSTALL_ROOT=%{buildroot}
%if 0%{?python3}
make -C Python3-qt5 install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}
test -x   %{buildroot}%{python3_sitearch}/PyQt5/Qsci.so || \
chmod a+x %{buildroot}%{python3_sitearch}/PyQt5/Qsci.so
%endif
%endif

%find_lang qscintilla --with-qt
grep "%{_qt4_translationdir}" qscintilla.lang > qscintilla-qt4.lang
grep "%{_qt5_translationdir}" qscintilla.lang > qscintilla-qt5.lang

%if !0%{?python} && !0%{?python3}
# unpackaged files
rm -rfv %{buildroot}%{_qt4_datadir}/qsci/
%endif


%check
# verify python module(s) permissions and libqscintilla2 linkage
# https://bugzilla.redhat.com/show_bug.cgi?id=1104559
ldd     %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so | grep libqscintilla2 || exit 1
test -x %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so
%if 0%{?python3}
ldd     %{buildroot}%{python3_sitearch}/PyQt4/Qsci.so | grep libqscintilla2 || exit 1
test -x %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f qscintilla-qt4.lang
%doc NEWS README
%license LICENSE
%{_qt4_libdir}/libqscintilla2.so.12*
%{_qt4_plugindir}/designer/libqscintillaplugin.so

%files devel
%doc doc/html-Qt4Qt5 doc/Scintilla example-Qt4Qt5
%{_qt4_headerdir}/Qsci/
%{_qt4_libdir}/libqscintilla2.so
%{_qt4_datadir}/mkspecs/features/qscintilla2.prf

%if 0%{?python}
%files python
%{python2_sitearch}/PyQt4/Qsci.so
%{_qt4_datadir}/qsci/

%files python-devel
%{_datadir}/sip/PyQt4/Qsci/
%endif

%if 0%{?python3}
%files -n python3-qscintilla
%{python3_sitearch}/PyQt4/Qsci.so
%{_qt4_datadir}/qsci/

%files -n python3-qscintilla-devel
%{_datadir}/python3-sip/PyQt4/Qsci/
%endif

%if 0%{?qt5}
%files qt5 -f qscintilla-qt5.lang
%doc NEWS README
%license LICENSE
%{_qt5_libdir}/libqscintilla2-qt5.so.12*
%{_qt5_plugindir}/designer/libqscintillaplugin.so

%files qt5-devel
%doc doc/html-Qt4Qt5 doc/Scintilla example-Qt4Qt5
%{_qt5_headerdir}/Qsci/
%{_qt5_libdir}/libqscintilla2-qt5.so
%{_qt5_archdatadir}/mkspecs/features/qscintilla2.prf

%if 0%{?python3}
%files -n python3-qscintilla-qt5
%{python3_sitearch}/PyQt5/Qsci.so
%{_qt5_datadir}/qsci/

%files -n python3-qscintilla-qt5-devel
%{_datadir}/sip/PyQt5/Qsci/
%endif
%endif


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.9-5
- Rebuild for new 4.0 release.

