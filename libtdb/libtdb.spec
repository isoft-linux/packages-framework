Name: libtdb
Version: 1.3.8
Release: 2%{?dist}
Summary: The tdb library
License: LGPLv3+
URL: http://tdb.samba.org/
Source: http://samba.org/ftp/tdb/tdb-%{version}.tar.gz

BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python2-devel
BuildRequires: python3-devel

Provides: bundled(libreplace)

%description
A library that implements a trivial database.

%package devel
Summary: Header files need to link the Tdb library
Requires: libtdb = %{version}-%{release}
Requires: pkgconfig

%description devel
Header files needed to develop programs that link against the Tdb library.

%package -n tdb-tools
Summary: Developer tools for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n tdb-tools
Tools to manage Tdb files

%package -n python-tdb
Summary: Python bindings for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n python-tdb
Python bindings for libtdb

%package -n python3-tdb
Summary: Python3 bindings for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n python3-tdb
Python3 bindings for libtdb

%prep
%setup -q -n tdb-%{version}

%build
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --extra-python=%{__python3}
make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtdb.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n python-tdb -p /sbin/ldconfig
%postun -n python-tdb -p /sbin/ldconfig

%post -n python3-tdb -p /sbin/ldconfig
%postun -n python3-tdb -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libtdb.so.*

%files devel
%defattr(-,root,root)
%doc docs/README
%{_includedir}/tdb.h
%{_libdir}/libtdb.so
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-tools
%defattr(-,root,root,-)
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_bindir}/tdbrestore
%{_mandir}/man8/tdbbackup.8*
%{_mandir}/man8/tdbdump.8*
%{_mandir}/man8/tdbtool.8*
%{_mandir}/man8/tdbrestore.8*

%files -n python-tdb
%defattr(-,root,root,-)
%{python_sitearch}/tdb.so
%{python_sitearch}/_tdb_text.py*

%files -n python3-tdb
%defattr(-,root,root,-)
%{python3_sitearch}/__pycache__/_tdb_text.cpython*.py[co]
%{python3_sitearch}/tdb.cpython*.so
%{python3_sitearch}/_tdb_text.py

%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 1.3.8-2
- Initial build

