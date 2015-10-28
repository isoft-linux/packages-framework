Name:          libimobiledevice
Version:       1.2.0
Release:       2 
Summary:       Library for connecting to mobile devices

License:       LGPLv2+
URL:           http://www.libimobiledevice.org/
Source0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2

BuildRequires: glib2-devel
BuildRequires: gnutls-devel
BuildRequires: libgcrypt-devel
BuildRequires: libplist-devel
BuildRequires: libtasn1-devel
BuildRequires: libusbx-devel
BuildRequires: libxml2-devel
BuildRequires: readline-devel
BuildRequires: libusbmuxd-devel

%description
libimobiledevice is a library for connecting to mobile devices including phones 
and music players

%package devel
Summary: Development package for libimobiledevice
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with libimobiledevice.

%prep
%setup -q

# Fix dir permissions on html docs
chmod +x docs/html

%build
%configure --disable-static --enable-dev-tools
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING.LESSER README
%doc %{_datadir}/man/man1/idevice*
%{_bindir}/idevice*
%{_libdir}/libimobiledevice.so.*

%files devel
%doc docs/html/
%{_libdir}/pkgconfig/libimobiledevice-1.0.pc
%{_libdir}/libimobiledevice.so
%{_includedir}/libimobiledevice/

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.2.0-2
- Rebuild for new 4.0 release.

