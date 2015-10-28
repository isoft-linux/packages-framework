Name:           liboggz
Version:        1.1.1
Release:        10%{?dist}
Summary:        Simple programming interface for Ogg files and streams

License:        BSD
URL:            http://www.xiph.org/oggz/
Source0:        http://downloads.xiph.org/releases/liboggz/%{name}-%{version}.tar.gz

BuildRequires:  libogg-devel >= 1.0
BuildRequires:  doxygen
BuildRequires:  docbook-utils

%description
Oggz provides a simple programming interface for reading and writing
Ogg files and streams. Ogg is an interleaving data container developed
by Monty at Xiph.Org, originally to support the Ogg Vorbis audio
format.

%package devel
Summary:	Files needed for development using liboggz
Requires:       liboggz = %{version}-%{release}
Requires:       libogg-devel >= 1.0
Requires:       pkgconfig

%description devel
Oggz provides a simple programming interface for reading and writing
Ogg files and streams. Ogg is an interleaving data container developed
by Monty at Xiph.Org, originally to support the Ogg Vorbis audio
format.

This package contains the header files and documentation needed for
development using liboggz.

%package doc
Summary:        Documentation for liboggz
Requires:	liboggz = %{version}-%{release}

%description doc
Oggz provides a simple programming interface for reading and writing
Ogg files and streams. Ogg is an interleaving data container developed
by Monty at Xiph.Org, originally to support the Ogg Vorbis audio
format.

This package contains HTML documentation needed for development using
liboggz.


%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-static
make %{?_smp_mflags}


%check
# Tests disabled for moment because of rpath issue
#make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall docdir=$PWD/__docs_staging INSTALL="%{__install} -p"

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# not particularly interested in the tex docs, the html version has everything
rm -rf __docs_staging/latex


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

                                                                                
%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README
# 0 length NEWS file
# %doc NEWS
%{_libdir}/liboggz.so.*
%{_mandir}/man1/*
%{_bindir}/oggz*

%files devel
%defattr(-,root,root)
%{_includedir}/oggz
%{_libdir}/liboggz.so
%{_libdir}/pkgconfig/oggz.pc

%files doc
%defattr(-,root,root)
%doc __docs_staging/*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.1.1-10
- Rebuild for new 4.0 release.

