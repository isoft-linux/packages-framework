Name:           libass
Version:        0.12.3
Release:        2 
Summary:        Portable library for SSA/ASS subtitles rendering

License:        ISC
URL:            http://code.google.com/p/libass/
Source0:        https://github.com/libass/libass/releases/download/%{version}/libass-%{version}.tar.xz

BuildRequires:  libpng-devel
BuildRequires:  enca-devel
BuildRequires:  fontconfig-devel
BuildRequires:  fribidi-devel


%description
Libass is a portable library for SSA/ASS subtitles rendering.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libass.pc

%changelog
* Sat Oct 24 2015 builder - 0.12.3-2
- Rebuild for new 4.0 release.

* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- update to 0.12.3
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

