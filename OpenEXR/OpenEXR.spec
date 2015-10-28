Name:	 OpenEXR
Version: 1.7.1
Release: 2 
Summary: A high dynamic-range (HDR) image file format

License: BSD
URL:	 http://www.openexr.com/
Source0: https://github.com/downloads/openexr/openexr/openexr-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global soname 7

Obsoletes: openexr < %{version}-%{release}
Provides:  openexr = %{version}-%{release}

BuildRequires:  ilmbase-devel 
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial
Light & Magic for use in computer imaging applications. This package contains
libraries and sample applications for handling the format.

%package devel
Summary: Headers and libraries for building apps that use %{name} 
Obsoletes: openexr-devel < %{version}-%{release}
Provides:  openexr-devel = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: ilmbase-devel
Requires: pkgconfig
%description devel
%{summary}.

%package libs
Summary: %{name} runtime libraries
%description libs
%{summary}.


%prep
%setup -q -n openexr-%{version}

%build
%configure --disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

#unpackaged files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion OpenEXR)" = "%{version}"
make check


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*

%post libs -p /sbin/ldconfig
%postun libs  -p /sbin/ldconfig

%files libs
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE NEWS README
%{_libdir}/libIlmImf.so.%{soname}*

%files devel
%defattr(-,root,root,-)
#omit for now, they're mostly useless, and include multilib conflicts (#342781)
#doc rpmdocs/examples 
%{_datadir}/aclocal/openexr.m4
%{_includedir}/OpenEXR/*
%{_libdir}/libIlmImf.so
%{_libdir}/pkgconfig/OpenEXR.pc


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.7.1-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

