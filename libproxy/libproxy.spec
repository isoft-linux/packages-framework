Name:		libproxy
Version:	0.4.11
Release:	1
Summary:	A library that provides automatic proxy configuration management.

Group:		Framework/Runtime/Library
License:	LGPLv2+
URL:		https://code.google.com/p/libproxy/
Source0:	https://code.google.com/p/libproxy/downloads/detail?name=libproxy-0.4.11.tar.gz
Patch0:     libproxy-fix-musl-missing-headers.patch
Patch1:     libproxy-fix-perl-off64_t.patch

BuildRequires:	cmake
BuildRequires:  NetworkManager-devel
%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Framework/Development/Library
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package    -n  python-libproxy 
Summary:        Python module of libproxy
Group:          Framework/Runtime/Library/Python
Requires:       %{name} = %{version}-%{release}

%description  -n python-libproxy 
This package contains python module of libproxy.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
mkdir build
pushd build
%cmake -DWITH_PERL=OFF ..
make %{?_smp_mflags}
popd

%install
pushd build
make install DESTDIR=%{buildroot}
popd


%files
%{_bindir}/proxy
%{_libdir}/libproxy.so.*
%{_libdir}/libproxy/*/modules/config_gnome3.so
%{_libdir}/libproxy/*/modules/network_networkmanager.so
%{_libexecdir}/pxgsettings

%files devel
%{_includedir}/proxy.h
%{_libdir}/libproxy.so
%{_libdir}/pkgconfig/libproxy-1.0.pc
%{_datadir}/cmake/Modules/Findlibproxy.cmake

%files -n python-libproxy
%{_libdir}/python?.?/site-packages/libproxy.py

%changelog
