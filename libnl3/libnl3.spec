Summary: Convenience library for kernel netlink sockets
License: LGPLv2
Name: libnl3
Version: 3.2.25
Release: 1
URL: http://www.infradead.org/~tgr/libnl/
Group:  Framework/Runtime/Library 
Source: http://www.infradead.org/~tgr/libnl/files/libnl-%{version}.tar.gz
Source1: http://www.infradead.org/~tgr/libnl/files/libnl-doc-%{version}.tar.gz

BuildRequires: flex bison
BuildRequires: python

%description
This package contains a convenience library to simplify
using the Linux kernel's netlink sockets interface for
network manipulation

%package devel
Summary: Libraries and headers for using libnl3
Group:  Framework/Development/Library
Requires: %{name} = %{version}-%{release}
Requires: %{name}-cli = %{version}-%{release}
Requires: kernel-headers

%description devel
This package contains various headers for using libnl3

%package cli
Summary: Command line interface utils for libnl3
Group:  Framework/Runtime/Utility
Requires: %{name} = %{version}-%{release}

%description cli
This package contains various libnl3 utils and additional
libraries on which they depend

%package doc
Summary: API documentation for libnl3
Group:  Framework/Development/Document 
Requires: %{name} = %{version}-%{release}

%description doc
This package contains libnl3 API documentation

%prep
%setup -q -n libnl-%{version}
tar -xzf %SOURCE1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rpmclean

%check
make check

%post -p /sbin/ldconfig
%post cli -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%postun cli -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%exclude %{_libdir}/libnl-cli*.so.*
%{_libdir}/libnl-*.so.*
%config(noreplace) %{_sysconfdir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libnl3/netlink/
%dir %{_includedir}/libnl3/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files cli
%defattr(-,root,root,-)
%{_libdir}/libnl-cli*.so.*
%{_libdir}/libnl/
%{_sbindir}/*
%{_mandir}/man8/* 

%files doc
%defattr(-,root,root,-)
%doc libnl-doc-%{version}/*.html
%doc libnl-doc-%{version}/*.css
%doc libnl-doc-%{version}/stylesheets/*
%doc libnl-doc-%{version}/images/*
%doc libnl-doc-%{version}/images/icons/*
%doc libnl-doc-%{version}/images/icons/callouts/*
%doc libnl-doc-%{version}/api/*

%changelog
