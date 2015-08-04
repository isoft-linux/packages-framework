%global needs_multilib_quirk 0 

%global _hardened_build 1

%global udevrulesdir %{_prefix}/lib/udev/rules.d

%global libusb1 1

%define __provides_exclude_from ^%{_libdir}/sane/.*\.so.*$
%define __requires_exclude ^libsane-.*\.so\.[0-9]*(\(\).*)?+$

%define _maindocdir %{_docdir}/%{name}
%define _docdocdir %{_docdir}/%{name}-doc

Summary: Scanner access software
Name: sane-backends
Version: 1.0.24
Release: 20 
# lib/ is LGPLv2+, backends are GPLv2+ with exceptions
# Tools are GPLv2+, docs are public domain
# see LICENSE for details
License: GPLv2+ and GPLv2+ with exceptions and Public Domain
Group: System Environment/Libraries
Source0: ftp://ftp.sane-project.org/pub/sane/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1: sane.png

Patch0: sane-backends-1.0.23-udev.patch
# Upstreamed at: https://alioth.debian.org/tracker/index.php?func=detail&aid=313040
Patch1: sane-backends-1.0.21-epson-expression800.patch
# Upstreamed at: https://alioth.debian.org/tracker/index.php?func=detail&aid=313043
Patch3: sane-backends-1.0.23-soname.patch


URL: http://www.sane-project.org

%if %libusb1
BuildRequires: libusbx-devel
%else
BuildRequires: libusb-devel
%endif
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: v4l-utils-devel
BuildRequires: gettext
BuildRequires: gphoto2-devel
Requires: systemd >= 183
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Scanner Access Now Easy (SANE) is a universal scanner interface.  The
SANE application programming interface (API) provides standardized
access to any raster image scanner hardware (flatbed scanner,
hand-held scanner, video and still cameras, frame-grabbers, etc.).

%package doc
Summary: SANE backends documentation
Group: Documentation
BuildArch: noarch

%description doc
This package contains documentation for SANE backends.

%package libs
Summary: SANE libraries
Group: System Environment/Libraries

%description libs
This package contains the SANE libraries which are needed by applications that
want to access scanners.

%package devel
Summary: SANE development toolkit
Group: Development/Libraries
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if %libusb1
Requires: libusbx-devel
%else
Requires: libusb-devel
%endif
Requires: libjpeg-devel
Requires: libtiff-devel
Requires: pkgconfig

%description devel
This package contains libraries and header files for writing Scanner Access Now
Easy (SANE) modules.

%package drivers-scanners
Summary: SANE backend drivers for scanners
Group: System Environment/Libraries
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description drivers-scanners
This package contains backend drivers to access scanner hardware through SANE.

%package drivers-cameras
Summary: Scanner backend drivers for digital cameras
Group: System Environment/Libraries
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description drivers-cameras
This package contains backend drivers to access digital cameras through SANE.

%prep
%setup -q

%patch0 -p1 -b .udev
%patch1 -p1 -b .epson-expression800
%patch3 -p1 -b .soname

%build
%configure \
    --with-gphoto2=%{_prefix} \
    --with-docdir=%{_maindocdir} \
    --disable-locking --disable-rpath \
%if %libusb1
    --enable-libusb_1_0 \
%endif
    --enable-pthread

make %{?_smp_mflags}

# Ensure ACL style udev rules
_topdir="$PWD"
pushd tools
./sane-desc -m udev+acl -s "${_topdir}/doc/descriptions:${_topdir}/doc/descriptions-external" -d0 > udev/libsane.rules
popd

%install
make DESTDIR="%{buildroot}" install

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps
rm -f %{buildroot}%{_bindir}/gamma4scanimage
rm -f %{buildroot}%{_mandir}/man1/gamma4scanimage.1*
rm -f %{buildroot}%{_libdir}/sane/*.a %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/libsane*.la %{buildroot}%{_libdir}/sane/*.la

mkdir -p %{buildroot}%{udevrulesdir}
install -m 0644 tools/udev/libsane.rules %{buildroot}%{udevrulesdir}/65-libsane.rules

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m 0644 tools/sane-backends.pc %{buildroot}%{_libdir}/pkgconfig/

mkdir %{buildroot}%{_docdocdir}
pushd %{buildroot}%{_maindocdir}
for f in *; do
    if [ -d "$f" ]; then
        mv "$f" "%{buildroot}%{_docdocdir}/${f}"
    else
        case "$f" in
        AUTHORS|ChangeLog|COPYING|LICENSE|NEWS|PROBLEMS|README|README.linux)
            ;;
        backend-writing.txt|PROJECTS|sane-*.html)
            mv "$f" "%{buildroot}%{_docdocdir}/${f}"
            ;;
        *)
            rm -rf "$f"
            ;;
        esac
    fi
done
popd

%find_lang %name

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc %{_maindocdir}
%dir /etc/sane.d
%dir /etc/sane.d/dll.d
%config(noreplace) /etc/sane.d/*.conf
%{udevrulesdir}/65-libsane.rules
%{_datadir}/pixmaps/sane.png

%{_bindir}/sane-find-scanner
%{_bindir}/scanimage
%{_sbindir}/*

%exclude %{_mandir}/man1/sane-config.1*
%{_mandir}/*/*

%dir %{_libdir}/sane

%files doc
%defattr(-, root, root)
%doc %{_docdocdir}

%files libs
%defattr(-, root, root)
%{_libdir}/libsane*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/sane-config
%{_mandir}/man1/sane-config.1*
%{_includedir}/sane
%{_libdir}/libsane*.so
%{_libdir}/pkgconfig/sane-backends.pc

%files drivers-scanners
%defattr(-, root, root)
%{_libdir}/sane/*.so*
%exclude %{_libdir}/sane/*gphoto2.so*

%files drivers-cameras
%defattr(-, root, root)
%{_libdir}/sane/*gphoto2.so*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

