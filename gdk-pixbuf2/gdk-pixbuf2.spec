%global with_x11 1

Name:           gdk-pixbuf2
Version:        2.32.1
Release:        1
Summary:        An image loading library

License:        LGPLv2+
URL:            http://www.gt.org
#VCS:		git:git://git.gnome.org/gdk-pixbuf
Source0:        http://download.gnome.org/sources/gdk-pixbuf/2.21/gdk-pixbuf-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  jasper-devel
BuildRequires:  gobject-introspection-devel >= 0.9.3
# gdk-pixbuf does a configure time check which uses the GIO mime
# layer; we need to actually have the mime type database.
BuildRequires:  shared-mime-info
# Bootstrap requirements
BuildRequires: autoconf automake libtool

# We also need MIME information at runtime
Requires: shared-mime-info

# gdk-pixbuf was included in gtk2 until 2.21.2
Conflicts: gtk2 <= 2.21.2


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

%package devel
Summary: Development files for gdk-pixbuf
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel

# gdk-pixbuf was included in gtk2 until 2.21.2
Conflicts: gtk2-devel <= 2.21.2

%description devel
This package contains the libraries and header files that are needed
for writing applications that are using gdk-pixbuf.


%prep
%setup -q -n gdk-pixbuf-%{version}

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
	--with-libjasper             \
	--with-included-loaders=png  \
    %if %with_x11
    --with-x11
    %else
    --without-x11
    %endif
)

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT    \
             RUN_QUERY_LOADER_TEST=false

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.la

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

#(cd $RPM_BUILD_ROOT%{_bindir}
# mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders
#)

%find_lang gdk-pixbuf

%post
/sbin/ldconfig
gdk-pixbuf-query-loaders --update-cache || :

%postun
/sbin/ldconfig
if [ $1 -gt 0 ]; then
  gdk-pixbuf-query-loaders --update-cache || :
fi

%files -f gdk-pixbuf.lang
%defattr(-,root,root,-)
%{_libdir}/libgdk_pixbuf-2.0.so.*
%if %with_x11
%{_libdir}/libgdk_pixbuf_xlib-2.0.so.*
%endif
%{_libdir}/girepository-1.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.so
%ghost %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{_bindir}/gdk-pixbuf-query-loaders
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gdk-pixbuf-2.0
%{_libdir}/libgdk_pixbuf-2.0.so

%if %with_x11
%{_libdir}/libgdk_pixbuf_xlib-2.0.so
%{_libdir}/pkgconfig/gdk-pixbuf-xlib-2.0.pc
%endif

%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_datadir}/gir-1.0
%{_datadir}/gtk-doc/html/*
%{_mandir}/man1/gdk-pixbuf-csource.1*


%changelog
* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to gnome-3.18.1

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

