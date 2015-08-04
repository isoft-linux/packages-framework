Summary:        Library providing low-level IEEE-1394 access
Name:           libraw1394
Version:        2.1.0
Release:        1
License:        LGPLv2+
Group:          System Environment/Libraries
Source:         http://www.kernel.org/pub/linux/libs/ieee1394/%{name}-%{version}.tar.xz
Patch0:         libraw1394-fix-types.patch
URL:            http://www.dennedy.org/libraw1394/
BuildRequires:  autoconf automake libtool kernel-headers

%description
The libraw1394 library provides direct access to the IEEE-1394 bus.
Support for both the obsolete ieee1394 interface and the new firewire
intererface are included, with run-time detection of the active stack.

%package devel
Summary:       Development libs for libraw1394
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}, pkgconfig

%description devel
Development libraries needed to build applications against libraw1394.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc COPYING.LIB README NEWS
%{_bindir}/dumpiso
%{_bindir}/sendiso
%{_bindir}/testlibraw
%{_libdir}/libraw1394.so.*
%{_mandir}/man1/dumpiso.1.gz
%{_mandir}/man1/sendiso.1.gz
%{_mandir}/man1/testlibraw.1.gz
%{_mandir}/man5/isodump.5.gz

%files devel
%defattr(-,root,root,0755)
%doc doc/libraw1394.sgml
%{_includedir}/libraw1394/
%{_libdir}/libraw1394.so
%{_libdir}/pkgconfig/libraw1394.pc


%changelog
* Thu Dec 12 2013 Cjacker <cjacker@gmail.com>
- first build for new release.

