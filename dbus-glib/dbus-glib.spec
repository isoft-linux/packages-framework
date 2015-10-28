%define gettext_package dbus

%define expat_version           1.95.5
%define glib2_version           2.2.0
%define gtk2_version 2.4.0
%define dbus_version 0.90

Summary: GLib bindings for D-Bus
Name: dbus-glib
Version: 0.104
Release: 4 
URL: http://www.freedesktop.org/software/dbus/
Source0: http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
License: AFL and GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: expat-devel >= %{expat_version}
#BuildRequires: libxml2-devel
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gettext
BuildRequires: autoconf

# this patch requires autoreconf
BuildRequires: autoconf automake libtool gettext-devel

%description

D-Bus add-on library to integrate the standard D-Bus library with
the GLib thread abstraction and main loop.

%package devel
Summary: Libraries and headers for the D-Bus GLib bindings
Requires: %name = %{version}-%{release}
Requires: glib2-devel 
Requires: dbus-devel 
Requires: pkgconfig
Obsoletes: dbus-devel < 0.90

%description devel

Headers and static libraries for the D-Bus GLib bindings 

%if 0
%package gtk
Summary: GTK based tools
Requires: %name = %{version}-%{release}
Requires: gtk2 >= %{gtk_version}
%description gtk
D-Bus tools written using the gtk+ GUI libaries

%endif

%prep
%setup -q
#%patch0 -p1
%build
%configure --disable-tests \
	--enable-verbose-mode=yes \
	--enable-asserts=yes \
	--disable-gtk-doc

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)

%doc COPYING ChangeLog NEWS

%{_libdir}/*glib*.so.*
%{_bindir}/dbus-binding-tool

%files devel
%defattr(-,root,root)

%{_libdir}/lib*.so
%{_libdir}/pkgconfig/dbus-glib-1.pc
%{_includedir}/*
%{_datadir}/gtk-doc/html/dbus-glib
%{_sysconfdir}/bash_completion.d/dbus-bash-completion.sh
%{_libexecdir}/dbus-bash-completion-helper
%{_mandir}/*
%if 0
%files gtk
%defattr(-,root,root)

%{_bindir}/dbus-viewer

%endif

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.104-4
- Rebuild for new 4.0 release.

