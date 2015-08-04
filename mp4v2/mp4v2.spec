Summary: Library for working with files using the mp4 container format
Name:    mp4v2
Version: 2.0.0 
Release: 1 
License: MPL
Group: System Environment/Libraries
URL: http://resare.com/libmp4v2/
Source0: http://resare.com/libmp4v2/dist/mp4v2-%{version}.tar.bz2

%description
The libmp4v2 library provides an abstraction layer for working with files
using the mp4 container format. This library is developed by mpeg4ip project
and is an exact copy of the library distributed in the mpeg4ip package.


%package devel
Summary: Development files for the mp4v2 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files and documentation needed to develop and compile programs
using the libmp4v2 library.


%prep
%setup -q

%build
%configure \
    --disable-static
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%{__rm} -rf %{buildroot}%{_mandir}/manm/

rpmclean
%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,0755)
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,0755)
%{_includedir}/mp4v2/*.h
%{_libdir}/*.so
%{_mandir}/man?/*


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

