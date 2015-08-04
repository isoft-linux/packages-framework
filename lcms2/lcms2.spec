Name:           lcms2
Version:        2.7
Release:        6
Summary:        Color Management Engine
License:        MIT
URL:            http://www.littlecms.com/
Source0:        http://www.littlecms.com/%{name}-%{version}.tar.gz

BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  zlib-devel

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

%package        utils
Summary:        Utility applications for %{name}
Group:          Applications/Productivity

%description    utils
The %{name}-utils package contains utility applications for %{name}.

%package        devel
Summary:        Development files for LittleCMS
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       littlecms-devel = %{version}-%{release}

%description    devel
Development files for LittleCMS.

%prep
%setup -q

%build
%configure --disable-static --program-suffix=2

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'
install -D -m 644 include/lcms2.h $RPM_BUILD_ROOT/usr/include/lcms2.h
install -D -m 644 include/lcms2_plugin.h $RPM_BUILD_ROOT/usr/include/lcms2_plugin.h

rpmclean
%clean
rm -rf ${RPM_BUILD_ROOT}

%check
LD_LIBRARY_PATH=`pwd`/src/.libs make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

