Name:		libwebp
Version:	0.4.3
Release:	1
Group:		Development/Libraries
URL:		http://webmproject.org/
Summary:	Library and tools for the WebP graphics format
# Additional IPR is licensed as well. See PATENTS file for details
License:	BSD
Source0:	 http://downloads.webmproject.org/releases/webp/libwebp-%{version}.tar.gz
BuildRequires:	libjpeg-devel libpng-devel libtool
BuildRequires:  giflib-devel
BuildRequires:  libtiff-devel

%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package tools
Group:		Development/Tools
Summary:	The WebP command line tools

%description tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package devel
Group:		Development/Libraries
Summary:	Development files for libwebp, a library for the WebP format
Requires:	%{name} = %{version}-%{release}

%description devel
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%prep
%setup -q

%build
%configure \
    --disable-static \
    --enable-libwebpmux \
    --enable-libwebpdemux \
    --enable-libwebpdecoder

make %{?_smp_mflags}

%install
%make_install
rpmclean

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files tools
%{_bindir}/cwebp
%{_bindir}/dwebp
%{_bindir}/vwebp
%{_bindir}/gif2webp
%{_bindir}/webpmux
%{_mandir}/man*/*

%files -n %{name}
%{_libdir}/%{name}*.so.*

%files devel
%{_libdir}/%{name}*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

