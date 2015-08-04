Summary: Compat library to support binary need libpng12
Name: libpng12-compat
Epoch: 2
Version: 1.2.50
Release: 3 
License: zlib
Group: System Environment/Libraries
URL: http://www.libpng.org/pub/png/

Source: ftp://ftp.simplesystems.org/pub/png/src/libpng-%{version}.tar.xz
Patch1: libpng-pngconf.patch
Patch2: libpng-1.2.50-apng.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel

%description
Compat library to support binary need libpng12
%prep
%setup -q -n libpng-%{version}

%patch1 -p1
%patch2 -p1
%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la

rpmclean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libpng*.so.*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
