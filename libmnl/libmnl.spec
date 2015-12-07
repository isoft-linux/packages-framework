Name:           libmnl
Version:        1.0.3
Release:        2%{?dist}
Summary:        A minimalistic Netlink library

License:        LGPLv2+
URL:            http://netfilter.org/projects/libmnl
Source0:        http://netfilter.org/projects/libmnl/files/%{name}-%{version}.tar.bz2

%description
libmnl is a minimalistic user-space library oriented to Netlink developers.
There are a lot of common tasks in parsing, validating, constructing of both
the Netlink header and TLVs that are repetitive and easy to get wrong.
This library aims to provide simple helpers that allows you to re-use code and
to avoid re-inventing the wheel.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}

%package 	static
Summary: 	Static development files for %{name}
Requires: %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description 	static
The %{name}-static package contains static libraries for devleoping applications that use %{name}.


%prep
%setup -q


%build
%configure --enable-static
make CFLAGS="%{optflags}" %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find examples '(' -name 'Makefile.am' -o -name 'Makefile.in' ')' -exec rm -f {} ';'
find examples -type d -name '.deps' -prune -exec rm -rf {} ';'
mv examples examples-%{_arch}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{_libdir}/*.so.*

%files devel
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc examples-%{_arch}
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files static
%{_libdir}/*.a

%changelog
* Mon Dec 07 2015 Cjacker <cjacker@foxmail.com> - 1.0.3-2
- Initial build

