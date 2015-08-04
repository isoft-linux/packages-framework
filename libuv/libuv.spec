Name:		libuv
Version:    1.6.1	
Release:	1
Summary:    Abstract IOCP Layer from NodeJS

Group:		Extra/Runtime/Library
License:	MIT and BSD and ISC
URL:		http://www.libuv.org
Source0:    http://libuv.org/dist/v0.10.29/%{name}-v%{version}.tar.gz	

%description
libuv is a new platform layer for Node. Its purpose is to abstract IOCP on
Windows and epoll/kqueue/event ports/etc. on Unix systems. We intend to
eventually contain all platform differences in this library.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n libuv-v%{version}

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#we do not ship static library
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.a
rpmclean

%check
make check

%files
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%changelog
* Mon Jul 13 2015 Cjacker <cjacker@foxmail.com>
- first build.
