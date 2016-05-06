Name:		phodav
Version:	2.0
Release:	4
Summary:	phodav is a WebDav server implementation using libsoup (RFC 4918). 

License:	GPL
URL:		https://wiki.gnome.org/phodav
Source0:	http://ftp.gnome.org/pub/GNOME/sources/phodav/2.0/phodav-2.0.tar.xz

Patch0:  put_forbidden_when_readonly.patch

BuildRequires:  systemd-devel
BuildRequires:  systemd-units
BuildRequires:  libsoup-devel
BuildRequires:  avahi-gobject-devel
BuildRequires:  intltool
BuildRequires:  asciidoc
BuildRequires:  xmlto

Requires:	libsoup
Requires:   lib%{name} = %{version}-%{release}

%description
%{summary}

%package -n libphodav 
Summary:        Libraries for %{name}

%description -n libphodav
%{summary}

%package -n libphodav-devel 
Summary:        Development files for lib%{name}
Requires:       lib%{name} = %{version}-%{release}

%description -n libphodav-devel
The lib%{name}-devel package contains libraries and header files for
developing applications that use lib%{name}.

%package -n spice-webdavd
Summary: Spice webdavd

%description -n spice-webdavd
Spice webdavd

%prep
%setup -q
%patch0 -p1

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%find_lang phodav

%files -f phodav.lang
%{_bindir}/chezdav
%{_mandir}/man1/chezdav.1.gz

%files -n libphodav
%{_libdir}/libphodav-*.so.*

%files -n libphodav-devel
%{_includedir}/libphodav-2.0
%{_libdir}/libphodav-*.so
%{_libdir}/pkgconfig/libphodav-*.pc
%{_datadir}/gtk-doc/html/phodav


%files -n spice-webdavd
%{_sbindir}/spice-webdavd
%{_libdir}/systemd/system/spice-webdavd.service
%{_libdir}/udev/rules.d/70-spice-webdavd.rules

%changelog
* Fri May 06 2016 WangMing <ming.wang@i-soft.com.cn> - 2.0-3
- Make Put operation forbidden when readonly.

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.0-2
- Rebuild for new 4.0 release.


