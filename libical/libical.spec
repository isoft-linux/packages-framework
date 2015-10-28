Summary:	Reference implementation of the iCalendar data type and serialization format
Name:		libical
Version:    1.0	
Release:	5
License:	LGPLv2 or MPLv1.1
URL:		http://freeassociation.sourceforge.net/
Source:		http://downloads.sourceforge.net/freeassociation/%{name}-%{version}.tar.gz
Requires:	tzdata
BuildRequires:	bison, byacc, flex
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Reference implementation of the iCalendar data type and serialization format
used in dozens of calendaring and scheduling products.

%package devel
Summary:	Development files for libical
Requires:	%{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The libical-devel package contains libraries and header files for developing 
applications that use libical.

%prep
%setup -q

%build
libtoolize -if
./autogen.sh
%configure --disable-static --enable-reentrant --with-backtrace
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README THANKS
%{_libdir}/%{name}.so.*
%{_libdir}/libicalss.so.*
%{_libdir}/libicalvcal.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/UsingLibical.txt
%{_includedir}/ical.h
%{_libdir}/%{name}.so
%{_libdir}/libicalss.so
%{_libdir}/libicalvcal.so
%{_libdir}/pkgconfig/libical.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/ical*.h
%{_includedir}/%{name}/pvl.h
%{_includedir}/%{name}/sspm.h
%{_includedir}/%{name}/port.h
%{_includedir}/%{name}/vcaltmp.h
%{_includedir}/%{name}/vcc.h
%{_includedir}/%{name}/vobject.h

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0-5
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

