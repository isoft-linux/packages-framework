Summary: 	Advanced Audio Decoder
Name: 		faad2
Version: 	2.7
Release: 	1
License: 	GPL
Group: 		System Environment/Libraries
URL: 		http://faac.sourceforge.net/
Source0:        http://resare.com/noa/livna/faad2-%{version}.tar.gz
#BuildRequires:	id3lib-devel
BuildRequires:	autoconf automake libtool

%package devel
Summary:	Development files for the faad library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

# --------------------------------------------------------------------

%description
FAAD is an Advanced Audio Decoder (MPEG2-AAC, MPEG4-AAC). 

%description devel
FAAD is an Advanced Audio Decoder (MPEG2-AAC, MPEG4-AAC). 
This package contains development files for the FAAD.


# --------------------------------------------------------------------

%prep
%setup -q 

%build
%configure --without-xmms --disable-static --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/faad
%{_libdir}/libfaad.so.*
%{_mandir}

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a

# --------------------------------------------------------------------

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

