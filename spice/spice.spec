Summary:SPICE: Simple Protocol for Independent Computing Environments
Name: spice
Version: 0.12.5
Release: 2
License: LGPLv2+
Source: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: spice-protocol, celt051-devel, libcacard-devel, pyparsing
BuildRequires: cyrus-sasl-devel

%description
SPICE is a remote display system built for virtual environments which
allows you to view a computing 'desktop' environment not only on the
machine where it is running, but from anywhere on the Internet and
from a wide variety of machine architectures.

%package -n libspice
Summary:        Runtime libraries for %{name}

%description -n libspice
This package contains runtime library of %{name}

%package -n libspice-devel
Summary:        Development libraries and header files for %{name}
Requires:       libspice = %{version}-%{release}

%description -n libspice-devel
This package contains Development libraries and header files of %{name}

%prep
%setup -q

%build
%configure --enable-client --with-sasl --enable-smartcard
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%{_bindir}/spicec

%files -n libspice
%{_libdir}/*.so.*

%files -n libspice-devel
%defattr(-, root, root, -)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/spice-server
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.12.5-2
- Rebuild for new 4.0 release.

