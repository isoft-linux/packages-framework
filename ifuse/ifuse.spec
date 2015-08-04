Name:          ifuse
Version:       1.1.3
Release:       7
Summary:       Mount Apple iPhone and iPod touch devices

Group:         System Environment/Libraries
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
