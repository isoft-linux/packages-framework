Name: libtevent
Version: 0.9.26
Release: 2%{?dist}
Summary: The tevent library
License: LGPLv3+
URL: http://tevent.samba.org/
Source: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz

BuildRequires: libtalloc-devel >= 2.0.7
BuildRequires: python-devel
BuildRequires: pytalloc-devel >= 2.0.7
BuildRequires: doxygen
BuildRequires: docbook-style-xsl
BuildRequires: libxslt

Provides: bundled(libreplace)

%description
Tevent is an event system based on the talloc memory management library.
Tevent has support for many event types, including timers, signals, and
the classic file descriptor events.
Tevent also provide helpers to deal with asynchronous code providing the
tevent_req (Tevent Request) functions.

%package devel
Summary: Developer tools for the Tevent library
Requires: libtevent%{?_isa} = %{version}-%{release}
Requires: libtalloc-devel%{?_isa} >= 2.0.7
Requires: pkgconfig

%description devel
Header files needed to develop programs that link against the Tevent library.


%package -n python-tevent
Summary: Python bindings for the Tevent library
Requires: libtevent%{?_isa} = %{version}-%{release}

%description -n python-tevent
Python bindings for libtevent

%prep
# Update timestamps on the files touched by a patch, to avoid non-equal
# .pyc/.pyo files across the multilib peers within a build, where "Level"
# is the patch prefix option (e.g. -p1)
# Taken from specfile for python-simplejson
UpdateTimestamps() {
  Level=$1
  PatchFile=$2

  # Locate the affected files:
  for f in $(diffstat $Level -l $PatchFile); do
    # Set the files to have the same timestamp as that of the patch:
    touch -r $PatchFile $f
  done
}

%setup -q -n tevent-%{version}

%build
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace

make %{?_smp_mflags} V=1

doxygen doxy.config

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtevent.a

# Install API docs
rm -f doc/man/man3/todo*
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libtevent.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/tevent.h
%{_libdir}/libtevent.so
%{_libdir}/pkgconfig/tevent.pc
%{_mandir}/man3/tevent*.gz

%files -n python-tevent
%defattr(-,root,root,-)
%{python_sitearch}/tevent.py*
%{python_sitearch}/_tevent.so


%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 0.9.26-2
- Initial build

