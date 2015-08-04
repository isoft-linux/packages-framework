Name:		libhangul
Version:	0.1.0
Release:	11%{?dist}

License:	LGPLv2+
URL:		https://code.google.com/p/libhangul/
Source0:	https://libhangul.googlecode.com/files/libhangul-%{version}.tar.gz

Summary:	Hangul input library
Group:		System Environment/Libraries
Requires(post):	/sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:	  gettext-devel, automake, libtool


%description
libhangul provides common features for Hangul input method programs.


%package devel
Summary:	Development files for libhangul
Group:		Development/Libraries
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
