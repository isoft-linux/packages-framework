%define upstream_version 20150421git

Summary: Mobile broadband provider database
Name: mobile-broadband-provider-info
Version: 1.%{upstream_version}
Release: 2%{?dist}
#
# Source from git://git.gnome.org/mobile-broadband-provider-info
# tarball built with:
#    ./autogen.sh --prefix=/usr
#    make distcheck
#
# Upstream release:
# http://ftp.gnome.org/pub/gnome/sources/mobile-broadband-provider-info/%{upstream_version}/mobile-broadband-provider-info-%{upstream_version}.tar.xz
Source: mobile-broadband-provider-info-%{upstream_version}.tar.bz2
License: Public Domain
Group: System Environment/Base

BuildArch: noarch
URL: http://live.gnome.org/NetworkManager/MobileBroadband/ServiceProviders
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: libxml2

%description
The mobile-broadband-provider-info package contains listings of mobile
broadband (3G) providers and associated network and plan information.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains files necessary for
developing developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{upstream_version}

%build
%configure
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, root, root, 0755)
%doc COPYING README
%dir %{_datadir}/%{name}
%attr(0644,root,root) %{_datadir}/%{name}/*
	
%files devel
%defattr(0644, root, root, 0755)
%{_datadir}/pkgconfig/%{name}.pc

%changelog
