Summary: Audio/Video Control library for IEEE-1394 devices
Name: libavc1394
Version: 0.5.4
Release: 4 
License: LGPL
Group: System Environment/Libraries
Source: http://dl.sourceforge.net/libavc1394/libavc1394-%{version}.tar.gz
Patch1: libavc1394-automake.patch
BuildRequires: libraw1394-devel
BuildRequires: autoconf automake libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-root
ExcludeArch: s390 s390x

%description
The libavc1394 library allows utilities to control IEEE-1394 devices
using the AV/C specification.  Audio/Video Control allows applications
to control devices like the tape on a VCR or camcorder.

%package devel
Summary: Development libs for libavc1394
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libraw1394-devel

%description devel
Development libraries required to build applications using libavc1394.

%prep
%setup -q
%patch1 -p1

%build
autoreconf -f -i
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README ChangeLog
%{_bindir}/dvcont
%{_bindir}/mkrfc2734
%{_libdir}/libavc1394.so.*
%{_libdir}/librom1394.so.*
%{_mandir}/man1/dvcont.1.gz
%{_mandir}/man1/mkrfc2734.1*


%files devel
%defattr(-,root,root,-)
%{_includedir}/libavc1394/
%{_libdir}/pkgconfig/libavc1394.pc
%{_libdir}/libavc1394.so
%{_libdir}/librom1394.so

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

