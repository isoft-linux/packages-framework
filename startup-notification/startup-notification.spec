Summary: Library for tracking application startup
Name: startup-notification
Version: 0.12
Release: 3 
URL: http://www.freedesktop.org/software/startup-notification/
Source0: %{name}-%{version}.tar.gz
License: LGPL
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libxcb-devel

%description

This package contains libstartup-notification which implements a
startup notification protocol. Using this protocol a desktop
environment can track the launch of an application and provide
feedback such as a busy cursor, among other features.

%package devel
Summary: Development portions of startup-notification
Requires: startup-notification = %{version}-%{release}
Requires: libX11-devel

%description devel

Header files and static libraries for libstartup-notification.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)

## FIXME add when upstream tarball is fixed to contain docs
## doc/startup-notification.txt
%doc AUTHORS COPYING ChangeLog
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root,-)

%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.12-3
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

