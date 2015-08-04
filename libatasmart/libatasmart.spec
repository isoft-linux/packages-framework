Name: libatasmart
Version: 0.19
Release: 4 
Summary: ATA S.M.A.R.T. Disk Health Monitoring Library
Group: System Environment/Libraries
Source0: http://0pointer.de/public/libatasmart-%{version}.tar.xz
License: LGPLv2+
Url: http://git.0pointer.de/?p=libatasmart.git;a=summary
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libudev-devel

%description
A scmall and lightweight parser library for ATA S.M.A.R.T. hard disk
health monitoring.

%package devel
Summary: Development Files for libatasmart Client Development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development Files for libatasmart Client Development

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT \( -name *.a -o -name *.la \) -exec rm {} \;
rm $RPM_BUILD_ROOT%{_docdir}/libatasmart/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README LGPL
%{_libdir}/libatasmart.so.*
%{_sbindir}/skdump
%{_sbindir}/sktest
%{_datadir}/vala/vapi/atasmart.vapi

%files devel
%defattr(-,root,root)
%{_includedir}/atasmart.h
%{_libdir}/libatasmart.so
%{_libdir}/pkgconfig/libatasmart.pc
%doc blob-examples/SAMSUNG* blob-examples/ST* blob-examples/Maxtor* blob-examples/WDC* blob-examples/FUJITSU* blob-examples/INTEL* blob-examples/TOSHIBA* blob-examples/MCC*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

