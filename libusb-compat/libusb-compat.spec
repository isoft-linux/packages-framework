Name: libusb-compat
Epoch: 1
Version: 0.1.5
Release: 1
Summary: A library which allows userspace access to USB devices
Group: System Environment/Libraries
License: LGPLv2+
URL: http://sourceforge.net/projects/libusb/
Source0: http://prdownloads.sourceforge.net/libusb/libusb-compat-%{version}.tar.bz2

BuildRequires: libusb-devel

%description
This package provides a way for applications to access USB devices.
Legacy libusb-0.1 is no longer supported by upstream, therefore content of this
package was replaced by libusb-compat. It provides compatibility layer allowing
applications written for libusb-0.1 to work with libusb-1.0.

%package devel
Summary: Development files for libusb
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files, libraries and documentation needed to
develop applications that use libusb-0.1. However new applications should use
libusb-1.0 library instead of this one.

%package static
Summary: Static development files for libusb
Group: Development/Libraries
Requires: %{name}-devel = %{epoch}:%{version}-%{release}

%description static
This package contains static libraries needed to develop applications that use
libusb-0.1. However new applications should use libusb-1.0 library instead of
this one.

%prep
%setup -q -n libusb-compat-%{version}

%build
%configure 
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libusb-0.1.so.*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README
%{_includedir}/usb.h
%{_libdir}/libusb.so
%{_libdir}/pkgconfig/libusb.pc
%{_bindir}/libusb-config

%files static
%defattr(-,root,root,-)
%{_libdir}/libusb.a



%changelog
* Wed Dec 04 2013 Cjacker <cjacker@gmail.com>
- first build for new OS
