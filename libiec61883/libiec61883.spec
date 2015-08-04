Summary: Streaming library for IEEE1394
Name: libiec61883
Version: 1.1.0
Release: 2
License: LGPL
Group: Libraries
Source: http://linux1394.org/dl/%{name}-%{version}.tar.gz
Patch: libiec61883-1.1.0-installtests.patch
URL: http://linux1394.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
ExcludeArch: s390 s390x

# Works only with newer libraw1394 versions
BuildRequires: libraw1394-devel >= 1.2.1
BuildRequires: autoconf, automake, libtool
Requires: libraw1394 >= 1.2.1

%description 

The libiec61883 library provides an higher level API for streaming DV,
MPEG-2 and audio over IEEE1394.  Based on the libraw1394 isochronous
functionality, this library acts as a filter that accepts DV-frames,
MPEG-2 frames or audio samples from the application and breaks these
down to isochronous packets, which are transmitted using libraw1394.

%package devel
Summary:  Development files for libiec61883
Group:    Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig, libraw1394-devel >= 1.2.1

%description devel
Development files needed to build applications against libiec61883

%package utils
Summary:  Utilities for use with libiec61883
Group:    Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description utils
Utilities that make use of iec61883

%prep
%setup -q
%patch -p1 -b .installtests

%build
autoreconf -if
export CFLAGS="%{optflags}"
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm $RPM_BUILD_ROOT%{_libdir}/libiec61883.a
rm $RPM_BUILD_ROOT%{_libdir}/libiec61883.la
rpmclean
%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_libdir}/libiec61883.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libiec61883.so
%{_includedir}/libiec61883/*.h
%{_libdir}/pkgconfig/libiec61883.pc

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

