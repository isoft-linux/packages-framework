%global source_dir  %{_datadir}/%{name}-source
%global inst_srcdir %{buildroot}/%{source_dir}

Name:             libev
Summary:          High-performance event loop/event model with lots of features
Version:          4.19
Release:          3%{?dist}
License:          BSD or GPLv2+
URL:              http://software.schmorp.de/pkg/libev.html
Source0:          http://dist.schmorp.de/libev/Attic/%{name}-%{version}.tar.gz

BuildRequires:    autoconf automake libtool

Patch0:           libev-4.19-Modernize-the-configure.ac.patch
Patch1:           libev-4.19-Respect-the-CFLAGS-if-defined.patch

%description
Libev is modeled (very loosely) after libevent and the Event Perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller.


%package devel
Summary:          Development headers for libev
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers and libraries for libev.


#%package libevent-devel
#Summary:          Compatibility development header with libevent for %{name}.
#Requires:         %{name}-devel%{?_isa} = %{version}-%{release}
#
## The event.h file actually conflicts with the one from libevent-devel
#Conflicts:        libevent-devel
#
#%description libevent-devel
#This package contains a development header to make libev compatible with
#libevent.


%package source
Summary:          High-performance event loop/event model with lots of features
BuildArch:        noarch

%description source
This package contains the source code for libev.


%prep
%setup -q

%patch0 -p1
%patch1 -p1

autoreconf -i


%build
%configure --disable-static --with-pic
make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

rm -rf %{buildroot}%{_libdir}/%{name}.la

# Make the source package
mkdir -p %{inst_srcdir}

find . -type f | grep -E '.*\.(c|h|am|ac|inc|m4|h.in|man.pre|pl|txt)$' | xargs tar cf - | (cd %{inst_srcdir} && tar xf -)
install -p -m 0644 Changes ev.pod LICENSE README %{inst_srcdir}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license LICENSE
%doc Changes README
%{_libdir}/%{name}.so.4
%{_libdir}/%{name}.so.4.0.0

%files devel
%{_includedir}/ev++.h
%{_includedir}/ev.h
%{_libdir}/%{name}.so
%{_mandir}/man?/*

#%files libevent-devel
#%{_includedir}/event.h

%files source
%{source_dir}


%changelog
