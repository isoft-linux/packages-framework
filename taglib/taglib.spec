Summary: TagLib Audio Meta-Data Library 
Name: taglib
Version: 1.9.1
Release: 2
License: GPL
URL: http://developer.kde.org/~wheeler/taglib.html
Source: http://developer.kde.org/~wheeler/files/src/%{name}-%{version}.tar.gz
BuildRequires:cmake

%description
TagLib is a library for reading and editing the meta-data of several 
popular audio formats. Currently it supports both ID3v1 and ID3v2 for 
MP3 files, Ogg Vorbis comments and ID3 tags and Vorbis comments in 
FLAC files.

%package devel
Summary: Development tools for taglib 
Requires: %{name} = %{version}-%{release}
%description devel
Development tools for taglib


%prep
%setup -q
%build
FLAGS="-fPIC $RPM_OPT_FLAGS"
export CXXFLAGS="$FLAGS"
export CFLAGS="$FLAGS"

mkdir build
cd build
%cmake .. -DCMAKE_RELEASE_TYPE=Release

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
cd build
make install  DESTDIR=$RPM_BUILD_ROOT


%clean 
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*-config
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/taglib.pc
%{_libdir}/pkgconfig/taglib_c.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.9.1-2
- Rebuild for new 4.0 release.


