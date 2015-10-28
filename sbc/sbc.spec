Name:          sbc
Version:       1.3
Release:       2
Summary:       Sub Band Codec used by bluetooth A2DP

License:       GPLv2 and LGPLv2+
URL:           http://www.bluez.org
Source0:       http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.xz
Patch0:         sbc-clang.patch
BuildRequires:  libsndfile-devel

%description
SBC (Sub Band Codec) is a low-complexity audio codec used in the Advanced Audio 
Distribution Profile (A2DP) bluetooth standard but can be used standalone. It 
uses 4 or 8 subbands, an adaptive bit allocation algorithm in combination with 
an adaptive block PCM quantizers.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%prep
%setup -q 

%build
autoreconf -ivf
%configure --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/sbc*
%{_libdir}/libsbc.so.1*

%files devel
%{_includedir}/sbc/
%{_libdir}/pkgconfig/sbc.pc
%{_libdir}/libsbc.so

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.3-2
- Rebuild for new 4.0 release.

