Summary: Common Access Card (CAC) Emulation Development library
Name:    libcacard 
Version: 2.5.0
Release: 2 
License: GPLv2+ and LGPLv2+ and BSD
URL: http://www.qemu.org/
Source0: %{name}-%{version}.tar.xz

BuildRequires: nss-devel glib2-devel

#if we need re-generate configure
BuildRequires: autoconf automake libtool

%description
Common Access Card (CAC) Emulation

%package devel
Summary:   CAC Emulation devel
Requires:  %{name} = %{version}-%{release}

%description devel
Common Access Card (CAC) Emulation Development library

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/vscclient
%{_libdir}/libcacard.so.*


%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcacard.so
%dir %{_includedir}/cacard
%{_includedir}/cacard/*

%changelog
* Sun Nov 15 2015 Cjacker <cjacker@foxmail.com> - 2.5.0-2
- libcacard now is seperated from qemu and released standalone.

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.4.0-2
- Rebuild for new 4.0 release.

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 2.4.0
