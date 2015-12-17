Name: libtalloc
Version: 2.1.5
Release: 2%{?dist}
Summary: The talloc library
License: LGPLv3+
URL: http://talloc.samba.org/
Source: http://samba.org/ftp/talloc/talloc-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python2-devel
BuildRequires: python3-devel
BuildRequires: doxygen

Provides: bundled(libreplace)

# Patches

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Talloc library.

%package -n python-talloc
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}
Provides: pytalloc%{?_isa} = %{version}-%{release}
Provides: pytalloc = %{version}-%{release}
Obsoletes: pytalloc < 2.1.3

%description -n python-talloc
Python libraries for creating bindings using talloc

%package -n python-talloc-devel
Summary: Development libraries for python-talloc
Requires: python-talloc = %{version}-%{release}
Provides: pytalloc-devel%{?_isa} = %{version}-%{release}
Provides: pytalloc-devel = %{version}-%{release}
Obsoletes: pytalloc-devel < 2.1.3

%description -n python-talloc-devel
Development libraries for python-talloc

%package -n python3-talloc
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description -n python3-talloc
Python 3 libraries for creating bindings using talloc

%package -n python3-talloc-devel
Summary: Development libraries for python3-talloc
Requires: python3-talloc = %{version}-%{release}

%description -n python3-talloc-devel
Development libraries for python3-talloc

%prep
%setup -q -n talloc-%{version}

%build
%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules \
           --extra-python=%{__python3}

make %{?_smp_mflags} V=1
doxygen doxy.config

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtalloc.a
rm -f $RPM_BUILD_ROOT/usr/share/swig/*/talloc.i

# Install API docs
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n python-talloc -p /sbin/ldconfig
%postun -n python-talloc -p /sbin/ldconfig

%post -n python3-talloc -p /sbin/ldconfig
%postun -n python3-talloc -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libtalloc.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3.gz
%{_mandir}/man3/libtalloc*.3.gz

%files -n python-talloc
%defattr(-,root,root,-)
%{_libdir}/libpytalloc-util.so.*
%{python_sitearch}/talloc.so

%files -n python-talloc-devel
%defattr(-,root,root,-)
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc
%{_libdir}/libpytalloc-util.so

%files -n python3-talloc
%defattr(-,root,root,-)
%{_libdir}/libpytalloc-util.cpython*.so.*
%{python3_sitearch}/talloc.cpython*.so

%files -n python3-talloc-devel
%defattr(-,root,root,-)
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc
%{_libdir}/libpytalloc-util.cpython*.so


%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 2.1.5-2
- Initial build

