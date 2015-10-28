Summary:     	libspectre is a small library for rendering Postscript documents	
Name:           libspectre
Version:       	0.2.7
Release:       	2
License:        GPLv2+
URL:            http://www.freedesktop.org/wiki/Software/libspectre/
Source0:       	http://libspectre.freedesktop.org/releases/%{name}-%{version}.tar.gz 
BuildRequires:  libtool automake autoconf 
BuildRequires:  pkgconfig
BuildRequires:	ghostscript-devel
Requires:	    ghostscript

%description
libspectre is a small library for rendering Postscript documents.
%package devel
Summary: Files needed for development using %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}
%{_libdir}/pkgconfig/*
%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.2.7-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

