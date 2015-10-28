%global udevdir %(pkg-config --variable=udevdir udev)
Name:           libgphoto2
Version:        2.5.8
Release:        2
Summary:        Library for accessing digital cameras
License:        GPLv2+ and GPLv2
URL:            http://www.gphoto.org/
Source0:        http://downloads.sourceforge.net/gphoto/libgphoto2-%{version}.tar.bz2

BuildRequires:  libusbx-devel
BuildRequires:  libjpeg-devel
BuildRequires:  pkgconfig
BuildRequires:  libltdl-devel, popt-devel
BuildRequires:  libexif-devel
BuildRequires:  gd-devel

%description
libgphoto2 is a library that can be used by applications to access
various digital cameras. libgphoto2 itself is not a GUI application,
opposed to gphoto. There are GUI frontends for the gphoto2 library,
however, such as gtkam for example.


%package devel
Summary:        Headers and links to compile against the libgphoto2 library
Requires:       %{name} = %{version}-%{release}
Requires:       libusbx-devel >= 1.0 
Obsoletes:      gphoto2-devel < 2.4.0-11
Provides:       gphoto2-devel = %{version}-%{release}

%description devel
libgphoto2 is a library that can be used by applications to access
various digital cameras. libgphoto2 itself is not a GUI application,
opposed to gphoto. There are GUI frontends for the gphoto2 library,
however, such as gtkam for example.

This package contains files needed to compile applications that
use libgphoto2.


%prep
%setup -q 

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing "

%configure \
	udevscriptdir='%{udevdir}' \
	--with-drivers=all \
	--with-doc-dir=%{_docdir}/%{name} \
	--disable-static \
	--disable-rpath \
    --with-gd \
    --with-libxml2

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

pushd packaging/linux-hotplug/
export LIBDIR=$RPM_BUILD_ROOT%{_libdir}
export CAMLIBS=$RPM_BUILD_ROOT%{_libdir}/%{name}/%{version}
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}

# Output udev rules for device identification; this is used by GVfs gphoto2
# backend and others.
#
mkdir -p $RPM_BUILD_ROOT/etc/udev/rules.d
$RPM_BUILD_ROOT%{_libdir}/%{name}/print-camera-list udev-rules version 136 > $RPM_BUILD_ROOT/etc/udev/rules.d/40-libgphoto2.rules
popd

# remove circular symlink in /usr/include/gphoto2 (#460807)
rm -f %{buildroot}%{_includedir}/gphoto2/gphoto2

# remove unneeded print-camera-list from libdir (#745081)
rm -f %{buildroot}%{_libdir}/libgphoto2/print-camera-list

rm -rf %{buildroot}%{_libdir}/libgphoto2/*/*a
rm -rf %{buildroot}%{_libdir}/libgphoto2_port/*/*a
rm -rf %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_libdir}/*.la

%find_lang %{name}-6
%find_lang %{name}_port-12

cat libgphoto2*.lang >> %{name}.lang


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING README NEWS
%dir %{_libdir}/libgphoto2_port
%dir %{_libdir}/libgphoto2_port/*
%dir %{_libdir}/libgphoto2
%dir %{_libdir}/libgphoto2/*
%{_libdir}/libgphoto2_port/*/*.so
%{_libdir}/libgphoto2/*/*.so
%{_libdir}/*.so.*
/etc/udev/rules.d/40-libgphoto2.rules
%{udevdir}/check-ptp-camera

%files devel
%doc %{_docdir}/%{name}
%{_datadir}/libgphoto2
%{_bindir}/gphoto2-config*
%{_bindir}/gphoto2-port-config
%{_includedir}/gphoto2
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.5.8-2
- Rebuild for new 4.0 release.

* Thu Jul 23 2015 Cjacker <cjacker@foxmail.com>
- update to 2.5.8
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

