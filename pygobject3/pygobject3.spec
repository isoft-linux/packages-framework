%{!?python_sitearch: %global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%{!?python3_sitearch: %global python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%define glib2_version                  2.22.4
%define gobject_introspection_version  0.10.8
%define python2_version                2.7

%global with_python3 1 
%define python3_version                3.4

Name: pygobject3
Version: 3.18.0
Release: 1
License: LGPLv2+ and MIT
Group: Development/Languages
Summary: Python 2 bindings for GObject Introspection
URL: https://live.gnome.org/PyGObject
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source: http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.0/pygobject-%{version}.tar.xz
Patch0: lm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires: python-devel >= %{python2_version}
BuildRequires: pycairo-devel
%if 0%{?with_python3}
BuildRequires: python3-devel >= %{python3_version}
BuildRequires: python3-cairo-devel
%endif # if with_python3

#BuildRequires: pycairo-devel
BuildRequires: autoconf, automake, libtool
BuildRequires: gnome-common
# The cairo override module depends on this
#Requires: pycairo

Requires: gobject-introspection >= %{gobject_introspection_version}

%description
The %{name} package provides a convenient wrapper for the GObject library
for use in Python programs.

%package devel
Summary: Development files for embedding PyGObject introspection support
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel
Requires: gobject-introspection-devel
Requires: pkgconfig

%description devel
This package contains files required to embed PyGObject

%if 0%{?with_python3}
%package -n python3-gobject
Summary: Python 3 bindings for GObject Introspection
Group: Development/Languages
Requires: python3-cairo
Requires: gobject-introspection >= %{gobject_introspection_version}

%description -n python3-gobject
The python3-gobject package provides a convenient wrapper for the GObject 
library and and other libraries that are compatible with GObject Introspection, 
for use in Python 3 programs.

%endif # with_python3

%prep
%setup -q -c pygobject-%{version}

cp -r pygobject-%{version} pygobject-%{version}-python2

%if 0%{?with_python3}
cp -r pygobject-%{version} pygobject-%{version}-python3
find pygobject-%{version}-python3 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find pygobject-%{version}-python2 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
pushd pygobject-%{version}-python2
PYTHON=/usr/bin/python
export PYTHON
export CC=cc
export CXX=c++
./autogen.sh
%configure
make %{?_smp_mflags}
popd

%if 0%{?with_python3}
pushd pygobject-%{version}-python3
PYTHON=/usr/bin/python3
export PYTHON
./autogen.sh
%configure
make %{_smp_mflags}
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd pygobject-%{version}-python3
PYTHON=%{__python3}
export PYTHON
make DESTDIR=$RPM_BUILD_ROOT install
popd

%endif # with_python3

pushd pygobject-%{version}-python2
make DESTDIR=$RPM_BUILD_ROOT install
popd

find $RPM_BUILD_ROOT -name '*.la' -delete
find $RPM_BUILD_ROOT -name '*.a' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644, root, root, 755)
%dir %{python_sitearch}/gi
%{python_sitearch}/gi/*
%{python_sitearch}/pygtkcompat/*
%{python_sitearch}/*.egg-info

%files devel
%defattr(644, root, root, 755)
%dir %{_includedir}/pygobject-3.0/
%{_includedir}/pygobject-3.0/pygobject.h
%{_libdir}/pkgconfig/pygobject-3.0.pc

%if 0%{?with_python3}
%files -n python3-gobject
%defattr(644, root, root, 755)
%dir %{python3_sitearch}/gi
%{python3_sitearch}/gi/*
%{python3_sitearch}/pygtkcompat/*
%{python3_sitearch}/*.egg-info
%endif # with_python3

%changelog
* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

