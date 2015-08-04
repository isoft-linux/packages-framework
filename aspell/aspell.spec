Summary: Spell checker
Name: aspell
Version: 0.60.6.1
Release: 12%{?dist}
Epoch: 12
# LGPLv2+ .. common/gettext.h
# LGPLv2  .. modules/speller/default/phonet.hpp,
#            modules/speller/default/phonet.cpp,
#            modules/speller/default/affix.cpp
# GPLv2+  .. ltmain.sh, misc/po-filter.c
# BSD     .. myspell/munch.c
License: LGPLv2+ and LGPLv2 and GPLv2+ and BSD
Group: Applications/Text
URL: http://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/aspell-%{version}.tar.gz

Patch0: aspell-0.60.3-install_info.patch
Patch1: aspell-0.60.5-fileconflict.patch
Patch2: aspell-0.60.5-pspell_conf.patch
# resolves: #447428
Patch3: aspell-0.60.6-zero.patch
Patch4: aspell-0.60.6-mp.patch
# resolves: #813261
Patch5: aspell-0.60.6.1-dump-personal-abort.patch
# resolves: #925034
Patch6: aspell-0.60.6.1-aarch64.patch

BuildRequires: chrpath, gettext, ncurses-devel, pkgconfig

%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It can
either be used as a library or as an independent spell checker. Its main
feature is that it does a much better job of coming up with possible
suggestions than just about any other spell checker out there for the
English language, including Ispell and Microsoft Word. It also has many
other technical enhancements over Ispell such as using shared memory for
dictionaries and intelligently handling personal dictionaries when more
than one Aspell process is open at once.

%package devel
Summary: Libraries and header files for Aspell development
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description devel
The aspell-devel package includes libraries
and header files needed for Aspell development.

%prep
%setup -q
%patch0 -p1 -b .iinfo
%patch1 -p1 -b .fc
%patch2 -p1 -b .mlib
%patch3 -p1 -b .zero
%patch4 -p1 -b .ai
%patch5 -p1 -b .dump-personal
%patch6 -p1 -b .aarch64
iconv -f iso-8859-2 -t utf-8 < manual/aspell.info > manual/aspell.info.aux
mv manual/aspell.info.aux manual/aspell.info

%build
%configure --disable-rpath
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}
cp scripts/aspell-import examples/aspell-import
chmod 644 examples/aspell-import
cp manual/aspell-import.1 examples/aspell-import.1

%install
# make install DESTDIR=$RPM_BUILD_ROOT doesn't work
%makeinstall

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60

mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/ispell ${RPM_BUILD_ROOT}%{_bindir}
mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/spell ${RPM_BUILD_ROOT}%{_bindir}

chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//nroff-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//sgml-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//context-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//email-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//tex-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//texinfo-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_bindir}/aspell
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/libpspell.so.*

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libaspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libpspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/*-filter.la
rm -f ${RPM_BUILD_ROOT}%{_bindir}/aspell-import
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/aspell-import.1

#we do not ship any info files.
rm -rf ${RPM_BUILD_ROOT}%{_infodir}

%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc README TODO COPYING examples/aspell-import examples/aspell-import.1
%dir %{_libdir}/aspell-0.60
%{_bindir}/a*
%{_bindir}/ispell
%{_bindir}/pr*
%{_bindir}/run-with-aspell
%{_bindir}/spell
%{_bindir}/word-list-compress
%{_libdir}/lib*.so.*
%{_libdir}/aspell-0.60/*
%{_mandir}/man1/aspell.1.*
%{_mandir}/man1/run-with-aspell.1*
%{_mandir}/man1/word-list-compress.1*
%{_mandir}/man1/prezip-bin.1.*

%files devel
%dir %{_includedir}/pspell
%{_bindir}/pspell-config
%{_includedir}/aspell.h
%{_includedir}/pspell/pspell.h
%{_libdir}/lib*spell.so
%{_libdir}/pkgconfig/*
%{_mandir}/man1/pspell-config.1*

%changelog
