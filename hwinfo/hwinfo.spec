Name:           hwinfo
Summary:        Hardware Library
License:        GPL-2.0+
# Until migration to github this should be correct url
Url:            http://gitorious.org/opensuse/hwinfo
Version:        21.17
Release:        2.1
Source:         %{name}-%{version}.tar.xz
BuildRequires:  doxygen
BuildRequires:  flex
BuildRequires:  perl-XML-Parser
BuildRequires:  pkgconfig
BuildRequires:  udev
%ifarch %ix86 x86_64
BuildRequires:  libx86emu-devel
%endif
Provides:       libhd
Obsoletes:      libhd
PreReq:         /sbin/ldconfig

%description
A simple program that lists results from the hardware detection
library.



%package      devel
Summary:        Hardware Detection Library
Provides:       libhddev
Obsoletes:      libhddev
Requires:       %name = %version
Requires:       perl-XML-Parser
Requires:       udev
Requires:       wireless-tools
Requires:       expat-devel

%description devel
This library collects information about the hardware installed on a
system.



%prep
%setup

%build
  make static
  # make copy of static library for installation
  cp src/libhd.a .
  make clean
  make LIBDIR=%{_libdir}
  make doc

%install
  make install DESTDIR=%{buildroot} LIBDIR=%{_libdir}
  install -m 644 libhd.a %{buildroot}%{_libdir}
  install -d -m 755 %{buildroot}%{_mandir}/man8/
  install -d -m 755 %{buildroot}%{_mandir}/man1/
  install -m 644 doc/check_hd.1 %{buildroot}%{_mandir}/man1/
  install -m 644 doc/convert_hd.1 %{buildroot}%{_mandir}/man1/
  install -m 644 doc/getsysinfo.1 %{buildroot}%{_mandir}/man1/
  install -m 644 doc/mk_isdnhwdb.1 %{buildroot}%{_mandir}/man1/
  install -m 644 doc/hwinfo.8 %{buildroot}%{_mandir}/man8/
  mkdir -p %{buildroot}/var/lib/hardware/udi

%clean 
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/sbin/hwinfo
/usr/sbin/mk_isdnhwdb
/usr/sbin/getsysinfo
%{_libdir}/libhd.so.*
%doc README
%doc %{_mandir}/man1/getsysinfo.1*
%doc %{_mandir}/man1/mk_isdnhwdb.1*
%doc %{_mandir}/man8/hwinfo.8*
%dir /var/lib/hardware
%dir /var/lib/hardware/udi
%dir /usr/share/hwinfo
/usr/share/hwinfo/*

%files devel
%defattr(-,root,root)
/usr/sbin/check_hd
/usr/sbin/convert_hd
%doc %{_mandir}/man1/convert_hd.1*
%doc %{_mandir}/man1/check_hd.1*
%{_libdir}/libhd.so
%{_libdir}/libhd.a
%{_libdir}/pkgconfig/hwinfo.pc
/usr/include/hd.h
%doc doc/libhd/html

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 21.17-2.1
- Rebuild for new 4.0 release.

