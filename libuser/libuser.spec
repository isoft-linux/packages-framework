Name: libuser
Version: 0.62
Release: 2%{?dist}
Group: System Environment/Base
License: LGPLv2+
URL: https://fedorahosted.org/libuser/
Source: https://fedorahosted.org/releases/l/i/libuser/libuser-%{version}.tar.xz
BuildRequires: glib2-devel, linuxdoc-tools, pam-devel, popt-devel, python2-devel
BuildRequires: cyrus-sasl-devel, python3-devel
Summary: A user and group account administration library

%global __provides_exclude_from ^(%{_libdir}/%{name}|%{python2_sitearch}|%{python3_sitearch})/.*$

%description
The libuser library implements a standardized interface for manipulating
and administering user and group accounts.  The library uses pluggable
back-ends to interface to its data sources.

Sample applications modeled after those included with the shadow password
suite are included.

%package devel
Group: Development/Libraries
Summary: Files needed for developing applications which use libuser
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel%{?_isa}

%description devel
The libuser-devel package contains header files, static libraries, and other
files useful for developing applications with libuser.

%package python
Summary: Python 2 bindings for the libuser library
Group: Development/Libraries
Requires: libuser%{?_isa} = %{version}-%{release}

%description python
The libuser-python package contains the Python 2 bindings for
the libuser library, which provides a Python 2 API for manipulating and
administering user and group accounts.

%package python3
Summary: Python 3 bindings for the libuser library
Group: Development/Libraries
Requires: libuser%{?_isa} = %{version}-%{release}

%description python3
The libuser-python3 package contains the Python bindings for
the libuser library, which provides a Python 3 API for manipulating and
administering user and group accounts.

%prep
%setup -qc
mv libuser-%{version} python2
cp -a python2 python3

pushd python2
cp -pr COPYING AUTHORS NEWS README TODO docs ..
popd


%build
pushd python2
%configure --without-selinux --without-ldap --with-html-dir=%{_datadir}/gtk-doc/html
make
popd

pushd python3
%configure --without-selinux --without-ldap --with-html-dir=%{_datadir}/gtk-doc/html \
	PYTHON=/usr/bin/python3
make
popd


%install
# There should not be any Python dependencies in the common files; install the
# python2 version second, just to be sure.
make -C python3 install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
make -C python2 install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%find_lang %{name}

%check

make -C python2 check || { cat python2/test-suite.log; false; }
# The Python 3 module only supports UTF-8
LC_ALL=en_US.UTF-8 make -C python3 check \
	|| { cat python3/test-suite.log; false; }

# Verify that all python modules load, just in case.
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH
cd $RPM_BUILD_ROOT/%{python2_sitearch}
python2 -c "import libuser"
cd $RPM_BUILD_ROOT/%{python3_sitearch}
# The Python 3 module only supports UTF-8
LC_ALL=en_US.UTF-8 python3 -c "import libuser"


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README TODO docs/*.txt
%config(noreplace) %{_sysconfdir}/libuser.conf

%attr(0755,root,root) %{_bindir}/*
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%attr(0755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%exclude %{_libdir}/*.la
%exclude %{_libdir}/%{name}/*.la

%files python
%doc python2/python/modules.txt
%{python2_sitearch}/*.so
%exclude %{python2_sitearch}/*.la

%files python3
%doc python3/python/modules.txt
%{python3_sitearch}/*.so
%exclude %{python3_sitearch}/*.la

%files devel
%{_includedir}/libuser
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*

%changelog
* Sat Jul 25 2015 Cjacker <cjacker@foxmail.com>
- Update to libuser-0.62
- Resolves: #1246225 (CVE-2015-3245, CVE-2015-3246)
