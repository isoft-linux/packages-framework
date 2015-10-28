# note this duplicates native anthy IMEs
%bcond_without anthy

Name:           m17n-lib
Version:        1.7.0
Release:        4%{?dist}
Summary:        Multilingual text library

License:        LGPLv2+
URL:            http://www.nongnu.org/m17n/
Source0:        http://download.savannah.gnu.org/releases/m17n/%{name}-%{version}.tar.gz
Patch0:         %{name}-1.6.1-multilib.patch

BuildRequires:  m17n-db-devel libthai-devel
BuildRequires:  libxml2-devel libXft-devel
BuildRequires:  fontconfig-devel freetype-devel
BuildRequires:  fribidi-devel gd-devel
BuildRequires:  libXaw-devel libotf-devel
BuildRequires:  autoconf gettext-devel
BuildRequires:  automake libtool

%if %{with anthy}
BuildRequires:  anthy-devel
%endif

Requires:       m17n-db

%description
m17n-lib is a multilingual text library used primarily to allow
the input of many languages with the input table maps from m17n-db.

The package provides the core and input method backend libraries.

%package  anthy
Summary:  Anthy module for m17n
Requires: %{name}%{?_isa} = %{version}-%{release}

%description anthy
Anthy module for %{name} allows ja-anthy.mim to support input conversion.


%package  devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-tools = %{version}-%{release}

%description devel
Development files for %{name}.


%package  tools
Summary:  m17n GUI Library tools
Requires: m17n-db-extras
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to test M17n GUI widget library.


%prep
%setup -q 
%patch0 -p1

%build
autoreconf -ivf
%configure --disable-rpath --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# parallel make usage with make command fails build on koji
make

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
# fix bug rh#680363
rm $RPM_BUILD_ROOT%{_libdir}/m17n/1.0/libmimx-ispell.so

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post tools -p /sbin/ldconfig
%postun tools -p /sbin/ldconfig

%files
%doc AUTHORS COPYING NEWS ChangeLog README
#Own module directory path
%dir %{_libdir}/m17n
%dir %{_libdir}/m17n/1.0
%{_bindir}/m17n-conv
%{_libdir}/libm17n.so.*
%{_libdir}/libm17n-core.so.*
%{_libdir}/libm17n-flt.so.*

#Anthy module
%files anthy
%{_libdir}/m17n/1.0/libmimx-anthy.so

%files devel
%{_bindir}/m17n-config
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%files tools
%{_bindir}/m17n-date
%{_bindir}/m17n-dump
%{_bindir}/m17n-edit
%{_bindir}/m17n-view
%{_libdir}/m17n/1.0/libm17n-X.so
%{_libdir}/m17n/1.0/libm17n-gd.so
%{_libdir}/libm17n-gui.so.*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.7.0-4
- Rebuild for new 4.0 release.

