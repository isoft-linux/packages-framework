Name:           libdvdread
Version:        5.0.3 
Release:        1 
Summary:        A library for reading DVD video discs based on Ogle code

Group:          System Environment/Libraries
License:        GPLv2+
Source0:        http://download.videolan.org/videolan/libdvdread/5.0.3/libdvdread-%{version}.tar.bz2

%description
libdvdread provides a simple foundation for reading DVD video disks.
It provides the functionality that is required to access many DVDs.

%package        devel
Summary:        Development files for libdvdread
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
libdvdread provides a simple foundation for reading DVD video disks.
It provides the functionality that is required to access many DVDs.

This package contains development files for libdvdread.

%prep
%setup -q

%build
%configure --disable-static

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/libdvdread.so.*

%files devel
%defattr(-,root,root,-)
%doc DEVELOPMENT-POLICY.txt TODO
%{_includedir}/dvdread
%{_libdir}/libdvdread.so
%{_libdir}/pkgconfig/dvdread.pc

%changelog
