Name: libcdio-paranoia
Version: 10.2+0.90+1
Release: 1 
Summary: CD paranoia on top of libcdio
Group: System Environment/Libraries
License: GPLv2+ and LGPLv2+
URL: http://www.gnu.org/software/libcdio/
Source0: http://ftp.gnu.org/gnu/libcdio/libcdio-paranoia-%{version}.tar.gz
Patch0: libcdio-paranoia-manpage.patch
BuildRequires: pkgconfig 
BuildRequires: gettext-devel
BuildRequires: chrpath
BuildRequires: libcdio-devel

%description
This CDDA reader distribution ('libcdio-cdparanoia') reads audio from the
CDROM directly as data, with no analog step between, and writes the
data to a file or pipe as .wav, .aifc or as raw 16 bit linear PCM.

Split off from libcdio to allow more flexible licensing and to be compatible
with cdparanoia-III-10.2's license. And also, libcdio is just too large.

%package devel
Summary: Header files and libraries for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains header files and libraries for %{name}.


%prep
%setup -q
%patch0 -p1

# fix pkgconfig files
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_paranoia.pc.in
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_cdda.pc.in

f=doc/ja/cd-paranoia.1.in
iconv -f euc-jp -t utf-8 -o $f.utf8 $f && mv $f.utf8 $f
iconv -f ISO88591 -t utf-8 -o THANKS.utf8 THANKS && mv THANKS.utf8 THANKS

%build
%configure \
	--disable-dependency-tracking \
	--disable-static \
	--disable-rpath
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

mv $RPM_BUILD_ROOT%{_mandir}/{jp,ja}

# copy include files to an additional directory for backward compatibility
# this is where most software still expects those files
cp -a $RPM_BUILD_ROOT%{_includedir}/cdio/paranoia/*.h $RPM_BUILD_ROOT%{_includedir}/cdio/

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so.*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README THANKS COPYING-GPL COPYING-LGPL
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*


%files devel
%defattr(-,root,root,-)
%doc doc/FAQ.txt doc/overlapdef.txt
%{_includedir}/cdio/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
