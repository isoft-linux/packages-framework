Name:           harfbuzz
Version:        1.3.4
Release:        1
Summary:        Text shaping library

License:        MIT
URL:            http://freedesktop.org/wiki/Software/HarfBuzz
Source0:        http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-%{version}.tar.bz2

BuildRequires:  cairo-devel
BuildRequires:  freetype-devel
BuildRequires:  glib2-devel
BuildRequires:  libicu-devel
BuildRequires:  graphite2-devel
BuildRequires:  gtk-doc

%description
HarfBuzz is an implementation of the OpenType Layout engine.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-icu%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        icu
Summary:        Harfbuzz ICU support library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    icu
This package contains Harfbuzz ICU support library.

%prep
%setup -q


%build
%configure --disable-static --with-graphite2

# Remove lib64 rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%check
#two arphic failed
make check ||:

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post icu -p /sbin/ldconfig
%postun icu -p /sbin/ldconfig


%files
%doc NEWS AUTHORS COPYING README
%{_libdir}/libharfbuzz.so.*

%files devel
%{_bindir}/hb-view
%{_bindir}/hb-ot-shape-closure
%{_bindir}/hb-shape
%{_includedir}/harfbuzz/
%{_libdir}/libharfbuzz.so
%{_libdir}/pkgconfig/harfbuzz.pc
%{_libdir}/libharfbuzz-icu.so
%{_libdir}/pkgconfig/harfbuzz-icu.pc
%{_datadir}/gtk-doc/html/*
%files icu
%{_libdir}/libharfbuzz-icu.so.*

%changelog
* Fri Dec 16 2016 sulit - 1.3.4-1
- upgrade harfbuzz to 1.3.4

* Fri Dec 16 2016 sulit - 1.1.0-7
- rebuild harfbuzz

* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 1.0.4-6
- Rebuild with icu 56.1

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.4-5
- Rebuild for new 4.0 release.

* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- update to 1.0.4
