%global snapshot 0

Name:           libpinyin
Version:        1.1.0
Release:        3
Summary:        Library to deal with pinyin

License:        GPLv2+
URL:            https://github.com/libpinyin/libpinyin
Source0:        http://downloads.sourceforge.net/libpinyin/libpinyin/%{name}-%{version}.tar.gz
%if %snapshot
Patch0:         libpinyin-1.0.x-head.patch
%endif

BuildRequires:  libdb-devel, glib2-devel
Requires:       %{name}-data%{?_isa} = %{version}-%{release}

%description
The libpinyin project aims to provide the algorithms core
for intelligent sentence-based Chinese pinyin input methods.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        data
Summary:        Data files for %{name}
Requires:       %{name} = %{version}-%{release}

%description data
The %{name}-data package contains data files.

%package        tools
Summary:        Tools for %{name}
Requires:       %{name} = %{version}-%{release}

%description tools
The %{name}-tools package contains tools.


%prep
%setup -q

%if %snapshot
%patch0 -p1 -b .head
%endif

%build
%configure --disable-static
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README
%{_libdir}/*.so.*
%dir %{_libdir}/libpinyin

%files devel
%doc
%dir %{_includedir}/libpinyin-%{version}
%{_includedir}/libpinyin-%{version}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libpinyin.pc

%files data
%doc
%{_libdir}/libpinyin/data

%files tools
%{_bindir}/gen_binary_files
%{_bindir}/import_interpolation
%{_bindir}/gen_unigram
%{_mandir}/man1/*.1.*


%changelog
