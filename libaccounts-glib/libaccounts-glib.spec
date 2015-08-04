Name:		libaccounts-glib
Version:	1.18
Release:	1
Group:		System Environment/Libraries
Summary:	Accounts framework for Linux and POSIX based platforms
License:	LGPLv2
URL:		https://gitlab.com/accounts-sso/libaccounts-glib
Source0:	%{name}-%{version}.tar.gz
Patch2:     libaccounts-glib-fix-clang-build.patch

BuildRequires:	dbus-glib-devel
BuildRequires:	libxml2-devel
BuildRequires:	sqlite-devel
BuildRequires:	gobject-introspection-devel
# no needed for final release tarball
BuildRequires:	libtool
BuildRequires:	gtk-doc

%description
%{summary}.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package docs
Summary:	Documentation for %{name}
BuildArch:	noarch

%description docs
The %{name}-docs package contains documentation for %{name}.

%prep
%setup -q

%build
gtkdocize
autoreconf -i --force
%configure --disable-static \
	--disable-gtk-doc

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la

# add docs manuall to %%doc instead
rm -rf %{buildroot}%{_prefix}/doc/reference

# remove tests for now
rm -f %{buildroot}%{_bindir}/*test*
rm -rf %{buildroot}%{_datadir}/libaccounts-glib0-test
rm -rf $RPM_BUILD_ROOT%{_datadir}/libaccounts-glib/testdata
rm -rf $RPM_BUILD_ROOT%{_libdir}/libaccounts-glib/*test*

rpmclean

%check
make check ||:

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS INSTALL ChangeLog README NEWS
%{_bindir}/ag-backup
%{_bindir}/ag-tool
%{_mandir}/man1/ag-backup.1.gz
%{_mandir}/man1/ag-tool.1.gz
%dir %{_datadir}/backup-framework
%dir %{_datadir}/backup-framework/applications
%{_datadir}/backup-framework/applications/*.conf
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0/Accounts-1.0.typelib
%dir %{_datadir}/xml/
%dir %{_datadir}/xml/accounts/
%dir %{_datadir}/xml/accounts/schema/
%dir %{_datadir}/xml/accounts/schema/dtd
%{_datadir}/xml/accounts/schema/dtd/accounts-*.dtd
%{_libdir}/python2.7/site-packages/gi/overrides/Accounts.py
%{_libdir}/python2.7/site-packages/gi/overrides/Accounts.pyc
%{_libdir}/python2.7/site-packages/gi/overrides/Accounts.pyo

%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}
%{_datadir}/gir-1.0/Accounts-1.0.gir
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/vala/vapi/libaccounts-glib.deps
%{_datadir}/vala/vapi/libaccounts-glib.vapi

%files docs
%doc %{_datadir}/gtk-doc/html/libaccounts-glib/

%changelog
