%define glib2_version 2.25.0
%define dbus_version 1.0
%define hal_version 0.5.7
%define gcrypt_version 1.2.2
%define libtasn1_version 0.3.4

Summary: Framework for managing passwords and other secrets
Name: gnome-keyring
Version: 3.18.0
Release: 2
License: GPLv2+ and LGPLv2+
#VCS: git:git://git.gnome.org/gnome-keyring
Source: http://download.gnome.org/sources/gnome-keyring/2.32/gnome-keyring-%{version}.tar.xz
Patch0:   gnome-keyring-fix-header.patch

URL: http://www.gnome.org

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: libgcrypt-devel >= %{gcrypt_version}
BuildRequires: libtasn1-devel >= %{libtasn1_version}
BuildRequires: pam-devel
BuildRequires: autoconf, automake, libtool
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libtasn1-tools
BuildRequires: gtk-doc
BuildRequires: perl-XML-Parser
BuildRequires: gcr-devel

%description
The gnome-keyring session daemon manages passwords and other types of
secrets for the user, storing them encrypted with a main password.
Applications can use the gnome-keyring library to integrate with the keyring.

%package devel
Summary: Development files for gnome-keyring
License: LGPLv2+
Requires: %name = %{version}-%{release}
Requires: glib2-devel

%description devel
The gnome-keyring-devel package contains the libraries and
header files needed to develop applications that use gnome-keyring.

%package pam
Summary: Pam module for unlocking keyrings
License: LGPLv2+
Requires: %{name} = %{version}-%{release}
# for /lib/security
Requires: pam

%description pam
The gnome-keyring-pam package contains a pam module that can
automatically unlock the "login" keyring when the user logs in.


%prep
%setup -q -n gnome-keyring-%{version}
%patch0 -p1

# Enable daemon autostart in XFCE
for i in daemon/*.desktop.in.in; do
  sed -i -e 's/OnlyShowIn=GNOME;LXDE;/OnlyShowIn=GNOME;LXDE;XFCE;/g' $i;
done


%build
%configure --disable-gtk-doc \
           --with-pam-dir=%{_libdir}/security \
           --disable-acl-prompts \
           --enable-pam \
           --with-gtk=3.0

# avoid unneeded direct dependencies
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang gnome-keyring

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >/dev/null 2>&1 ||:
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas >/dev/null 2>&1 ||:


%files -f gnome-keyring.lang
%defattr(-, root, root)
%dir %{_libdir}/gnome-keyring
%{_libdir}/pkcs11/gnome-keyring-pkcs11.so
%{_libdir}/gnome-keyring/devel/*.so
# GPL
%{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_sysconfdir}/xdg/autostart/*
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/p11-kit/modules/gnome-keyring.module
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_mandir}/man1/gnome-keyring-3.1.gz
%{_mandir}/man1/gnome-keyring-daemon.1.gz
%{_mandir}/man1/gnome-keyring.1.gz

#%files devel
#%defattr(-, root, root)
#%{_libdir}/pkgconfig/*
#%{_includedir}/*

%files pam
%defattr(-, root, root)
%{_libdir}/security/*.so


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.18.0-2
- Rebuild for new 4.0 release.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 3.18.0

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.17.91

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

