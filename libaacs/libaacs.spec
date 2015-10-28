Name:           libaacs
Version:        0.8.1
Release:        2.1
License:        LGPL-2.1+
Summary:        Open implentation of AACS specification
Url:            http://www.videolan.org/developers/libaacs.html
Source:         ftp://ftp.videolan.org/pub/videolan/libaacs/%{version}/libaacs-%{version}.tar.bz2
Patch1:         libaacs-pthread.patch
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  libgcrypt-devel
BuildRequires:  autoconf automake libtool
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
libaacs is a research project to implement the Advanced Access Content System specification.
This research project provides, through an open-source library, a way to understand how the AACS works.

%package devel
Summary:        Open implentation of AACS specification - Development files
Requires:       %{name} = %{version}

%description devel
libaacs is a research project to implement the Advanced Access Content System specification.
This research project provides, through an open-source library, a way to understand how the AACS works.

%prep
%setup -q
%patch1 -p0

%build
./bootstrap
%configure --disable-static
make %{?_smp_mflags}

%install
%makeinstall
find %{buildroot} -type f -name "*.la" -delete -print

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc COPYING
%{_bindir}/aacs_info
%{_libdir}/libaacs.so.0
%{_libdir}/libaacs.so.0.*

%files devel
%defattr(-, root, root)
%{_libdir}/libaacs.so
%{_libdir}/pkgconfig/libaacs.pc
%{_includedir}/%{name}/

%changelog
* Sat Oct 24 2015 builder - 0.8.1-2.1
- Rebuild for new 4.0 release.

