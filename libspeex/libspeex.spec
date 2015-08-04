Summary:	A voice compression format (codec)
Name:		libspeex
Version: 	1.2	
%define rc_ver	rc2
Release:	1.12.%{rc_ver}
License:	BSD
Group:		System Environment/Libraries
URL:		http://www.speex.org/
Source0:	http://downloads.xiph.org/releases/speex/speex-%{version}%{rc_ver}.tar.gz
Provides:   speex=%{version}-%{release}
BuildRequires:	libogg-devel

%description
Speex is a patent-free compression format designed especially for
speech. It is specialized for voice communications at low bit-rates in
the 2-45 kbps range. Possible applications include Voice over IP
(VoIP), Internet audio streaming, audio books, and archiving of speech
data (e.g. voice mail).

%package devel
Summary: 	Development package for %{name}
Group: 		Development/Libraries
Requires: 	%{name} = %{version}-%{release}
Requires: 	pkgconfig
Provides:   speex-devel=%{version}-%{release}

%description devel
Speex is a patent-free compression format designed especially for
speech. This package contains development files for %{name}

%package -n speex-tools
Summary:	The tools package for %{name}
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description -n speex-tools
Speex is a patent-free compression format designed especially for
speech. This package contains tools files and user's manual for %{name}.

%prep
%setup -q -n speex-%{version}%{rc_ver}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_docdir}/speex/manual.pdf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING TODO ChangeLog README NEWS
%{_libdir}/libspeex*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/manual.pdf
%{_includedir}/speex
%{_datadir}/aclocal/speex.m4
%{_libdir}/pkgconfig/speex*.pc
%{_libdir}/libspeex*.so

#%files -n speex-tools
#%defattr(-,root,root,-)
#%{_bindir}/speexenc
#%{_bindir}/speexdec
#%{_mandir}/man1/speexenc.1*
#%{_mandir}/man1/speexdec.1*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

