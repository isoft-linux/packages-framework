Name:      hunspell
Summary:   Hunspell is a spell checker and morphological analyzer library
Version:   1.3.3
Release:   1 
Source0:   http://downloads.sourceforge.net/%{name}/hunspell-%{version}.tar.gz
Patch0:     hunspell-musl-fix-includes.patch

Group:     System Environment/Libraries
URL:       http://hunspell.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:   LGPLv2+ or GPLv2+ or MPLv1.1
BuildRequires: libtool, ncurses-devel

%description
Hunspell is a spell checker and morphological analyzer library and program 
designed for languages with rich morphology and complex word compounding or 
character encoding. Hunspell interfaces: Ispell-like terminal interface using 
Curses library, Ispell pipe interface, OpenOffice.org UNO module.

%package devel
Requires: hunspell = %{version}-%{release}, pkgconfig
Summary: Files for developing with hunspell
Group: Development/Libraries

%description devel
Includes and definitions for developing with hunspell

%prep
%setup -q
%patch0 -p1
# Filter unwanted Requires for the "use explicitely" string in ispellaff2myspell
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(explicitely)/d'
EOF

%define __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build
libtoolize --automake -if
aclocal -I m4
autoconf
automake --add-missing
%configure --disable-static  --with-ui --with-readline
for i in man/*.? man/hu/*.?; do
    iconv -f ISO-8859-2 -t UTF-8 $i > $i.new
    mv -f $i.new $i
done
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
%find_lang %{name}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_bindir}/example
mkdir $RPM_BUILD_ROOT/%{_datadir}/myspell
install -m 755 src/tools/affixcompress $RPM_BUILD_ROOT/%{_bindir}/affixcompress
install -m 755 src/tools/makealias $RPM_BUILD_ROOT/%{_bindir}/makealias
rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_datadir}/myspell
%{_bindir}/hunspell
%{_mandir}/man1/hunspell.1.gz
%{_mandir}/man5/hunspell.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/*.so
%{_bindir}/affixcompress
%{_bindir}/makealias
%{_bindir}/munch
%{_bindir}/unmunch
%{_bindir}/wordforms
%{_bindir}/analyze
%{_bindir}/chmorph
%{_bindir}/hzip
%{_bindir}/hunzip
%{_bindir}/ispellaff2myspell
%{_bindir}/wordlist2hunspell
%{_libdir}/pkgconfig/hunspell.pc
%{_mandir}/man1/hunzip.1.gz
%{_mandir}/man1/hzip.1.gz
%{_mandir}/man3/hunspell.3.gz

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

