%define talloc_version 2.0.8
%define tdb_version 1.3.3
%define tevent_version 0.9.17

Name: libldb
Version: 1.1.23
Release: 2%{?dist}
Summary: A schema-less, ldap like, API and database
Requires: libtalloc%{?_isa} >= %{talloc_version}
Requires: libtdb%{?_isa} >= %{tdb_version}
Requires: libtevent%{?_isa} >= %{tevent_version}
License: LGPLv3+
URL: http://ldb.samba.org/
Source: http://samba.org/ftp/ldb/ldb-%{version}.tar.gz

BuildRequires: libtalloc-devel >= %{talloc_version}
BuildRequires: libtdb-devel >= %{tdb_version}
BuildRequires: libtevent-devel >= %{tevent_version}
BuildRequires: popt-devel
BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python-devel
BuildRequires: python-tdb
BuildRequires: pytalloc-devel
BuildRequires: python-tevent
BuildRequires: doxygen
BuildRequires: openldap-devel

Provides: bundled(libreplace)

# Patches

%description
An extensible library that implements an LDAP like API to access remote LDAP
servers, or use local tdb databases.

%package -n ldb-tools
Summary: Tools to manage LDB files
Requires: libldb%{?_isa} = %{version}-%{release}

%description -n ldb-tools
Tools to manage LDB files

%package devel
Summary: Developer tools for the LDB library
Requires: libldb%{?_isa} = %{version}-%{release}
Requires: libtdb-devel%{?_isa} >= %{tdb_version}
Requires: libtalloc-devel%{?_isa} >= %{talloc_version}
Requires: libtevent-devel%{?_isa} >= %{tevent_version}
Requires: pkgconfig

%description devel
Header files needed to develop programs that link against the LDB library.

%package -n pyldb
Summary: Python bindings for the LDB library
Requires: libldb%{?_isa} = %{version}-%{release}
Requires: python-tdb%{?_isa} >= %{tdb_version}

%description -n pyldb
Python bindings for the LDB library

%package -n pyldb-devel
Summary: Development files for the Python bindings for the LDB library
Requires: pyldb%{?_isa} = %{version}-%{release}

%description -n pyldb-devel
Development files for the Python bindings for the LDB library

%prep
%setup -q -n ldb-%{version}

%build

%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --with-modulesdir=%{_libdir}/ldb/modules \
           --with-privatelibdir=%{_libdir}/ldb

# Don't build with multiple processors
# It breaks due to a threading issue in WAF
make V=1
doxygen Doxyfile

%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/libldb.a

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

# Install API docs
cp -a apidocs/man/* $RPM_BUILD_ROOT/%{_mandir}

# LDB 1.1.8+ bug: remove manpage named after full
# file path
rm -f $RPM_BUILD_ROOT/%{_mandir}/man3/_*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n pyldb -p /sbin/ldconfig
%postun -n pyldb -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_libdir}/ldb
%{_libdir}/libldb.so.*
%dir %{_libdir}/ldb/modules
%dir %{_libdir}/ldb/modules/ldb
%{_libdir}/ldb/modules/ldb/*.so

%files -n ldb-tools
%defattr(-,root,root,-)
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%{_libdir}/ldb/libldb-cmdline.so
%{_mandir}/man1/ldbadd.1.*
%{_mandir}/man1/ldbdel.1.*
%{_mandir}/man1/ldbedit.1.*
%{_mandir}/man1/ldbmodify.1.*
%{_mandir}/man1/ldbrename.1.*
%{_mandir}/man1/ldbsearch.1.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/ldb_module.h
%{_includedir}/ldb_handlers.h
%{_includedir}/ldb_errors.h
%{_includedir}/ldb_version.h
%{_includedir}/ldb.h
%{_libdir}/libldb.so

%{_libdir}/pkgconfig/ldb.pc
%{_mandir}/man3/ldb*.gz
%{_mandir}/man3/ldif*.gz

%files -n pyldb
%defattr(-,root,root,-)
%{python_sitearch}/ldb.so
%{_libdir}/libpyldb-util.so.1*
%{python_sitearch}/_ldb_text.py*

%files -n pyldb-devel
%defattr(-,root,root,-)
%{_includedir}/pyldb.h
%{_libdir}/libpyldb-util.so
%{_libdir}/pkgconfig/pyldb-util.pc
%{_mandir}/man*/Py*.gz


%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 1.1.23-2
- Initial build

