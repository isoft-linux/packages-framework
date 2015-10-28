%global with_python3 1
%global qtassistant 0 
%global webkit 1

%if 0%{?with_python3}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")

%endif
%{!?__python2:%global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}
%global python2_dbus_dir %(%{__python2} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")

Summary: Python bindings for Qt4
Name: 	 PyQt4
Version: 4.11.4
Release: 3%{?dist}

# GPLv2 exceptions(see GPL_EXCEPTIONS*.txt)
License: (GPLv3 or GPLv2 with exceptions) and BSD
Url:     http://www.riverbankcomputing.com/software/pyqt/
%if 0%{?snap:1}
Source0:  http://www.riverbankcomputing.com/static/Downloads/PyQt4/PyQt-x11-gpl-%{version}%{?snap:-snapshot-%{snap}}.tar.gz
%else
Source0:  http://downloads.sourceforge.net/pyqt/PyQt-x11-gpl%{?snap:-snapshot}-%{version}%{?snap:-%{snap}}.tar.gz
%endif

Source2: pyuic4.sh

## upstreamable patches

## upstream patches
# fix FTBFS on ARM
Patch60:  qreal_float_support.diff

# rhel patches
Patch300: PyQt-x11-gpl-4.10-webkit.patch

BuildRequires: chrpath
BuildRequires: dbus-python
BuildRequires: findutils
BuildRequires: pkgconfig(dbus-1) pkgconfig(dbus-python)
BuildRequires: pkgconfig(phonon)
%if 0%{?qtassistant}
BuildRequires: pkgconfig(QtAssistantClient)
%endif
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtDeclarative) pkgconfig(QtDesigner)
BuildRequires: pkgconfig(QtGui) pkgconfig(QtHelp) pkgconfig(QtMultimedia)
BuildRequires: pkgconfig(QtNetwork) pkgconfig(QtOpenGL)
BuildRequires: pkgconfig(QtScript) pkgconfig(QtScriptTools)
BuildRequires: pkgconfig(QtSql) pkgconfig(QtSvg) pkgconfig(QtTest)
BuildRequires: pkgconfig(QtXml) pkgconfig(QtXmlPatterns)
%if 0%{?webkit}
# TODO: make -webkit subpkg
BuildRequires: pkgconfig(QtWebKit)
%endif
BuildRequires: python2-devel
BuildRequires: sip-devel >= 4.16.8

%if 0%{?with_python3}
BuildRequires: python3-dbus
BuildRequires: python3-devel 
BuildRequires: python3-sip-devel >= 4.16.8
%endif # with_python3

Requires: dbus-python
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

%if 0%{?webkit}
# could theoretically enumerate all the modules built/packaged here, but this
# should be good start (to ease introduction of -webkit for epel-6+ for example)
Obsoletes: %{name}-webkit < %{version}-%{release}
Provides: %{name}-webkit = %{version}-%{release}
Provides: %{name}-webkit%{?_isa} = %{version}-%{release}
%endif

Provides: python-qt4 = %{version}-%{release}
Provides: pyqt4 = %{version}-%{release}

#%filter_provides_in %{python2_sitearch} %{?_qt4_plugindir}
%if 0%{?with_python3}
#%filter_provides_in %{python3_sitearch} %{?_qt4_plugindir}
%endif
#%filter_setup

%description
These are Python bindings for Qt4.

%package devel
Summary: Files needed to build other bindings based on Qt4
%if 0%{?webkit}
Obsoletes: %{name}-webkit-devel < %{version}-%{release}
Provides: %{name}-webkit-devel = %{version}-%{release}
%endif
Provides: python-qt4-devel = %{version}-%{release}
Provides: pyqt4-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
Requires: sip-devel
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt4 classes (e.g. KDE or your own).

%package doc
Summary: PyQt4 developer documentation and examples
BuildArch: noarch
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
Provides: python-qt4-doc = %{version}-%{release}
%description doc
%{summary}.

# split-out arch'd subpkg, since (currently) %%_qt4_datadir = %%_qt4_libdir
%package qsci-api
Summary: Qscintilla API file support
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
Provides: python-qt4-qsci-api = %{version}-%{release}
%description qsci-api
%{summary}.

%if 0%{?qtassistant}
%package assistant
Summary: Python bindings for QtAssistant
Provides: python-qt4-assistant = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description assistant
%{summary}.
%endif

# The bindings are imported as "PyQt4", hence it's reasonable to name the
# Python 3 subpackage "python3-PyQt4", despite the apparent tautology
%package -n python3-%{name}
Summary: Python 3 bindings for Qt4
Requires: python3-dbus
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%{?_sip_api:Requires: python3-sip-api(%{_sip_api_major}) >= %{_sip_api}}
%if 0%{?webkit}
Provides: python3-%{name}-webkit = %{version}-%{release}
Provides: python3-%{name}-webkit%{?_isa} = %{version}-%{release}
%endif
Provides: python3-qt4 = %{version}-%{release}
%description -n python3-%{name}
These are Python 3 bindings for Qt4.

%package -n python3-%{name}-assistant
Summary: Python 3 bindings for QtAssistant
Provides: python3-qt4-assistant = %{version}-%{release}
Requires: python3-%{name}%{?_isa} = %{version}-%{release}
%description -n python3-%{name}-assistant
%{summary}.

%package -n python3-%{name}-devel
Summary: Python 3 bindings for Qt4
Provides: python3-%{name}-webkit-devel = %{version}-%{release}
Provides: python3-qt4-devel = %{version}-%{release}
Requires: python3-%{name}%{?_isa} = %{version}-%{release}
Requires: python3-sip-devel
# when split happened, upgrade path
Obsoletes: python3-PyQt4-devel < 4.10.3-6
%description -n python3-%{name}-devel
Files needed to build other Python 3 bindings for C++ classes that inherit
from any of the Qt4 classes (e.g. KDE or your own).


%prep
%setup -q -n PyQt-x11-gpl-%{version}%{?snap:-snapshot-%{snap}}

# save orig for comparison later
cp -a ./sip/QtGui/opengl_types.sip ./sip/QtGui/opengl_types.sip.orig
%patch60 -p1 -b .arm
%if ! 0%{?webkit}
%patch300 -p1 -b .webkit
%endif

# permissions, mark examples non-executable
find examples/ -name "*.py" | xargs chmod a-x

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build

QT4DIR=%{_qt4_prefix}
PATH=%{_qt4_bindir}:$PATH ; export PATH

# Python 2 build:
%{__python2} configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qmake=/usr/bin/qmake-qt4 \
  --qsci-api --qsci-api-destdir=%{_qt4_datadir}/qsci \
  --verbose 

make %{?_smp_mflags}

# Python 3 build:
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qmake=/usr/bin/qmake-qt4 \
  --no-qsci-api \
  --sipdir=%{_datadir}/python3-sip/PyQt4 \
  --verbose 

make %{?_smp_mflags}
popd
%endif # with_python3


%install

# Install Python 3 first, and move aside any executables, to avoid clobbering
# the Python 2 installation:
%if 0%{?with_python3}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{py3dir}
%endif # with_python3

make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}

# remove Python 3 code from Python 2.6 directory, fixes FTBFS (#564633)
rm -rfv %{buildroot}%{python2_sitearch}/PyQt4/uic/port_v3/

# likewise, remove Python 2 code from the Python 3.1 directory:
rm -rfv %{buildroot}%{python3_sitearch}/PyQt4/uic/port_v2/

# webkit
%if ! 0%{?webkit}
rm -rf %{buildroot}%{python3_sitearch}/PyQt4/uic/widget-plugins/qtwebkit* \
       %{buildroot}%{python2_sitearch}/PyQt4/uic/widget-plugins/qtwebkit*
%endif

# install pyuic4 wrapper to support both python2/python3
rm -fv %{buildroot}%{_bindir}/pyuic4
install -p -m755 -D %{SOURCE2} \
  %{buildroot}%{_bindir}/pyuic4
sed -i \
  -e "s|@PYTHON3@|%{__python3}|g" \
  -e "s|@PYTHON2@|%{__python2}|g" \
  %{buildroot}%{_bindir}/pyuic4


%check
# verify opengl_types.sip sanity
diff -u ./sip/QtGui/opengl_types.sip.orig \
        ./sip/QtGui/opengl_types.sip ||:


%files
%doc NEWS README
%doc LICENSE
%{python2_dbus_dir}/qt.so
%dir %{python2_sitearch}/PyQt4/
%{python2_sitearch}/PyQt4/__init__.py*
%{python2_sitearch}/PyQt4/pyqtconfig.py*
%{python2_sitearch}/PyQt4/phonon.so
%{python2_sitearch}/PyQt4/Qt.so
%{python2_sitearch}/PyQt4/QtCore.so
%{python2_sitearch}/PyQt4/QtDBus.so
%{python2_sitearch}/PyQt4/QtDeclarative.so
%{python2_sitearch}/PyQt4/QtDesigner.so
%{python2_sitearch}/PyQt4/QtGui.so
%{python2_sitearch}/PyQt4/QtHelp.so
%{python2_sitearch}/PyQt4/QtMultimedia.so
%{python2_sitearch}/PyQt4/QtNetwork.so
%{python2_sitearch}/PyQt4/QtOpenGL.so
%{python2_sitearch}/PyQt4/QtScript.so
%{python2_sitearch}/PyQt4/QtScriptTools.so
%{python2_sitearch}/PyQt4/QtSql.so
%{python2_sitearch}/PyQt4/QtSvg.so
%{python2_sitearch}/PyQt4/QtTest.so
%if 0%{?webkit}
%{python2_sitearch}/PyQt4/QtWebKit.so
%endif
%{python2_sitearch}/PyQt4/QtXml.so
%{python2_sitearch}/PyQt4/QtXmlPatterns.so
%{python2_sitearch}/PyQt4/uic/
%{_qt4_plugindir}/designer/*

%if 0%{?qtassistant}
%files assistant
%{python2_sitearch}/PyQt4/QtAssistant.so
%endif

%files devel
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%{_datadir}/sip/PyQt4/

%files doc
%doc doc/*
%doc examples/

%files qsci-api
# avoid dep on qscintilla-python, own %_qt4_datadir/qsci/... here for now
%dir %{_qt4_datadir}/qsci/
%dir %{_qt4_datadir}/qsci/api/
%dir %{_qt4_datadir}/qsci/api/python/
%{_qt4_datadir}/qsci/api/python/PyQt4.api

%if 0%{?with_python3}
%files -n python3-%{name}
%doc NEWS README
%doc LICENSE
%{python3_dbus_dir}/qt.so
%dir %{python3_sitearch}/PyQt4/
%{python3_sitearch}/PyQt4/__init__.py*
#%{python3_sitearch}/PyQt4/__pycache__/
%{python3_sitearch}/PyQt4/pyqtconfig.py*
%{python3_sitearch}/PyQt4/phonon.so
%{python3_sitearch}/PyQt4/Qt.so
%{python3_sitearch}/PyQt4/QtCore.so
%{python3_sitearch}/PyQt4/QtDBus.so
%{python3_sitearch}/PyQt4/QtDeclarative.so
%{python3_sitearch}/PyQt4/QtDesigner.so
%{python3_sitearch}/PyQt4/QtGui.so
%{python3_sitearch}/PyQt4/QtHelp.so
%{python3_sitearch}/PyQt4/QtMultimedia.so
%{python3_sitearch}/PyQt4/QtNetwork.so
%{python3_sitearch}/PyQt4/QtOpenGL.so
%{python3_sitearch}/PyQt4/QtScript.so
%{python3_sitearch}/PyQt4/QtScriptTools.so
%{python3_sitearch}/PyQt4/QtSql.so
%{python3_sitearch}/PyQt4/QtSvg.so
%{python3_sitearch}/PyQt4/QtTest.so
%if 0%{?webkit}
%{python3_sitearch}/PyQt4/QtWebKit.so
%endif
%{python3_sitearch}/PyQt4/QtXml.so
%{python3_sitearch}/PyQt4/QtXmlPatterns.so
%{python3_sitearch}/PyQt4/uic/

%if 0%{?qtassistant}
%files -n python3-%{name}-assistant
%{python3_sitearch}/PyQt4/QtAssistant.so
%endif

%files -n python3-%{name}-devel
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%{_datadir}/python3-sip/PyQt4/
%endif


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.11.4-3
- Rebuild for new 4.0 release.

