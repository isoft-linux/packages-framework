Name:		libotf
Version:	0.9.13
Release:	6%{?dist}
Summary:	A Library for handling OpenType Font

Group:		System Environment/Libraries
License:	LGPLv2+
URL:            http://www.nongnu.org/m17n/
Source0:        http://download.savannah.gnu.org/releases/m17n/%{name}-%{version}.tar.gz

BuildRequires:	gcc chrpath freetype-devel libXaw-devel
Requires:	freetype

%description 
The library "libotf" provides the following facilites.
Read Open Type Layout Tables from OTF file. Currently these tables are
supported; head, name, cmap, GDEF, GSUB, and GPOS.  Convert a Unicode
character sequence to a glyph code sequence by using the above tables.
The combination of libotf and the FreeType library (Ver.2) realizes
CTL (complex text layout) by OpenType fonts. This library is currently
used by the m17n library. It seems that the probject Free Type Layout
provides the similar (or better) facility as this library, but
currently they have not yet released their library. So, we have
developed this one.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
for file in $RPM_BUILD_ROOT/usr/bin/*; do chrpath -d $file || true; done

(cd example && make clean && rm -rf .deps && rm Makefile)
rm $RPM_BUILD_ROOT/usr/bin/libotf-config

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README NEWS
%{_libdir}/*.so.*
%{_bindir}/otfdump
%{_bindir}/otflist
%{_bindir}/otftobdf
%{_bindir}/otfview

%files devel
%doc example
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
