Name:		ebook-tools
Version:	0.2.2
Release:	5
Summary:	Tools for accessing and converting various ebook file formats

Group:		Applications/Publishing
License:	MIT
URL:		http://sourceforge.net/projects/ebook-tools/

Source0:	http://downloads.sourceforge.net/ebook-tools/%{name}-%{version}.tar.gz

## upstreamable patches
# support libzip pkgconfig
Patch51:        ebook-tools-0.2.1-libzip_pkgconfig.patch

BuildRequires:	cmake
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libzip)

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description
Tools for accessing and converting various ebook file formats.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package libs
Summary:	Libraries for %{name}
Group:		System Environment/Libraries

%description libs
The %{name}-libs package contains libraries to be used by 
%{name} and others.

%prep
%setup -q
%patch51 -p1 -b .libzip_pkgconfig


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd
make %{_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform} 

#remove because it doesnt work without clit
rm -f %{buildroot}%{_bindir}/lit2epub

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/einfo

%files	devel
%defattr(-,root,root,-)
%{_libdir}/libepub.so
%{_includedir}/epub*.h

%files	libs
%defattr(-,root,root,-)
%doc README LICENSE
%{_libdir}/libepub.so.0*

%changelog
