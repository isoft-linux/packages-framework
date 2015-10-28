Summary: 1394-based digital camera control library
Name: libdc1394
Version: 2.2.1
Release: 2
License: LGPLv2+
URL: http://sourceforge.net/projects/libdc1394/
Source: http://downloads.sourceforge.net/project/libdc1394/libdc1394-2/%{version}/libdc1394-%{version}.tar.gz

BuildRequires: kernel-headers
BuildRequires: libraw1394-devel libusb1-devel

%description
Libdc1394 is a library that is intended to provide a high level programming
interface for application developers who wish to control IEEE 1394 based
cameras that conform to the 1394-based Digital Camera Specification.

%package devel
Summary: Header files and libraries for %{name}
Requires: %{name} = %{version}-%{release}, libraw1394-devel
Requires: pkgconfig

%description devel
This package contains the header files and libraries
for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package tools
Summary: Tools for use with %{name}
Requires: %{name} = %{version}-%{release}

%description tools
This package contains tools that are useful when working and
developing with %{name}.

%prep
%setup -q -n libdc1394-%{version}

%build
%configure --disable-static --disable-doxygen-html --disable-doxygen-dot
#fix rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_libdir}/libdc1394*.so.*

%files devel
%defattr(-, root, root, 0755)
%doc examples/*.h examples/*.c
%{_includedir}/dc1394/
%{_libdir}/libdc1394*.so
%{_libdir}/pkgconfig/%{name}-2.pc

%files tools
%defattr(-, root, root, 0755)
%{_bindir}/dc1394_*
%{_mandir}/man1/dc1394_*.1.gz

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.2.1-2
- Rebuild for new 4.0 release.

* Thu Dec 12 2013 Cjacker <cjacker@gmail.com>
- first build for new release.

