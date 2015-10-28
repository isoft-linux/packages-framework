Name:		libhangul
Version:	0.1.0
Release:	12%{?dist}

License:	LGPLv2+
URL:		https://code.google.com/p/libhangul/
Source0:	https://libhangul.googlecode.com/files/libhangul-%{version}.tar.gz

Summary:	Hangul input library
Requires(post):	/sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:	  gettext-devel, automake, libtool


%description
libhangul provides common features for Hangul input method programs.


%package devel
Summary:	Development files for libhangul
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
%description devel
This package contains development files necessary to develop programs
providing Hangul input.


%prep
%setup -q
autoreconf -fi

%build
%configure --disable-static

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rm $RPM_BUILD_ROOT%{_libdir}/%{name}.la
%find_lang %{name}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/lib*.so.*
%{_datadir}/%{name}
%{_bindir}/hangul

%files devel
%defattr(-, root, root)
%{_includedir}/hangul-*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.1.0-12
- Rebuild for new 4.0 release.

