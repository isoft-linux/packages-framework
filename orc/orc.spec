Name:		orc
Version:	0.4.24
Release:    2	
Summary:	The Oil Run-time Compiler

License:	BSD
URL:		http://cgit.freedesktop.org/gstreamer/orc/
Source0:	http://code.entropywave.com/download/orc/orc-%{version}.tar.xz

BuildRequires:	gtk-doc, libtool

%description
Orc is a library and set of tools for compiling and executing
very simple programs that operate on arrays of data.  The "language"
is a generic assembly language that represents many of the features
available in SIMD architectures, including saturated addition and
subtraction, and many arithmetic operations.

%package doc
Summary:	Documentation for Orc
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for Orc.

%package devel
Summary:	Development files and libraries for Orc
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-compiler
Requires:	pkgconfig

%description devel
This package contains the files needed to build packages that depend
on orc.

%package compiler
Summary:	Orc compiler
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description compiler
The Orc compiler, to produce optimized code.



%prep
%setup -q

%build
%configure --disable-static --enable-gtk-doc --enable-user-codemem

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

# Remove unneeded files.
find %{buildroot}/%{_libdir} -name \*.a -or -name \*.la -delete
rm -rf %{buildroot}/%{_libdir}/orc

touch -r stamp-h1 %{buildroot}%{_includedir}/%{name}-0.4/orc/orc-stdint.h   


%clean
rm -rf %{buildroot}


%check
%ifnarch s390 s390x ppc ppc64 %{arm} i686
make check
%endif


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig



%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/liborc-*.so.*
%{_bindir}/orc-bugreport

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/orc/

%files devel
%defattr(-,root,root,-)
%doc examples/*.c
%{_includedir}/%{name}-0.4/
%{_libdir}/liborc-*.so
%{_libdir}/pkgconfig/orc-0.4.pc
%{_datadir}/aclocal/orc.m4

%files compiler
%defattr(-,root,root,-)
%{_bindir}/orcc



%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.4.24-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

