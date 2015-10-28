Name:           faac
Version:        1.28
Release:        3
Summary:        Encoder and encoding library for MPEG2/4 AAC

License:        LGPL
URL:            http://www.audiocoding.com/
Source0:        http://download.sourceforge.net/sourceforge/faac/faac-%{version}.tar.bz2

Patch0: mp4v2-1.9.patch
Patch1: mp4v2-2.0.0.patch
Patch2: altivec.patch

BuildRequires:  mp4v2-devel
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  automake


%description
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

%package devel
Summary:        Development libraries of the FAAC AAC encoder
Requires:       %{name} = %{version}-%{release}

%description devel
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

This package contains development files and documentation for libfaac.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0

%build
autoreconf -ivf
LIBS="-lmp4v2" %configure
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
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.28-3
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

