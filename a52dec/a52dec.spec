Summary: A free library for decoding ATSC A/52 (also known as AC-3) streams.
Name: a52dec 
Version: 0.7.4 
Release: 5
License: GPL
URL:    http://liba52.sourceforge.net/files/
Source: http://liba52.sourceforge.net/files/%{name}-%{version}.tar.gz
%description
liba52 is a free library for decoding ATSC A/52 (also known as AC-3) streams. 
The A/52 standard is used in a variety of applications, including digital television and DVD. 
%package devel
Summary: Shared libraries for a52dec
Requires: %{name} = %{version}

%description devel
Shared libraries for a52dec
%prep
%setup -q

%build
export CFLAGS="-fPIC"
%configure --disable-static --enable-shared
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.7.4-5
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

