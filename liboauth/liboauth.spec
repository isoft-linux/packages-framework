Name:           liboauth
Version:        1.0.3
Release:        5
Summary:        OAuth library functions

License:        MIT
URL:            http://liboauth.sourceforge.net/
Source0:        http://liboauth.sourceforge.net/pool/liboauth-%{version}.tar.gz

BuildRequires:  libcurl-devel nss-devel
#Requires:       

%description
liboauth is a collection of POSIX-c functions implementing the OAuth
Core RFC 5849 standard. liboauth provides functions to escape and
encode parameters according to OAuth specification and offers
high-level functionality to sign requests or verify OAuth signatures
as well as perform HTTP requests.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
%if 0%{?el5}
Requires:       pkgconfig libcurl-devel nss-devel
%endif

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static --enable-nss
make %{?_smp_mflags}


%install
%if 0%{?el5}
rm -rf $RPM_BUILD_ROOT
%endif
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/oauth.pc
%{_mandir}/man3/oauth.*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.3-5
- Rebuild for new 4.0 release.

