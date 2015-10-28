Summary: An Enchanting Spell Checking Library
Name: enchant
Version: 1.6.0
Release: 3
Epoch: 1
License: LGPL
Source: http://www.abisource.com/downloads/enchant/%{version}/enchant-%{version}.tar.gz
URL: http://www.abisource.com/
BuildRequires: glib2-devel >= 2.0.0
BuildRequires: hunspell-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
A library that wraps other spell checking backends.

%package devel
Summary: Support files necessary to compile applications with libenchant.
Requires: enchant = %{epoch}:%{version}-%{release}
Requires: glib2-devel

%description devel
Libraries, headers, and support files necessary to compile applications using libenchant.

%prep
%setup -q

%build
%configure --disable-ispell --disable-aspell --disable-hspell --with-myspell-dir=/usr/share/myspell
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/enchant/*.la

%files
%defattr(-,root,root)
%doc AUTHORS COPYING.LIB README
%{_bindir}/*
%{_libdir}/lib*.so.*
%dir %{_libdir}/enchant
%{_libdir}/enchant/lib*.so*
%{_mandir}/man1/enchant.1.gz
%{_datadir}/enchant

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/enchant/*.a
%{_libdir}/pkgconfig/enchant.pc
%{_includedir}/enchant

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sat Oct 24 2015 builder - 1:1.6.0-3
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

