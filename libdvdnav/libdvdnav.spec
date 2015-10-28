Name:           libdvdnav
Version:        5.0.3
Release:        2 
Summary:        A library for reading DVD video discs based on Ogle code

License:        GPLv2+
Source0:        http://download.videolan.org/videolan/libdvdnav/5.0.3/libdvdnav-%{version}.tar.bz2

BuildRequires:  libdvdread-devel >= 4.1.3-0.3

%description
libdvdnav provides a simple library for reading DVD video discs.
The code is based on Ogle and used in, among others, the Xine dvdnav plug-in.

%package        devel
Summary:        Development files for libdvdnav
Requires:       %{name} = %{version}-%{release}
Requires:       libdvdread-devel >= 4.1.3-0.3
Requires:       pkgconfig

%description    devel
libdvdnav-devel contains the files necessary to build packages that use the
libdvdnav library.

%prep
%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libdvdnav.so.*

%files devel
%defattr(-,root,root,-)
%doc TODO
%{_libdir}/libdvdnav.so
%{_includedir}/dvdnav
%{_libdir}/pkgconfig/dvdnav.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 5.0.3-2
- Rebuild for new 4.0 release.

