Name: libmfx
Version: 1.16	
Release: 2.git
Summary: Libmfx is part of Intel's Media SDK as a dispatch interface for video encode/decode 	
License: Redistributable	
URL: https://github.com/lu-zero/mfx_dispatch	
#git clone https://github.com/lu-zero/mfx_dispatch
Source0: mfx_dispatch.tar.gz

BuildRequires: libva-devel	
#Requires:	

%description
Libmfx is part of Intel's Media SDK as a dispatch interface for video encode/decode that's supported on both Windows and Linux. Under Linux, libmfx in turn interfaces with VA-API for doing the video encode/decode on the Intel HD Graphics hardware of recent generations. 

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n mfx_dispatch

%build
if [ ! -f "configure" ]; then autoreconf -ivf; fi
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%files
%{_libdir}/libmfx.so.*

%files devel
%{_includedir}/mfx
%{_libdir}/libmfx.so
%{_libdir}/libmfx.a
%{_libdir}/pkgconfig/libmfx.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.16-2.git
- Rebuild for new 4.0 release.


