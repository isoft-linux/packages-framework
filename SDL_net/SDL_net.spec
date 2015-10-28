Name:		SDL_net
Version:	1.2.8
Release: 	4
Summary:	Simple DirectMedia Layer - Network Library

License:	LGPLv2
URL:		http://www.libsdl.org/projects/SDL_net/
Source0:	http://www.libsdl.org/projects/SDL_net/release/SDL_net-%{version}.tar.gz

BuildRequires:	SDL-devel >= 1.2.10 

%description
This is an example portable network library for use with SDL.
It is available under the zlib license, found in the file COPYING.
The API can be found in the file SDL_net.h
This library supports UNIX, Windows, MacOS Classic, MacOS X,
BeOS and QNX.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel >= 1.2.10
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure \
    --disable-dependency-tracking	\
    --disable-static 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README CHANGES COPYING
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/SDL

%changelog
* Sun Oct 25 2015 Cjacker <cjacker@foxmail.com> - 1.2.8-4
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

