%define	name		libIDL
%define	version		0.8.14
%define	release		3
%define epoch		1

Summary: Library for parsing IDL (Interface Definition Language)
Name: libIDL		
Version: 0.8.14
Release: 2
Epoch: 2
License: LGPLv2+
URL: http://www.gnome.org
Source: http://ftp.gnome.org/pub/gnome/sources/libIDL/0.8/libIDL-%{version}.tar.bz2
BuildRequires: pkgconfig >= 0.8
BuildRequires: glib2-devel >= 2.0
BuildRequires: flex bison

%description
libIDL is a library for parsing IDL (Interface Definition Language).
It can be used for both COM-style and CORBA-style IDL.

%package devel
Summary: Libraries and include files for %{name}.
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Development files for %{name}.

%prep
%setup -q

%build
export CFLAGS="-fPIC $RPM_OPT_FLAGS" 
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_infodir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/libIDL-config-2
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/libIDL-2.0.pc
%dir %{_includedir}/libIDL-2.0
%{_includedir}/libIDL-2.0/libIDL/*.h
%{_libdir}/*.a

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2:0.8.14-2
- Rebuild for new 4.0 release.

* Fri Oct 23 2015 Cjacker <cjacker@foxmail.com> - 2:0.8.14-2
- rebuild, improve SPEC file.

* Sun Aug 02 2015 Cjacker <cjacker@foxmail.com>
- build for new release.
