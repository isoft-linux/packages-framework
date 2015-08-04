Name: libcdio
Version: 0.92
Release: 1
Summary: CD-ROM input and control library
Group: System Environment/Libraries
License: GPLv3+
URL: http://www.gnu.org/software/libcdio/
Source0: http://ftp.gnu.org/gnu/libcdio/libcdio-0.92.tar.gz
Source1: http://ftp.gnu.org/gnu/libcdio/libcdio-0.92.tar.gz.sig
Source2: libcdio-no_date_footer.hml
Source3: cdio_config.h
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig doxygen
BuildRequires: ncurses-devel
Requires(post): /sbin/ldconfig
BuildRequires: gettext-devel
BuildRequires: chrpath


%description
This library provides an interface for CD-ROM access. It can be used
by applications that need OS- and device-independent access to CD-ROM
devices.

%package devel
Summary: Header files and libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains header files and libraries for %{name}.


%prep
%setup -q

f=src/cd-paranoia/doc/ja/cd-paranoia.1.in
iconv -f euc-jp -t utf-8 -o $f.utf8 $f && mv $f.utf8 $f
iconv -f ISO88591 -t utf-8 -o THANKS.utf8 THANKS && mv THANKS.utf8 THANKS

%build
%configure \
	--disable-vcd-info \
	--disable-dependency-tracking \
	--disable-cddb \
	--disable-static \
	--disable-rpath
make %{?_smp_mflags}

# another multilib fix; remove the architecture information from version.h
sed -i -e "s,%{version}.*$,%{version}\\\",g" include/cdio/version.h

cd doc/doxygen
sed -i -e "s,HTML_FOOTER.*$,HTML_FOOTER = libcdio-no_date_footer.hml,g; \
		s,EXCLUDE .*$,EXCLUDE = ../../include/cdio/cdio_config.h,g;" Doxyfile
cp %{SOURCE2} .
./run_doxygen

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# multilib header hack; taken from postgresql.spec
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x | sparc | sparc64 )
		mv $RPM_BUILD_ROOT%{_includedir}/cdio/cdio_config.h $RPM_BUILD_ROOT%{_includedir}/cdio/cdio_config_`uname -i`.h
		install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_includedir}/cdio
		;;
	*)
		;;
esac

rm -rf $RPM_BUILD_ROOT%{_infodir}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

rm -rf examples
mkdir -p examples/C++
cp -a example/{*.c,README} examples
cp -a example/C++/{*.cpp,README} examples/C++

# fix timestamps of generated man-pages
for i in cd-info iso-read iso-info cd-read cd-drive; do 
	# remove build architecture information from man pages
	sed -i -e 's, version.*linux-gnu,,g' $RPM_BUILD_ROOT%{_mandir}/man1/$i.1
	# remove libtool leftover from man pages
	sed -i -e 's,lt-,,g;s,LT-,,g' $RPM_BUILD_ROOT%{_mandir}/man1/$i.1
	# fix timestamps to be the same in all packages
done

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so.*

%check
# disable test using local CDROM
%{__sed} -i -e "s,testiso9660\$(EXEEXT),,g" \
	    -e "s,testisocd\$(EXEEXT),,g" \
	    -e "s,check_paranoia.sh check_opts.sh, check_opts.sh,g" \
	    test/Makefile
#realpath failed.
#make check


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README README.libcdio THANKS TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*


%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/html examples
%{_includedir}/cdio
%{_includedir}/cdio++
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
