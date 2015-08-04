Name:           xvidcore
Version:        1.3.3
Release:        2
Summary:        Free reimplementation of the OpenDivX video codec
Group:          System Environment/Libraries
License:        XVID (GPL with specific restrictions)
URL:            http://www.xvid.org/
Source0:        http://downloads.xvid.org/downloads/xvidcore-%{version}.tar.bz2

%description
Free reimplementation of the OpenDivX video codec. You can play OpenDivX
and DivX4 videos with it, as well as encode compatible files.

%package        devel
Summary:        Development files for the XviD video codec
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files, static library and API
documentation for the XviD video codec.


%prep
%setup -q -n xvidcore
%build
cd build/generic
%configure --disable-assembly
make %{?_smp_mflags} 
cd -


%install
rm -rf $RPM_BUILD_ROOT
make -C build/generic install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libxvidcore.a
chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so*
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libxvidcore.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/xvid.h
%{_libdir}/libxvidcore.so

