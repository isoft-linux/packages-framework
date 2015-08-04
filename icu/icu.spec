Name:      icu
Version:   55.1 
Release:   3
Summary:   International Components for Unicode
Group:     Development/Tools
License:   MIT and UCD and Public Domain
URL:       http://www.icu-project.org/
Source0:   http://download.icu-project.org/files/icu4c/55.1/icu4c-55_1-src.tgz
#fix TestTwoDigitYear fail.
Patch1:     icu-testtwodigityear.patch
BuildRequires: autoconf
Requires: lib%{name} = %{version}-%{release}

%description
Tools and utilities for developing with icu.

%package -n lib%{name}
Summary: International Components for Unicode - libraries
Group:   System Environment/Libraries

%description -n lib%{name}
The International Components for Unicode (ICU) libraries provide
robust and full-featured Unicode services on a wide variety of
platforms. ICU supports the most current version of the Unicode
standard, and they provide support for supplementary Unicode
characters (needed for GB 18030 repertoire support).
As computing environments become more heterogeneous, software
portability becomes more important. ICU lets you produce the same
results across all the various platforms you support, without
sacrificing performance. It offers great flexibility to extend and
customize the supplied services.

%package  -n lib%{name}-devel
Summary:  Development files for International Components for Unicode
Group:    Development/Libraries
Requires: lib%{name} = %{version}-%{release}
Requires: pkgconfig

%description -n lib%{name}-devel
Includes and definitions for developing with icu.

%package -n lib%{name}-doc
Summary: Documentation for International Components for Unicode
Group:   Documentation

%description -n lib%{name}-doc
%{summary}.

%prep
%setup -q -n %{name}
%build
cd source
%configure --with-data-packaging=library --disable-samples
make %{?_smp_mflags} 
#make doc

%install
rm -rf $RPM_BUILD_ROOT source/__docs
make -C source install DESTDIR=$RPM_BUILD_ROOT
#make -C source install-doc docdir=__docs
sed -i s/\\\$\(THREADSCXXFLAGS\)// $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/icu*.pc
sed -i s/\\\$\(THREADSCPPFLAGS\)/-D_REENTRANT/ $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/icu*.pc

rpmclean

%check
make check -C source

%clean
rm -rf $RPM_BUILD_ROOT

%post -n lib%{name} -p /sbin/ldconfig

%postun -n lib%{name} -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/derb
%{_bindir}/genbrk
%{_bindir}/gencfu
%{_bindir}/gencnval
%{_bindir}/genrb
%{_bindir}/gendict
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv
%{_sbindir}/*
%{_mandir}/man1/derb.1*
%{_mandir}/man1/gencnval.1*
%{_mandir}/man1/genrb.1*
%{_mandir}/man1/genbrk.1*
%{_mandir}/man1/gencfu.1*
%{_mandir}/man1/gendict.1*
%{_mandir}/man1/makeconv.1*
%{_mandir}/man1/pkgdata.1*
%{_mandir}/man1/uconv.1*
%{_mandir}/man8/*.8*

%files -n lib%{name}
%defattr(-,root,root,-)
%doc license.html readme.html
%{_libdir}/*.so.*

%files -n lib%{name}-devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_bindir}/icuinfo
%{_mandir}/man1/%{name}-config.1*
%{_includedir}/layout
%{_includedir}/unicode
%{_libdir}/*.so
%{_libdir}/pkgconfig/icu*.pc
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%{_datadir}/%{name}/%{version}/install-sh
%{_datadir}/%{name}/%{version}/mkinstalldirs
%{_datadir}/%{name}/%{version}/config
%doc %{_datadir}/%{name}/%{version}/license.html

#%files -n lib%{name}-doc
#%defattr(-,root,root,-)
#%doc license.html readme.html
#%doc source/__docs/%{name}/html/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

