Name: libdaemon
Version: 0.14
Release: 5
Summary: library for writing UNIX daemons

License: GPL 
URL: http://0pointer.de/lennart/projects/libdaemon/
Source0: http://0pointer.de/lennart/projects/libdaemon/%{name}-%{version}.tar.gz
Patch0: libdaemon-fix-header.patch

# Requires lynx to build the docs

%description
libdaemon is a lightweight C library which eases the writing of UNIX daemons.
It consists of the following parts:
* A wrapper around fork() which does the correct daemonization
  procedure of a process
* A wrapper around syslog() for simpler and compatible log output to
  Syslog or STDERR
* An API for writing PID files
* An API for serializing UNIX signals into a pipe for usage with
  select() or poll()
* An API for running subprocesses with STDOUT and STDERR redirected
  to syslog.

%package devel
Summary: libraries and header files for libdaemon development
Requires: libdaemon = %{version}

%description devel
The libdaemon-devel package contains the header files and libraries
necessary for developing programs using libdaemon.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-static --disable-lynx
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*so.*

%files devel
%defattr(-,root,root)
%doc doc/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.14-5
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

