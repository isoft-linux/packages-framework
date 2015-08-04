%global libiconv_version 1.12

Name: enca
Summary: Character set analyzer and detector
Version: 1.13
Release: 1 
License: GPLv2
Group: Applications/Text
Source: http://dl.cihar.com/enca/enca-%{version}.tar.bz2

URL: http://gitorious.org/enca

%description
Enca is an Extremely Naive Charset Analyser. It detects character set and
encoding of text files and can also convert them to other encodings using
either a built-in converter or external libraries and tools like libiconv,
librecode, or cstocs.

Currently, it has support for Belarussian, Bulgarian, Croatian, Czech,
Estonian, Latvian, Lithuanian, Polish, Russian, Slovak, Slovene, Ukrainian,
Chinese and some multibyte encodings (mostly variants of Unicode)
independent on the language.

This package also contains shared Enca library other programs can make use of.

Install %{name} if you need to cope with text files of dubious origin
and unknown encoding and convert them to some reasonable encoding.


%package devel
Summary: Header files and libraries for %{name} charset analyzer
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains the static libraries and header files
for writing programs using the Extremely Naive Charset Analyser library,
and its API documentation.

Install %{name}-devel if you are going to create applications using the Enca
library.


%prep
%setup -q 
%build
%configure \
	--disable-dependency-tracking \
	--without-librecode \
	--disable-external \
	%{!?_with_static:--disable-static} \
	--disable-gtk-doc

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT HTML_DIR=/tmp/html

rm -rf $RPM_BUILD_ROOT/tmp/html
rm -rf $RPM_BUILD_ROOT/%{_libexecdir}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la


%check
#iconv check will fail even with libiconv
#make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libenca.so.*
%{_mandir}/*/*
%doc AUTHORS COPYING FAQ README THANKS TODO

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%doc devel-docs/html/*.html README.devel


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

