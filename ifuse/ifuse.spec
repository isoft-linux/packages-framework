Name:          ifuse
Version:       1.1.3
Release:       8
Summary:       Mount Apple iPhone and iPod touch devices

License:       GPLv2+
URL:           http://www.libimobiledevice.org/
Source0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2

BuildRequires: fuse-devel
BuildRequires: libimobiledevice-devel
BuildRequires: libplist-devel
Requires: fuse

%description
A fuse filesystem for mounting iPhone and iPod touch devices

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS README
%{_bindir}/ifuse
%{_mandir}/man1/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.1.3-8
- Rebuild for new 4.0 release.

