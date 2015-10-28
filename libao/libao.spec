Name:           libao
Version:        1.2.0
Release:        6%{?dist}
Summary:        Cross Platform Audio Output Library
License:        GPLv2+
URL:            http://xiph.org/ao/
Source0:        http://downloads.xiph.org/releases/ao/%{name}-%{version}.tar.gz
Patch1:         0001-ao_pulse.c-fix-latency-calculation.patch
BuildRequires:  alsa-lib-devel
BuildRequires:  pkgconfig(libpulse)

%description
Libao is a cross platform audio output library. It currently supports
ESD, OSS, Solaris, and IRIX.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch1 -p1
sed -i "s/-O20 -ffast-math//" configure


%build
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
%make_install INSTALL="install -p"
# remove unpackaged files from the buildroot
find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}*


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS CHANGES COPYING README
%{_libdir}/libao.so.*
%{_libdir}/ao
%{_mandir}/man5/*

%files devel
%doc doc/*.html doc/*.c doc/*.css
%{_includedir}/ao
%{_libdir}/ckport
%{_libdir}/libao.so
%{_libdir}/pkgconfig/ao.pc
%{_datadir}/aclocal/ao.m4


%changelog
* Sat Oct 24 2015 builder - 1.2.0-6
- Rebuild for new 4.0 release.

