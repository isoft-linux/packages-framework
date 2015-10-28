Summary: Library of Optimized Inner Loops, CPU optimized functions
Name: liboil
Version: 0.3.16
Release: 13%{?dist}
# See COPYING which details everything, various BSD licenses apply
License: BSD
URL: http://liboil.freedesktop.org/
Source: http://liboil.freedesktop.org/download/%{name}-%{version}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=435771
Patch4: liboil-0.3.13-disable-ppc64-opts.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: glib2-devel, pkgconfig

%description
Liboil is a library of simple functions that are optimized for various CPUs.
These functions are generally loops implementing simple algorithms, such as
converting an array of N integers to floating-poing numbers or multiplying
and summing an array of N numbers. Clearly such functions are candidates for
significant optimization using various techniques, especially by using
extended instructions provided by modern CPUs (Altivec, MMX, SSE, etc.).


%package devel
Summary: Development files and static library for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig, gtk-doc

%description devel
Liboil is a library of simple functions that are optimized for various CPUs.
These functions are generally loops implementing simple algorithms, such as
converting an array of N integers to floating-poing numbers or multiplying
and summing an array of N numbers. Clearly such functions are candidates for
significant optimization using various techniques, especially by using
extended instructions provided by modern CPUs (Altivec, MMX, SSE, etc.).

%prep
%setup -q
%patch4 -p0 -b .disable-ppc64-opts

%build
%configure
# Remove standard rpath from oil-bugreport
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING BUG-REPORTING NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_bindir}/oil-bugreport
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%doc %{_datadir}/gtk-doc/html/%{name}/


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.3.16-13
- Rebuild for new 4.0 release.

