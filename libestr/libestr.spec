Name:           libestr
Version:        0.1.9
Release:        5%{?dist}
Summary:        String handling essentials library

License:        LGPLv2+
URL:            http://libestr.adiscon.com/
Source0:        http://libestr.adiscon.com/files/download/libestr-%{version}.tar.gz

%description
This package compiles the string handling essentials library
used by the Rsyslog daemon.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The package contains libraries and header files for
developing applications that use libestr.

%prep
%setup -q

%build
%configure --disable-static --with-pic
V=1 make %{?_smp_mflags}

%install
make install INSTALL="install -p" DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.{a,la}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README AUTHORS ChangeLog
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/libestr.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libestr.pc

%changelog
