Summary: Utilities for devices that use SCSI command sets
Name: sg3_utils
Version: 1.41
Release: 1
License: GPLv2+ and BSD
Group: Applications/System
Source0: http://sg.danny.cz/sg/p/sg3_utils-%{version}b4r644.tar.xz
URL: http://sg.danny.cz/sg/sg3_utils.html
Requires: %{name}-libs = %{version}-%{release}

%description
Collection of Linux utilities for devices that use the SCSI command set.
Includes utilities to copy data based on "dd" syntax and semantics (called
sg_dd, sgp_dd and sgm_dd); check INQUIRY data and VPD pages (sg_inq); check
mode and log pages (sginfo, sg_modes and sg_logs); spin up and down
disks (sg_start); do self tests (sg_senddiag); and various other functions.
See the README, CHANGELOG and COVERAGE files. Requires the linux kernel 2.4
series or later. In the 2.4 series SCSI generic device names (e.g. /dev/sg0)
must be used. In the 2.6 series other device names may be used as
well (e.g. /dev/sda).

Warning: Some of these tools access the internals of your system
and the incorrect usage of them may render your system inoperable.

%package libs
Summary: Shared library for %{name}
Group: System Environment/Libraries

%description libs
This package contains the shared library for %{name}.

%package devel
Summary: Development library and header files for the sg3_utils library
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package contains the %{name} library and its header files for
developing applications.

%prep
%setup -q -n %{name}-%{version}b4r644

%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man8/*

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/scsi/*.h
%{_libdir}/*.so


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

