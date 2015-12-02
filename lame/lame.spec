Summary: LAME Ain't an MP3 Encoder... but it's the best of all
Name: lame
Version: 3.99.5
Release: 2%{?dist}
License: LGPL
URL: http://lame.sourceforge.net/
Source: http://dl.sf.net/project/lame/lame/3.99/lame-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: gtk2-devel
BuildRequires: libtool
BuildRequires: libvorbis-devel
BuildRequires: ncurses-devel
BuildRequires: nasm
Provides: mp3encoder

%description
LAME is an educational tool to be used for learning about MP3 encoding.  The
goal of the LAME project is to use the open source model to improve the
psychoacoustics, noise shaping and speed of MP3. Another goal of the LAME
project is to use these improvements for the basis of a patent-free audio
compression codec for the GNU project.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup

%build
%configure \
    --disable-dependency-tracking \
    --disable-static \
    --enable-nasm

%{__make} test CFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

### Some apps still expect to find <lame.h>
%{__ln_s} -f lame/lame.h %{buildroot}%{_includedir}/lame.h

### Clean up documentation to be included
find doc/html -name "Makefile*" | xargs rm -f
%{__rm} -rf %{buildroot}%{_docdir}/lame/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc ChangeLog COPYING INSTALL* doc/html/
%doc LICENSE README TODO USAGE
%doc %{_mandir}/man1/lame.1*
%{_bindir}/lame
%{_libdir}/libmp3lame.so.*

%files devel
%doc API DEFINES HACKING STYLEGUIDE
%{_includedir}/lame/
%{_includedir}/lame.h
%{_libdir}/libmp3lame.so

%changelog
* Wed Dec 02 2015 Cjacker <cjacker@foxmail.com> - 3.99.5-2
- Initial build

