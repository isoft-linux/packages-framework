Summary: An encoder/decoder for the Free Lossless Audio Codec.
Name:    libflac
Version: 1.3.1
Release: 3 
License: LGPL/GPL
Source: https://svn.xiph.org/releases/flac/flac-%{version}.tar.xz
URL:    http://flac.sourceforge.net/

Provides: flac = %{version}-%{release}
BuildRequires: glib2-devel, libogg-devel, nasm
BuildRequires: libtool, gettext-devel
Obsoletes: flac-libs
Obsoletes: xmms-flac < 1.1.2-24

%description
FLAC stands for Free Lossless Audio Codec. Grossly oversimplified, FLAC
is similar to Ogg Vorbis, but lossless. The FLAC project consists of
the stream format, reference encoders and decoders in library form,
flac, a command-line program to encode and decode FLAC files, metaflac,
a command-line metadata editor for FLAC files and input plugins for
various music players.

%package devel
Summary: Static libraries and header files from FLAC.
Requires: %{name} = %{version}-%{release}
Provides: flac-devel = %{version}-%{release}

%description devel
This package contains all the files needed to develop applications that
will use the Free Lossless Audio Codec.

%prep
%setup -q -n flac-%{version}

%build
export XMMS_CONFIG=no 
%configure --with-pic

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
find doc/ -name "Makefile*" -exec rm -f {} \;
rm -rf $RPM_BUILD_ROOT/usr/share/doc

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root,-)
#%doc AUTHORS COPYING* README
%{_bindir}/flac
%{_bindir}/metaflac
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
#%doc doc/html
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/aclocal/*.m4
%{_libdir}/pkgconfig/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.3.1-3
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

