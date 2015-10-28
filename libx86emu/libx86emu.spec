ExclusiveArch:  %ix86 x86_64

Name:           libx86emu
BuildRequires:  xz
Summary:        A small x86 emulation library.
License:        BSD-3-Clause
Version:        1.5
Release:        2.2
PreReq:         /sbin/ldconfig
Source:         %{name}-%{version}.tar.xz
Url:            https://github.com/wfeldt/libx86emu

%description
Small x86 emulation library with focus of easy usage and extended
execution logging functions.


%package -n     libx86emu-devel
Summary:        A small x86 emulation library.
Requires:       %{name} = %version

%description -n libx86emu-devel
Small x86 emulation library with focus of easy usage and extended
execution logging functions.

%prep
%setup -n libx86emu-%{version}

%build
make LIBDIR=%{_libdir}

%install
install -d -m 755 %{buildroot}%{_libdir}
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%doc README LICENSE

%files -n libx86emu-devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/x86emu.h

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.5-2.2
- Rebuild for new 4.0 release.

