Summary: 	Library for reading and writing sound files
Name: 		libsndfile
Version: 	1.0.25
Release: 	1
License: 	LGPL
Group: 		System Environment/Libraries
URL: 		http://www.mega-nerd.com/libsndfile/
Source0: 	http://www.mega-nerd.com/libsndfile/libsndfile-%{version}.tar.gz
Patch0:		libsndfile-1.0.11-svx-channels.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

BuildRequires:  alsa-lib-devel, libogg-devel, libvorbis-devel
BuildRequires:  libflac-devel

%package devel
Summary:	Development files for libsndfile
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release} pkgconfig

%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface. It can
currently read/write 8, 16, 24 and 32-bit PCM files as well as 32 and
64-bit floating point WAV files and a number of compressed formats. It
compiles and runs on *nix, MacOS, and Win32.

%description devel
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface. 
This package contains files needed to develop with libsndfile.


%prep
%setup -q


%build
CFLAGS="-fPIC $RPM_OPT_FLAGS" %configure --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __docs
make install DESTDIR=$RPM_BUILD_ROOT
cp -pR $RPM_BUILD_ROOT%{_docdir}/libsndfile1-dev/html __docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/libsndfile1-dev


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README NEWS ChangeLog
%{_bindir}/*
%{_libdir}/%{name}.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc __docs/*
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_libdir}/pkgconfig/sndfile.pc


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

