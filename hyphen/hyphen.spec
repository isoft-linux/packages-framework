Name:      hyphen
Summary:   A text hyphenation library
Version:   2.8.8
Release:   3
Source:    http://downloads.sourceforge.net/hunspell/hyphen-%{version}.tar.gz
URL:       http://hunspell.sf.net
License:   GPLv2 or LGPLv2+ or MPLv1.1
BuildRequires: perl, patch, autoconf, automake, libtool

%ifarch %{ix86} x86_64
BuildRequires: valgrind
%endif

%description
Hyphen is a library for high quality hyphenation and justification.

%package devel
Requires: hyphen = %{version}-%{release}
Summary: Files for developing with hyphen

%description devel
Includes and definitions for developing with hyphen

%package en
Requires: hyphen
Summary: English hyphenation rules
BuildArch: noarch

%description en
English hyphenation rules.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%check
#%ifarch %{ix86} x86_64, see rhbz#813780
%ifarch %{ix86}
VALGRIND=memcheck make check
%else
make check
%endif

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

pushd $RPM_BUILD_ROOT/%{_datadir}/hyphen/
en_US_aliases="en_AG en_AU en_BS en_BW en_BZ en_CA en_DK en_GB en_GH en_HK en_IE en_IN en_JM en_MW en_NA en_NZ en_PH en_SG en_TT en_ZA en_ZM en_ZW"
for lang in $en_US_aliases; do
        ln -s hyph_en_US.dic hyph_$lang.dic
done
popd


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%dir %{_datadir}/hyphen

%files en
%defattr(-,root,root,-)
%{_datadir}/hyphen/hyph_en*.dic

%files devel
%defattr(-,root,root,-)
%{_includedir}/hyphen.h
%{_libdir}/*.so
%{_bindir}/substrings.pl

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.8.8-3
- Rebuild for new 4.0 release.

