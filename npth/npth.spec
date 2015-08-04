Name:           npth
Version:        1.2
Release:        2
Summary:        The New GNU Portable Threads library
License:        LGPLv3+ or GPLv2+ or (LGPLv3+ and GPLv2+)
URL:            http://git.gnupg.org/cgi-bin/gitweb.cgi?p=npth.git
Source:         ftp://ftp.gnupg.org/gcrypt/npth/npth-%{version}.tar.bz2
Source2:        npth-config.1

%description
nPth is a non-preemptive threads implementation using an API very similar
to the one known from GNU Pth. It has been designed as a replacement of
GNU Pth for non-ancient operating systems. In contrast to GNU Pth is is
based on the system's standard threads implementation. Thus nPth allows
the use of libraries which are not compatible to GNU Pth.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

mkdir -p %{buildroot}%{_mandir}/man1/
install -pm0644 %{S:2} %{buildroot}%{_mandir}/man1/

find %{buildroot} -name '*.la' -delete -print

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so.*

%files devel
%{_bindir}/*
%{_libdir}/*.so
%{_includedir}/*.h
%{_mandir}/*/*
%{_datadir}/aclocal/*

%changelog
