%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           libmtp
Version:        1.1.9
Release:        1 
Summary:        A software library for MTP media players
URL:            http://libmtp.sourceforge.net/

Group:          System Environment/Libraries
Source0:        http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
License:        LGPLv2+
Requires:       udev
BuildRequires:  libusb1-devel
BuildRequires:  doxygen
Obsoletes:	libmtp-hal

%description
This package provides a software library for communicating with MTP
(Media Transfer Protocol) media players, typically audio players, video
players etc.

%package examples
Summary:        Example programs for libmtp
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description examples
This package provides example programs for communicating with MTP
devices.

%package devel
Summary:        Development files for libmtp
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       libusb1-devel

%description devel
This package provides development files for the libmtp
library for MTP media players.

%prep
%setup -q

%build
%configure --disable-static \
	   --disable-mtpz \
	   --with-udev-rules=69-libmtp.rules
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# Remove libtool archive remnant
rm -f $RPM_BUILD_ROOT%{_libdir}/libmtp.la
# Replace links with relative links
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-delfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-getfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-newfolder
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-sendfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-sendtr
pushd $RPM_BUILD_ROOT%{_bindir}
ln -sf mtp-connect mtp-delfile
ln -sf mtp-connect mtp-getfile
ln -sf mtp-connect mtp-newfolder
ln -sf mtp-connect mtp-sendfile
ln -sf mtp-connect mtp-sendtr
popd
# Copy documentation to a good place
mkdir -p -m 755 $RPM_BUILD_ROOT%{_pkgdocdir}
install -p -m 644 AUTHORS ChangeLog COPYING INSTALL README TODO \
      $RPM_BUILD_ROOT%{_pkgdocdir}
# Touch generated files to make them always have the same time stamp.
touch -r configure.ac \
      $RPM_BUILD_ROOT%{_includedir}/*.h \
      $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*.pc \

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root,root,-)
%dir %{_pkgdocdir}
%{_pkgdocdir}/COPYING
%{_libdir}/libmtp.so.9*
%{_libdir}/udev/rules.d/*
%{_libdir}/udev/mtp-probe
%{_libdir}/udev/hwdb.d/69-libmtp.hwdb
%files examples
%defattr(-,root,root,-)
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmtp.so
%{_pkgdocdir}/*
%exclude %{_pkgdocdir}/COPYING
%{_includedir}/*.h
%{_libdir}/pkgconfig/libmtp.pc


%changelog
