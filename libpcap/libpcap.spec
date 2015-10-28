Name: libpcap
Version: 1.7.4
Release: 2 
Summary: A system-independent interface for user-level packet capture
License: BSD with advertising
URL: http://www.tcpdump.org
BuildRequires: bison flex

Source:  http://www.tcpdump.org/release/%{name}-%{version}.tar.gz

%description
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.

%package devel
Summary: Libraries and header files for the libpcap library
Requires: %{name} = %{version}-%{release}

%description devel
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

This package provides the libraries, include files, and other
resources needed for developing libpcap applications.

%prep
%setup -q

%build
%configure \
    --disable-bluetooth

make %{?_smp_mflags}

%install

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/libpcap.a


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libpcap.so.*
%{_mandir}/man7/pcap*.7*

%files devel
%defattr(-,root,root)
%{_bindir}/pcap-config
%{_includedir}/pcap*.h
%{_includedir}/pcap
%{_libdir}/libpcap.so
%{_mandir}/man1/pcap-config.1*
%{_mandir}/man3/pcap*.3*
%{_mandir}/man5/pcap*.5*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.7.4-2
- Rebuild for new 4.0 release.

* Mon Jul 20 2015 Cjacker <cjacker@foxmail.com>
- update to 1.7.4
