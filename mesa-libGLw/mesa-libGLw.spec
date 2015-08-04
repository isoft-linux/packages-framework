Summary: Xt / Motif OpenGL widgets
Name: mesa-libGLw
Version: 8.0.0
Release: 6%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org
Source0: ftp://ftp.freedesktop.org/pub/mesa/glw/glw-%{version}.tar.bz2

BuildRequires: libXt-devel
BuildRequires: libGL-devel
BuildRequires: openmotif-devel

Provides: libGLw

%description
Mesa libGLw runtime library.

%package devel
Summary: Mesa libGLw development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libGL-devel
Requires: openmotif-devel
Provides: libGLw-devel

%description devel
Mesa libGLw development package.

%prep
%setup -q -n glw-%{version}

%build
%configure --disable-static --enable-motif
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libGLw.so.1
%{_libdir}/libGLw.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/libGLw.so
%{_libdir}/pkgconfig/glw.pc
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h

%changelog
