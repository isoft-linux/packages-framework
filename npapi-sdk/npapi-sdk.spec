%define debug_package %{nil}
Name:		npapi-sdk
Version:	0.27.2
Release:	2
Summary:	NPAPI-SDK is a bundle of Netscape Plugin Application Programming Interface headers by Mozilla

License:	Mozilla
Source0:	    https://bitbucket.org/mgorny/npapi-sdk/downloads/npapi-sdk-%{version}.tar.bz2	

%description
NPAPI-SDK is a bundle of Netscape Plugin Application Programming Interface headers by Mozilla. This package provides a clear way to install those headers and depend on them. 

%prep
%setup -q

%build
%configure

%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%doc samples/unix-basic
%dir %{_includedir}/npapi-sdk
%{_includedir}/npapi-sdk/*
%{_libdir}/pkgconfig/npapi-sdk.pc


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.27.2-2
- Rebuild for new 4.0 release.


