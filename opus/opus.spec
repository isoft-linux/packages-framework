Name:          opus
Version:       1.1.1
Release:       3%{?dist}
Summary:       An audio codec for use in low-delay speech and audio communication

License:       BSD
URL:           http://www.opus-codec.org/
Source0:       http://downloads.xiph.org/releases/%{name}/%{name}-%{version}.tar.gz
BuildRequires: doxygen

%description
The Opus codec is designed for interactive speech and audio transmission over 
the Internet. It is designed by the IETF Codec Working Group and incorporates 
technology from Skype's SILK codec and Xiph.Org's CELT codec.

%package devel
Summary: Development package for opus
Requires: libogg-devel
Requires: opus = %{version}-%{release}

%description devel
Files for development with opus.

%prep
%setup -q -n %{name}-%{version}

%build
%configure --enable-custom-modes --disable-static

make %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete
rm -rf %{buildroot}%{_datadir}/doc/opus/html

%check
make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/libopus.so.*

%files devel
%defattr(-,root,root,-)
%doc README doc/html
%{_includedir}/opus
%{_libdir}/libopus.so
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4
%{_datadir}/man/man3/opus_*.3.gz

%changelog
* Sat Dec 05 2015 Cjacker <cjacker@foxmail.com> - 1.1.1-3
- Update to 1.1.1 official release

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.1.1-0.4.beta
- Rebuild for new 4.0 release.

