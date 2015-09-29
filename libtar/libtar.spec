Summary:        Tar file manipulation API
Name:           libtar
Version:        1.2.20
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Libraries
URL:            http://www.feep.net/libtar/
Source0:        ftp://ftp.feep.net/pub/software/libtar/libtar-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  zlib-devel libtool

%description
libtar is a C library for manipulating tar archives. It supports both
the strict POSIX tar format and many of the commonly-used GNU
extensions.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%{expand: %%define optflags %{optflags} -fPIC}
autoreconf -fi
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
chmod +x $RPM_BUILD_ROOT%{_libdir}/libtar.so.*
rm $RPM_BUILD_ROOT%{_libdir}/*.la


%files
%doc COPYRIGHT TODO README ChangeLog*
%{_bindir}/%{name}
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/libtar.h
%{_includedir}/libtar_listhash.h
%{_libdir}/lib*.so
%{_mandir}/man3/*.3*


%changelog

