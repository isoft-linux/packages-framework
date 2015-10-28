Summary: 	LZMA utils
Name: 		lzma
Version: 	4.32.7
Release: 	15
License: 	GPLv2+
Source0:	http://tukaani.org/%{name}/%{name}-%{version}.tar.lzma
URL:		http://tukaani.org/%{name}/

%description
LZMA provides very high compression ratio and fast decompression. The
core of the LZMA utils is Igor Pavlov's LZMA SDK containing the actual
LZMA encoder/decoder. LZMA utils add a few scripts which provide
gzip-like command line interface and a couple of other LZMA related
tools. 

%package 	libs
Summary:	Libraries for decoding LZMA compression
License:	LGPLv2+

%description 	libs
Libraries for decoding LZMA compression.

%package 	devel
Summary:	Devel libraries & headers for liblzmadec
License:	LGPLv2+
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description  devel
Devel libraries & headers for liblzmadec.

%prep
%setup -q  -n %{name}-%{version}

%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
%configure --disable-static

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
rm -f %{buildroot}/%{_libdir}/*.a
rm -f %{buildroot}/%{_libdir}/*.la
# base package tools/manuals obsoleted by xz-lzma-compat (rhbz #999937)
rm -f %{buildroot}%{_bindir}/*
rm -f %{buildroot}%{_mandir}/man1/*

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%defattr(-,root,root,-)
%doc COPYING.*
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.32.7-15
- Rebuild for new 4.0 release.

