Name:		libcue
Version:	1.4.0
Release:	6%{?dist}
Summary:	Cue sheet parser library

Group:		System Environment/Libraries
# Files libcue/rem.{c,h} contains a BSD header
License:	GPLv2 and BSD
URL:		https://libcue.sourceforge.net/
Patch1:		libcue-0001-Rename-buffer-to-yy_buffer.patch
Patch2:		libcue-0002-Hide-flex-related-symbols.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	flex
Source0:	https://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.bz2


%description
Libcue is intended for parsing a so-called cue sheet from a char string or
a file pointer. For handling of the parsed data a convenient API is available.


%package devel
Summary:	Development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig


%description	devel
Development files for %{name}.


%prep
%setup -q
%patch1 -p1 -b .rename_buffer
%patch2 -p1 -b .hide_flex
autoreconf -ivf


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/libcue.la


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%{_libdir}/%{name}.so.*
%doc AUTHORS COPYING NEWS


%files devel
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
