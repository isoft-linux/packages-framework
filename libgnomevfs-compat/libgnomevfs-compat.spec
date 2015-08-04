#gnome-vfs is a very old vfs implementation of gnome.
#almost all software of gnome dropes dependency on gnome-vfs
#but binary release of libreoffice includes gnome-integration package still need gnome-vfs
#here provide a compatible package to provide libgnomevfs runtime.
#and ONLY a compatible runtime, all gnome-vfs features will NOT work.
#we did NOT and will NOT ship full old gnome-vfs.
#by cjacker.

Summary: The GNOME virtual file-system libraries
Name: 	libgnomevfs-compat
Version: 2.24.4
Release: 19%{?dist}
License: LGPLv2+ and GPLv2+
Source0: http://download.gnome.org/sources/gnome-vfs/2.24/gnome-vfs-%{version}.tar.bz2
URL: http://www.gnome.org/
BuildRequires: GConf2-devel 
BuildRequires: libxml2-devel, zlib-devel
BuildRequires: glib2-devel 
BuildRequires: popt, bzip2-devel, openjade
BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: libtool
BuildRequires: intltool
BuildRequires: autoconf
BuildRequires: gtk-doc 
BuildRequires: perl-XML-Parser 
BuildRequires: pkgconfig(avahi-client) pkgconfig(avahi-glib)
BuildRequires: dbus-devel 
BuildRequires: dbus-glib-devel 
BuildRequires: gettext

Patch3: gnome-vfs-2.9.90-modules-conf.patch

# remove gnome-mime-data dependency
Patch4: gnome-vfs-2.24.1-disable-gnome-mime-data.patch

# CVE-2009-2473 neon, gnome-vfs2 embedded neon: billion laughs DoS attack
Patch5: gnome-vfs-2.24.3-CVE-2009-2473.patch

# send to upstream
Patch101:	gnome-vfs-2.8.2-schema_about_for_upstream.patch

# Default
Patch104:	gnome-vfs-2.8.2-browser_default.patch

Patch6: gnome-vfs-2.15.91-mailto-command.patch

Patch300: gnome-vfs-2.20.0-ignore-certain-mountpoints.patch


# gnome-vfs-daemon exits on dbus, and constantly restarted causing dbus/hal to hog CPU
Patch404: gnome-vfs-2.24.xx-utf8-mounts.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=435653
Patch405: 0001-Add-default-media-application-schema.patch

# from upstream
Patch7: gnome-vfs-2.24.5-file-method-chmod-flags.patch

# fix compilation against new glib2
Patch8: gnome-vfs-2.24.4-enable-deprecated.patch


%description
GNOME VFS is the GNOME virtual file system. It is the foundation of
the Nautilus file manager. It provides a modular architecture and
ships with several modules that implement support for file systems,
http, ftp, and others. It provides a URI-based API, backend
supporting asynchronous file operations, a MIME type manipulation
library, and other features.

%prep
%setup -q -n gnome-vfs-%{version} 

%patch3 -p1 -b .modules-conf
%patch4 -p1 -b .mime-data
%patch5 -p1 -b .CVE-2009-2473

%patch6 -p1 -b .mailto-command
%patch7 -p1 -b .file-method-chmod-flags
%patch8 -p1 -b .enable-deprecated

# send to upstream
%patch101 -p1 -b .schema_about

%patch104 -p1 -b .browser_default

%patch300 -p1 -b .ignore-certain-mount-points

%patch404 -p1 -b .utf8-mounts

%patch405 -p1 -b .default-media

# for patch 10 and 4
libtoolize --force  || :
aclocal  || :
autoheader  || :
automake --add-missing || :
autoconf  || :

%build
CFLAGS="%optflags -fno-strict-aliasing" \
%configure \
    --disable-samba \
    --disable-gtk-doc \
    --disable-hal \
    --disable-static
pushd libgnomevfs
make %{?_smp_mflags}
popd

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
pushd libgnomevfs
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
popd
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}/gnome-vfs*
rm -rf %{buildroot}%{_libdir}/lib*.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%{_libdir}/libgnomevfs-2.so.0*

%changelog
