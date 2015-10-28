Summary: Library to access the contents of an iPod
Name: libgpod
Version: 0.8.3
Release: 2 
License: LGPLv2+
URL: http://www.gtkpod.org/libgpod.html
Source0: http://downloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.bz2
Patch50:  libgpod-0.8.2-pkgconfig_overlinking.patch

BuildRequires: automake libtool
BuildRequires: docbook-style-xsl
BuildRequires: glib2-devel
BuildRequires: gdk-pixbuf2-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libimobiledevice-devel
BuildRequires: libplist-devel
BuildRequires: libusbx-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt
BuildRequires: sg3_utils-devel
BuildRequires: sqlite-devel
Requires: udev

%description
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.


%package devel
Summary: Development files for the libgpod library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.

This package contains the files required to develop programs that will use
libgpod.


%package doc
Summary: API documentation for the libgpod library
License: GFDL
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description doc
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.

This package contains the API documentation.

%prep
%setup -q

%patch50 -p1 -b .pkgconfig_overlinking

#autoreconf -f

# remove execute perms on the python examples as they'll be installed in %%doc
chmod -x bindings/python/examples/*.py


%build
%configure --without-hal --enable-udev --with-temp-mount-dir=%{_localstatedir}/run/%{name}
make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install
%find_lang %{name}

# Setup tmpfiles.d config
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
echo "D /var/run/%{name} 0755 root root -" > \
    %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

rm -rf $RPM_BUILD_ROOT%{_libdir}/libgpod.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libgpod-sharp.pc


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README*
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_bindir}/*
%{_libdir}/*.so.*
%dir %{_localstatedir}/run/%{name}
/lib/udev/iphone-set-info
/lib/udev/ipod-set-info
/lib/udev/rules.d/*.rules
#%dir %{_libdir}/libgpod/

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/gpod-1.0/
%{_libdir}/pkgconfig/%{name}-1.0.pc
%{_libdir}/*.so


%files doc
%defattr(-, root, root, 0755)
%{_datadir}/gtk-doc


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.8.3-2
- Rebuild for new 4.0 release.

