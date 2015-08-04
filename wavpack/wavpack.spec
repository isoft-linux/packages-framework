Name:		wavpack
Summary:	A completely open audiocodec
Version:	4.70.0
Release:    1	
License:	BSD
Group:		Applications/Multimedia
Url:		http://www.wavpack.com/
Source:		http://www.wavpack.com/%{name}-%{version}.tar.bz2

%description
WavPack is a completely open audio compression format providing lossless,
high-quality lossy, and a unique hybrid compression mode. Although the
technology is loosely based on previous versions of WavPack, the new
version 4 format has been designed from the ground up to offer unparalleled
performance and functionality.

%package devel
Summary:	WavPack - development files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
Files needed for developing apps using wavpack

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/%{_libdir}/*.la

rpmclean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/*
%{_libdir}/libwavpack.so.*
%{_mandir}/man1/wavpack.1*
%{_mandir}/man1/wvgain.1*
%{_mandir}/man1/wvunpack.1*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libwavpack.so

%changelog
