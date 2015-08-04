Summary:    SpeexDSP is a patent-free, Open Source/Free Software DSP library	
Name:		libspeexdsp
Version: 	1.2	
%define rc_ver	rc3
Release:	1.12.%{rc_ver}
License:	BSD
Group:		System Environment/Libraries
URL:		http://www.speex.org/
Source0:	http://downloads.xiph.org/releases/speex/speexdsp-%{version}%{rc_ver}.tar.gz

#fix stdint include.
Patch0:     speexdsp-fixbuilds-774c87d.patch

BuildRequires:	libogg-devel
Provides: speexdsp=%{version}-%{release}

%description
Speex is a patent-free compression format designed especially for
speech. It is specialized for voice communications at low bit-rates in
the 2-45 kbps range. Possible applications include Voice over IP
(VoIP), Internet audio streaming, audio books, and archiving of speech
data (e.g. voice mail).

%package devel
Summary: 	Development package for %{name}
Group: 		Development/Libraries
Requires: 	%{name} = %{version}-%{release}
Requires: 	pkgconfig
Provides: speexdsp-devel=%{version}-%{release}

%description devel
Speex is a patent-free compression format designed especially for
speech. This package contains development files for %{name}

%prep
%setup -q -n speexdsp-%{version}%{rc_ver}
%patch0 -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libspeexdsp.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/manual.pdf
%dir %{_includedir}
%{_includedir}/speex/*.h
%{_libdir}/pkgconfig/speexdsp.pc
%{_libdir}/libspeexdsp.so

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

