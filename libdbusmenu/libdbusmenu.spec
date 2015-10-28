%global tools_doc %{_docdir}/%{name}-tools
%global glib_doc  %{_docdir}/%{name}-glib-devel

Name:		libdbusmenu
Version:	12.10.2
Release:	10%{?dist}
Summary:	A library that pulling out some code out of indicator-applet

# All files installed in final rpms use C sources with dual licensing headers.
# Tests compiled in the build process are licensed GPLv3

License:	LGPLv3 or LGPLv2 and GPLv3
URL:		https://launchpad.net/libdbusmenu
Source0:	https://launchpad.net/libdbusmenu/12.10/12.10.2/+download/%{name}-%{version}.tar.gz

BuildRequires:	vala-tools vala-devel
BuildRequires:	json-glib-devel
BuildRequires:	chrpath
BuildRequires:	intltool
BuildRequires:	gobject-introspection-devel
BuildRequires:  gnome-doc-utils
BuildRequires:	python
BuildRequires:	glib2-devel
# valgrind exists only on selected arches
%ifarch %{ix86} x86_64 ppc ppc64 s390x %{arm}
BuildRequires:	valgrind-devel
%endif
BuildRequires:	pkgconfig
BuildRequires:	glibc-devel
BuildRequires:	gtk3-devel
BuildRequires:	gtk2-devel
BuildRequires:	atk-devel

%description
It passes a menu structure across DBus so that a program can create 
a menu simply without worrying about how it is displayed on the 
other side of the bus


%package devel
Summary:	%{summary}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	dbus-glib-devel 
%description devel
Development Files for %{name}


%package gtk2
Summary:	%{summary}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description gtk2
Shared libraries for the %{name}-gtk2 library

%package gtk3
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	%{summary}

%description gtk3
Shared libraries for the %{name}-gtk3 library


%package	gtk2-devel
Summary:	Development files for %{name}
Requires:	%{name}-gtk2%{?_isa} = %{version}-%{release}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	gtk2-devel
Requires:	dbus-glib-devel
%description	gtk2-devel
The %{name}-gtk2-devel package contains libraries and header files for
developing applications that use %{name}.

%package	gtk3-devel
Summary:	Development files for %{name}
Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	gtk3-devel
Requires:	dbus-glib-devel

%description	gtk3-devel
The %{name}-gtk3-devel package contains libraries and header files for
developing applications that use %{name}.

%package	jsonloader
Summary:	Test lib development files
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
%description	jsonloader
It passes a menu structure across DBus so that a program can create
a menu simply without worrying about how it is displayed on the
other side of the bus

%package	jsonloader-devel
Summary:	Test lib development files for %{name}
Requires:	%{name}-jsonloader%{?_isa} = %{version}-%{release}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description	jsonloader-devel
It passes a menu structure across DBus so that a program can create
a menu simply without worrying about how it is displayed on the
other side of the bus

%package	doc
Summary:	Document files for %{name}
BuildArch:	noarch
%description	doc 
The %{name}-doc package contains documents for
developing applications that use %{name}.

%package	tools 
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	Development tools for the dbusmenu libraries

%description	tools 
The %{name}-tools package contains helper tools for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version} -c
cp -a %{name}-%{version}/{README,COPYING,COPYING.2.1,COPYING-GPL3,AUTHORS} .
cp -a %{name}-%{version} %{name}-gtk3-%{version}

%build
pushd %{name}-gtk3-%{version}
sed -i -e 's@^#!.*python$@#!/usr/bin/python2@' tools/dbusmenu-bench
export CFLAGS="%{optflags} -Wno-error=deprecated-declarations"
%configure --disable-static --disable-scrollkeeper  --with-gtk=3 --disable-dumper
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags} V=1
popd


pushd %{name}-%{version}
sed -i -e 's@^#!.*python$@#!/usr/bin/python2@' tools/dbusmenu-bench
export CFLAGS="%{optflags} -Wno-error=deprecated-declarations"
%configure  --disable-static --disable-scrollkeeper --with-gtk=2 --disable-dumper
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags} V=1
popd


%install
pushd %{name}-gtk3-%{version}
make install DESTDIR=%{buildroot}
chrpath --delete %{buildroot}%{_libdir}/libdbusmenu-gtk3.so.4.0.12
chrpath --delete %{buildroot}%{_libdir}/libdbusmenu-jsonloader.so.4.0.12
chrpath --delete %{buildroot}%{_libexecdir}/dbusmenu-testapp

find %{buildroot} -name '*.la' -exec rm -f {} ';'
popd


pushd %{name}-%{version}
make install DESTDIR=%{buildroot}
chrpath --delete %{buildroot}%{_libdir}/libdbusmenu-gtk.so.4.0.12
chrpath --delete %{buildroot}%{_libdir}/libdbusmenu-jsonloader.so.4.0.12
chrpath --delete %{buildroot}%{_libexecdir}/dbusmenu-testapp

find %{buildroot} -name '*.la' -exec rm -f {} ';'
popd


# Put documentation in correct directory
install -dm755 %{buildroot}%{tools_doc}/
mv %{buildroot}%{_docdir}/%{name}/README.dbusmenu-bench \
	%{buildroot}%{tools_doc}

# Put examples in correct documentation directory
install -dm755 %{buildroot}%{glib_doc}/examples/
mv %{buildroot}%{_docdir}/%{name}/examples/glib-server-nomenu.c \
	%{buildroot}%{glib_doc}/examples/


%post -p /sbin/ldconfig
%post gtk2 -p /sbin/ldconfig
%post gtk3 -p /sbin/ldconfig
%post jsonloader -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun gtk2 -p /sbin/ldconfig
%postun gtk3 -p /sbin/ldconfig
%postun jsonloader -p /sbin/ldconfig

%files 
%doc README COPYING COPYING.2.1 COPYING-GPL3 AUTHORS
%{_libdir}/libdbusmenu-glib.so.*
%{_libdir}/girepository-1.0/Dbusmenu-0.4.typelib

%files devel
%dir %{_includedir}/libdbusmenu-glib-0.4/
%dir %{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-glib/*.h
%{_libdir}/libdbusmenu-glib.so
%{_libdir}/pkgconfig/dbusmenu-glib-0.4.pc
%{_datadir}/gir-1.0/Dbusmenu-0.4.gir
%{_datadir}/vala/vapi/Dbusmenu-0.4.vapi
%dir %{glib_doc}/
%dir %{glib_doc}/examples/
%doc %{glib_doc}/examples/glib-server-nomenu.c

%files jsonloader
%{_libdir}/libdbusmenu-jsonloader.so.*


%files jsonloader-devel
%dir %{_includedir}/libdbusmenu-glib-0.4/
%dir %{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-jsonloader/
%{_includedir}/libdbusmenu-glib-0.4/libdbusmenu-jsonloader/*.h
%{_libdir}/libdbusmenu-jsonloader.so
%{_libdir}/pkgconfig/dbusmenu-jsonloader-0.4.pc

%files gtk3
%{_libdir}/libdbusmenu-gtk3.so.*
%{_libdir}/girepository-1.0/DbusmenuGtk3-0.4.typelib

%files gtk2
%{_libdir}/libdbusmenu-gtk.so.*
%{_libdir}/girepository-1.0/DbusmenuGtk-0.4.typelib


%files gtk3-devel
%dir %{_includedir}/libdbusmenu-gtk3-0.4
%dir %{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk
%{_includedir}/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/*.h
%{_libdir}/libdbusmenu-gtk3.so
%{_libdir}/pkgconfig/dbusmenu-gtk3-0.4.pc
%{_datadir}/gir-1.0/DbusmenuGtk3-0.4.gir
%{_datadir}/vala/vapi/DbusmenuGtk3-0.4.vapi

%files gtk2-devel
%dir %{_includedir}/libdbusmenu-gtk-0.4
%dir %{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk
%{_includedir}/libdbusmenu-gtk-0.4/libdbusmenu-gtk/*.h
%{_libdir}/libdbusmenu-gtk.so
%{_libdir}/pkgconfig/dbusmenu-gtk-0.4.pc
%{_datadir}/gir-1.0/DbusmenuGtk-0.4.gir
%{_datadir}/vala/vapi/DbusmenuGtk-0.4.vapi


%files doc 
%doc README COPYING COPYING.2.1 AUTHORS
%dir %{_datadir}/gtk-doc/
%{_datadir}/gtk-doc/*

%files tools
%{_libexecdir}/dbusmenu-bench
%{_libexecdir}/dbusmenu-testapp
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/json/
%{_datadir}/%{name}/json/test-gtk-label.json
%dir %{tools_doc}/
%{tools_doc}/README.dbusmenu-bench

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 12.10.2-10
- Rebuild for new 4.0 release.

