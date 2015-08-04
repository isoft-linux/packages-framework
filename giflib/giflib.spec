Summary:	Library for manipulating GIF format image files
Name:		giflib
Version:    5.1.1
Release:    8	
License:	MIT
Group:		System Environment/Libraries
URL:		http://www.sourceforge.net/projects/%{name}/
Source:		http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Provides:	libungif = %{version}-%{release}
Obsoletes:	libungif <= %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The giflib package contains a shared library of functions for loading and
saving GIF format image files. It is API and ABI compatible with libungif,
the library which supported uncompressed GIFs while the Unisys LZW patent
was in effect.

%package devel
Summary:	Development tools for programs using the giflib library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	libungif-devel = %{version}-%{release}
Obsoletes:	libungif-devel <= %{version}-%{release}

%description devel
The giflib-devel package includes header files, libraries necessary for
developing programs which use the giflib library to load and save GIF format
image files. It contains the documentation of the giflib library, too.

%package utils
Summary:	Programs for manipulating GIF format image files
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Provides:	libungif-progs = %{version}-%{release}
Obsoletes:	libungif-progs <= %{version}-%{release}

%description utils
The giflib-utils package contains various programs for manipulating GIF
format image files. Install it if you need to manipulate GIF format image
files.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} all

# Handling of libungif compatibility
MAJOR=`echo '%{version}' | sed -e 's/\([0-9]\+\)\..*/\1/'`
%{__cc} $RPM_OPT_FLAGS -shared -Wl,-soname,libungif.so.$MAJOR -Llib/.libs -lgif -o libungif.so.%{version}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Handling of libungif compatibility
install -p -m 755 libungif.so.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -sf libungif.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libungif.so.4
ln -sf libungif.so.4 $RPM_BUILD_ROOT%{_libdir}/libungif.so

# Don't install any static .a and libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

# Remove makefile relics from documentation
rm -f doc/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*
%files devel
%defattr(-,root,root,-)
%doc doc/* util/giffiltr.c util/gifspnge.c
%{_libdir}/lib*.so
%{_includedir}/*.h

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

