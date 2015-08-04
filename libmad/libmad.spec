# $Id: libmad.spec,v 1.1 2007/09/01 10:22:23 cjacker Exp $
# Authority: matthias

Summary: MPEG audio decoding library
Name: libmad
Version: 0.15.1b
Release: 2
License: GPL
Group: System Environment/Libraries
URL: http://www.underbit.com/products/mad/
Source: ftp://ftp.mars.org/pub/mpeg/%{name}-%{version}.tar.gz
Patch0: libmad-clang.patch
Patch1: libmad-gcc5.patch

Provides: mad = %{version}-%{release}

%description
MAD (libmad) is a high-quality MPEG audio decoder. It currently supports
MPEG-1 and the MPEG-2 extension to Lower Sampling Frequencies, as well as
the so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.
 
MAD does not yet support MPEG-2 multichannel audio (although it should be
backward compatible with such streams) nor does it currently support AAC.


%package devel
Summary: Header and library for developing programs that will use libmad
Group: Development/Libraries
Requires: %{name} = %{version}, pkgconfig

%description devel
MAD (libmad) is a high-quality MPEG audio decoder. It currently supports
MPEG-1 and the MPEG-2 extension to Lower Sampling Frequencies, as well as
the so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

This package contains the header file as well as the static library needed
to develop programs that will use libmad for mpeg audio decoding.


%prep
%setup
#%patch -p1
%patch1 -p1

# Create an additional pkgconfig file
%{__cat} << EOF > mad.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{_libdir} -lmad -lm
Cflags: -I%{_includedir}
EOF


%build
touch NEWS AUTHORS ChangeLog
autoreconf -ivf
CFLAGS="-fPIC $RPM_OPT_FLAGS" CXXFLAGS="-fPIC $RPM_OPT_FLAGS" %configure \
    --disable-dependency-tracking \
    --enable-accuracy \
    --disable-debugging
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__install} -D -m 0644 mad.pc %{buildroot}%{_libdir}/pkgconfig/mad.pc


%clean
%{__rm} -rf %{buildroot}


%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%files 
%defattr(-, root, root, 0755)
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

