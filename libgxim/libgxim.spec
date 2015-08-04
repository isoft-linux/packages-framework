Name:		libgxim
Version:	0.5.0
Release:	5
License:	LGPLv2+
URL:		http://tagoh.bitbucket.org/libgxim/
BuildRequires:	intltool gettext ruby
BuildRequires:	glib2-devel >= 2.26, gtk2-devel
Source0:	http://bitbucket.org/tagoh/%{name}/downloads/%{name}-%{version}.tar.bz2

Summary:	GObject-based XIM protocol library
Group:		System Environment/Libraries

%description
libgxim is a X Input Method protocol library that is implemented by GObject.
this library helps you to implement XIM servers or client applications to
communicate through XIM protocol without using Xlib API directly, particularly
if your application uses GObject-based main loop.

This package contains the shared library.

%package	devel
Summary:	Development files for libgxim
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	glib2-devel >= 2.26.0
Requires:	gtk2-devel

%description	devel
libgxim is a X Input Method protocol library that is implemented by GObject.
this library helps you to implement XIM servers or client applications to
communicate through XIM protocol without using Xlib API directly, particularly
if your application uses GObject-based main loop.

This package contains the development files to make any applications with
libgxim.

%prep
%setup -q


%build
%configure --disable-static --disable-rebuilds

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# clean up the unnecessary files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/libgxim.so.*

%files	devel
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/libgxim.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libgxim
%{_datadir}/gtk-doc/html/libgxim

%changelog
