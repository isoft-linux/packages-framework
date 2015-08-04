Summary:	Sample rate conversion library for audio data
Name:		libsamplerate
Version:	0.1.8
Release:	4
License:	GPL
Group:		System Environment/Libraries
URL:		http://www.mega-nerd.com/SRC/
Source0:	http://www.mega-nerd.com/SRC/%{name}-%{version}.tar.gz
BuildRequires:	libsndfile-devel >= 1.0.6 pkgconfig

%package devel
Summary:	Development related files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release} pkgconfig


%description
Secret Rabbit Code is a sample rate converter for audio. It is capable
of arbitrary and time varying conversions. It can downsample by a
factor of 12 and upsample by the same factor. The ratio of input and
output sample rates can be a real number. The conversion ratio can
also vary with time for speeding up and slowing down effects.

%description devel
Secret Rabbit Code is a sample rate converter for audio. It is capable
of arbitrary and time varying conversions. It can downsample by a
factor of 12 and upsample by the same factor. The ratio of input and
output sample rates can be a real number. The conversion ratio can
also vary with time for speeding up and slowing down effects.
This package contains development files for %{name}


%prep
%setup -q

%build
%configure --disable-dependency-tracking --disable-fftw
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT _doc
make install DESTDIR=$RPM_BUILD_ROOT
cp -a doc _doc
rm _doc/Makefile* _doc/NEWS _doc/ChangeLog

rpmclean
%check || :
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/sndfile-resample
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/samplerate.h
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/samplerate.pc
%{_docdir}/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

