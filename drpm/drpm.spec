Name:           drpm
Version:        0.2.0
Release:        3%{?dist}
Summary:        A small library for fetching information from deltarpm packages
License:        LGPLv3+
URL:            http://fedorahosted.org/%{name}
Source:         http://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:  librpm-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
BuildRequires:  cmake >= 2.8
BuildRequires:  libcmocka-devel >= 1.0
%ifarch x86_64 %{ix86} %{arm} ppc ppc32 %{power64} s390x aarch64 amd64 mips32 mips64
BuildRequires:  valgrind
%endif

%package devel
Summary:        C interface for the drpm library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description
The drpm package provides a small library allowing one to fetch
various info from deltarpm packages.

%description devel
The drpm-devel package provides a C interface (drpm.h) for the drpm library.

%prep
%setup -q

%build
%cmake .
make %{?_smp_mflags}

%install
%make_install

%check
make check %{?_smp_mflags}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libdrpm.so.*
%license COPYING COPYING.LESSER

%files devel
%{_libdir}/libdrpm.so
%{_includedir}/drpm.h
%{_libdir}/pkgconfig/drpm.pc

%changelog
