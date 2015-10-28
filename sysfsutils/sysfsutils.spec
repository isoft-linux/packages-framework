Name:           sysfsutils
URL:            http://sourceforge.net/projects/linux-diag/
License:        GPLv2
Version:        2.1.0
Release:        19%{?dist}

Summary:        Utilities for interfacing with sysfs
Source0:        http://prdownloads.sourceforge.net/linux-diag/%{name}-%{version}.tar.gz
Patch0:         sysfsutils-2.0.0-redhatify.patch
Patch1:         sysfsutils-2.0.0-class-dup.patch
Patch2:         sysfsutils-2.1.0-get_link.patch
Patch3:         sysfsutils-2.1.0-manpages.patch
Patch4:         sysfsutils-aarch64.patch

%description
This package's purpose is to provide a set of utilities for interfacing
with sysfs.

%package -n libsysfs
Summary: Shared library for interfacing with sysfs
License: LGPLv2+

%description -n libsysfs
Library used in handling linux kernel sysfs mounts and their various files.

%package -n libsysfs-devel
Summary: Static library and headers for libsysfs
License: LGPLv2+
Requires: libsysfs = %{version}-%{release}

%description -n libsysfs-devel
libsysfs-devel provides the header files and static libraries required
to build programs using the libsysfs API.

%prep
%setup -q
%patch0 -p1 -b .redhatify
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure --disable-static --libdir=/%{_lib}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_bindir}/dlist_test $RPM_BUILD_ROOT%{_bindir}/get_bus_devices_list $RPM_BUILD_ROOT%{_bindir}/get_class_dev $RPM_BUILD_ROOT%{_bindir}/get_classdev_parent $RPM_BUILD_ROOT%{_bindir}/get_device $RPM_BUILD_ROOT%{_bindir}/get_driver $RPM_BUILD_ROOT%{_bindir}/testlibsysfs $RPM_BUILD_ROOT%{_bindir}/write_attr
rm -f $RPM_BUILD_ROOT/%{_lib}/*.la

%post -n libsysfs -p /sbin/ldconfig

%postun -n libsysfs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/systool
%{_bindir}/get_module
%{_mandir}/man1/systool.1.gz
%doc COPYING AUTHORS README NEWS CREDITS ChangeLog docs/libsysfs.txt cmd/GPL

%files -n libsysfs
%defattr(-,root,root)
/%{_lib}/libsysfs.so.*
%doc COPYING AUTHORS README NEWS CREDITS ChangeLog docs/libsysfs.txt lib/LGPL

%files -n libsysfs-devel
%defattr(-,root,root)
%dir %{_includedir}/sysfs
%{_includedir}/sysfs/libsysfs.h
%{_includedir}/sysfs/dlist.h
/%{_lib}/libsysfs.so


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.1.0-19
- Rebuild for new 4.0 release.

