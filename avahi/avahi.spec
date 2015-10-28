%global WITH_MONO 0
%global WITH_QT3 0

%global WITH_COMPAT_DNSSD 1
%global WITH_COMPAT_HOWL  1

Name:             avahi
Version:          0.6.32
Release:          2.rc.1
Summary:          Local network service discovery
License:          LGPLv2+
URL:              http://avahi.org
Requires:         dbus
Requires:         expat
Requires:         libdaemon >= 0.11
Requires(pre):    shadow-utils
Requires(pre):    coreutils
Requires(pre):    /usr/bin/getent
Requires(pre):    /usr/sbin/groupadd
Requires:         %{name}-libs = %{version}-%{release}
BuildRequires:    automake
BuildRequires:    libtool
BuildRequires:    dbus-devel >= 0.90
BuildRequires:    dbus-glib-devel >= 0.70
BuildRequires:    dbus-python
BuildRequires:    python-libxml2
BuildRequires:    libdaemon-devel >= 0.11
BuildRequires:    glib2-devel
BuildRequires:    libcap-devel
BuildRequires:    expat-devel
%if %{WITH_QT3}
BuildRequires:    qt3-devel
%endif
BuildRequires:    qt4-devel

BuildRequires: xmltoman
BuildRequires:    python-devel
BuildRequires:    python3-devel
BuildRequires:    gdbm-devel
BuildRequires:    pygtk2
BuildRequires:    intltool
BuildRequires:    perl-XML-Parser
%if %{WITH_MONO}
BuildRequires:    mono-devel >= 1.1.13
BuildRequires:    monodoc-devel
%endif
BuildRequires:    systemd
Requires:         systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Source0:          http://avahi.org/download/%{name}-%{version}-rc.tar.gz


Patch100:         avahi-0.6.30-mono-libdir.patch

%description
Avahi is a system which facilitates service discovery on
a local network -- this means that you can plug your laptop or
computer into a network and instantly be able to view other people who
you can chat with, find printers to print to or find files being
shared. This kind of technology is already found in MacOS X (branded
'Rendezvous', 'Bonjour' and sometimes 'ZeroConf') and is very
convenient.

%package tools
Summary:          Command line tools for mDNS browsing and publishing
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description tools
Command line tools that use avahi to browse and publish mDNS services.

%package ui-tools
Summary:          UI tools for mDNS browsing
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}
Requires:         %{name}-glib%{?_isa} = %{version}-%{release}
Requires:         %{name}-ui-gtk3%{?_isa} = %{version}-%{release}
Requires:         python-avahi = %{version}-%{release}
Requires:         vnc
Requires:         openssh-clients
Requires:         pygtk2
Requires:         pygtk2-libglade
Requires:         gdbm
Requires:         dbus-python

%description ui-tools
Graphical user interface tools that use Avahi to browse for mDNS services.

%package glib
Summary:          Glib libraries for avahi
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description glib
Libraries for easy use of avahi from glib applications.

%package glib-devel
Summary:          Libraries and header files for avahi glib development
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-glib = %{version}-%{release}
Requires:         glib2-devel

%description glib-devel
The avahi-devel package contains the header files and libraries
necessary for developing programs using avahi with glib.

%package gobject
Summary:          GObject wrapper library for Avahi
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-glib = %{version}-%{release}

%description gobject
This library contains a GObject wrapper for the Avahi API

%package gobject-devel
Summary:          Libraries and header files for Avahi GObject development
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-glib = %{version}-%{release}
Requires:         %{name}-glib-devel = %{version}-%{release}
Requires:         %{name}-gobject = %{version}-%{release}

%description gobject-devel
The avahi-gobject-devel package contains the header files and libraries
necessary for developing programs using avahi-gobject.

%package ui
Summary:          Gtk user interface library for Avahi (Gtk+ 2 version)
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}
Requires:         %{name}-glib%{?_isa} = %{version}-%{release}
Requires:         gtk2

%description ui
This library contains a Gtk 2.x widget for browsing services.

%package ui-gtk3
Summary:          Gtk user interface library for Avahi (Gtk+ 3 version)
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}
Requires:         %{name}-glib%{?_isa} = %{version}-%{release}
Requires:         gtk3

%description ui-gtk3
This library contains a Gtk 3.x widget for browsing services.

%package ui-devel
Summary:          Libraries and header files for Avahi UI development
Requires:         %{name}-devel%{?_isa} = %{version}-%{release}
Requires:         %{name}-ui%{?_isa} = %{version}-%{release}
Requires:         %{name}-ui-gtk3%{?_isa} = %{version}-%{release}
#Requires:         %{name}-glib-devel = %{version}-%{release}

%description ui-devel
The avahi-ui-devel package contains the header files and libraries
necessary for developing programs using avahi-ui.

%if %{WITH_QT3}
%package qt3
Summary:          Qt3 libraries for avahi
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description qt3
Libraries for easy use of avahi from Qt3 applications.

%package qt3-devel
Summary:          Libraries and header files for avahi Qt3 development
Requires:         %{name}-devel%{?_isa} = %{version}-%{release}
Requires:         %{name}-qt3%{?_isa} = %{version}-%{release}

%description qt3-devel
The avahi-qt3-devel package contains the header files and libraries
necessary for developing programs using avahi with Qt3.
%endif

%package qt4
Summary:          Qt4 libraries for avahi
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description qt4
Libraries for easy use of avahi from Qt4 applications.

%package qt4-devel
Summary:          Libraries and header files for avahi Qt4 development
Requires:         %{name}-devel%{?_isa} = %{version}-%{release}
Requires:         %{name}-qt4%{?_isa} = %{version}-%{release}

%description qt4-devel
Th avahi-qt4-devel package contains the header files and libraries
necessary for developing programs using avahi with Qt4.



%if %{WITH_MONO}
%package sharp
Summary:          Mono language bindings for avahi mono development
Requires:         mono-core >= 1.1.13
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description sharp
The avahi-sharp package contains the files needed to develop
mono programs that use avahi.

%package ui-sharp
Summary:          Mono language bindings for avahi-ui
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-ui = %{version}-%{release}
Requires:         %{name}-sharp = %{version}-%{release}
Requires:         mono-core >= 1.1.13
Requires:         gtk-sharp2
BuildRequires:    gtk-sharp2-devel

%description ui-sharp
The avahi-sharp package contains the files needed to run
Mono programs that use avahi-ui.

%package ui-sharp-devel
Summary:          Mono language bindings for developing with avahi-ui
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-ui-sharp = %{version}-%{release}

%description ui-sharp-devel
The avahi-sharp-ui-devel package contains the files needed to develop
Mono programs that use avahi-ui.
%endif

%package libs
Summary:          Libraries for avahi run-time use
Requires:         %{name} = %{version}-%{release}
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}

%description libs
The avahi-libs package contains the libraries needed
to run programs that use avahi.

%package devel
Summary:          Libraries and header files for avahi development
Requires:         %{name}-libs = %{version}-%{release}
Requires:         pkgconfig

%description devel
The avahi-devel package contains the header files and libraries
necessary for developing programs using avahi.

%if %{WITH_COMPAT_HOWL}
%package compat-howl
Summary:          Libraries for howl compatibility
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Obsoletes:        howl-libs
Provides:         howl-libs

%description compat-howl
Libraries that are compatible with those provided by the howl package.

%package compat-howl-devel
Summary:          Header files for development with the howl compatibility libraries
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-compat-howl = %{version}-%{release}
Obsoletes:        howl-devel
Provides:         howl-devel

%description compat-howl-devel
Header files for development with the howl compatibility libraries.
%endif

%if %{WITH_COMPAT_DNSSD}
%package compat-libdns_sd
Summary:          Libraries for Apple Bonjour mDNSResponder compatibility
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description compat-libdns_sd
Libraries for Apple Bonjour mDNSResponder compatibility.

%package compat-libdns_sd-devel
Summary:          Header files for the Apple Bonjour mDNSResponder compatibility libraries
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}
Requires:         %{name}-compat-libdns_sd = %{version}-%{release}

%description compat-libdns_sd-devel
Header files for development with the Apple Bonjour mDNSResponder compatibility
libraries.
%endif

%package autoipd
Summary:          Link-local IPv4 address automatic configuration daemon (IPv4LL)
Requires(pre):    shadow-utils
Conflicts:        %{name} < %{version}-%{release}
Conflicts:        %{name} > %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description autoipd
avahi-autoipd implements IPv4LL, "Dynamic Configuration of IPv4
Link-Local Addresses"  (IETF RFC3927), a protocol for automatic IP address
configuration from the link-local 169.254.0.0/16 range without the need for a
central server. It is primarily intended to be used in ad-hoc networks which
lack a DHCP server.

%package dnsconfd
Summary:          Configure local unicast DNS settings based on information published in mDNS
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}

%description dnsconfd
avahi-dnsconfd connects to a running avahi-daemon and runs the script
/etc/avahi/dnsconfd.action for each unicast DNS server that is announced on the
local LAN. This is useful for configuring unicast DNS servers in a DHCP-like
fashion with mDNS.


%package -n python-avahi
Summary:          Python2 Avahi bindings
Provides:         python2-avahi = %{version}-%{release}
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description -n python-avahi
%{summary}.

%package -n python3-avahi
Summary:          Python3 Avahi bindings
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description -n python3-avahi
%{summary}.

%prep
%setup -q -n %{name}-%{version}-rc

%patch100 -p1 -b .mono-libdir
rm -fv docs/INSTALL


%build
# patch100 requires autogen
rm -fv missing
NOCONFIGURE=1 ./autogen.sh

%configure \
        --with-distro=none \
        --disable-monodoc \
        --with-avahi-user=avahi \
        --with-avahi-group=avahi \
        --with-avahi-priv-access-group=avahi \
        --with-autoipd-user=avahi-autoipd \
        --with-autoipd-group=avahi-autoipd \
        --with-systemdsystemunitdir=/usr/lib/systemd/system \
%if ! %{WITH_QT3}
        --disable-qt3 \
%endif
        --enable-introspection \
%if %{WITH_COMPAT_DNSSD}
        --enable-compat-libdns_sd \
%endif
%if %{WITH_COMPAT_HOWL}
        --enable-compat-howl \
%endif
%if ! %{WITH_MONO}
        --disable-mono \
%endif
;
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install
find %{buildroot} \( -name '*.a' -o -name '*.la' \) -exec rm {} \;

# remove example
rm -f %{buildroot}%{_sysconfdir}/avahi/services/ssh.service
rm -f %{buildroot}%{_sysconfdir}/avahi/services/sftp-ssh.service

# create /var/run/avahi-daemon to ensure correct selinux policy for it:
mkdir -p %{buildroot}%{_localstatedir}/run/avahi-daemon
mkdir -p %{buildroot}%{_localstatedir}/lib/avahi-autoipd

# remove the documentation directory - let % doc handle it:
rm -rf %{buildroot}%{_datadir}/%{name}-%{version}

# Make /etc/avahi/etc/localtime owned by avahi:
mkdir -p %{buildroot}/etc/avahi/etc
touch %{buildroot}/etc/avahi/etc/localtime

# fix bug 197414 - add missing symlinks for avahi-compat-howl and avahi-compat-dns-sd
%if %{WITH_COMPAT_HOWL}
ln -s avahi-compat-howl.pc  %{buildroot}/%{_libdir}/pkgconfig/howl.pc
%endif
%if %{WITH_COMPAT_DNSSD}
ln -s avahi-compat-libdns_sd.pc %{buildroot}/%{_libdir}/pkgconfig/libdns_sd.pc
ln -s avahi-compat-libdns_sd/dns_sd.h %{buildroot}/%{_includedir}/
%endif

# Add python3 support
mkdir -p %{buildroot}%{python3_sitelib}/avahi/
cp -r %{buildroot}%{python2_sitelib}/avahi/* %{buildroot}%{python3_sitelib}/avahi/
rm -fv %{buildroot}%{buildroot}%{python3_sitelib}/avahi/*.py{c,o}

rm -f %{buildroot}%{_sysconfdir}/rc.d/init.d/avahi-daemon
rm -f %{buildroot}%{_sysconfdir}/rc.d/init.d/avahi-dnsconfd


# Hide Menu Items.
echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/avahi-discover.desktop
echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/bssh.desktop
echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/bvnc.desktop


%find_lang %{name}

%pre
/usr/bin/getent group avahi >/dev/null 2>&1 || /usr/sbin/groupadd \
        -r \
        -g 70 \
        avahi >/dev/null 2>&1 || :
/usr/bin/getent passwd avahi >/dev/null 2>&1 || /usr/sbin/useradd \
        -r -l \
        -u 70 \
        -g avahi \
        -d %{_localstatedir}/run/avahi-daemon \
        -s /sbin/nologin \
        -c "Avahi mDNS/DNS-SD Stack" \
        avahi >/dev/null 2>&1 || :

%post
/sbin/ldconfig >/dev/null 2>&1 || :
/usr/bin/dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :
if [ "$1" -eq 1 -a -s /etc/localtime ]; then
        /usr/bin/cp -cfp /etc/localtime /etc/avahi/etc/localtime >/dev/null 2>&1 || :
fi
%systemd_post avahi-daemon.socket avahi-daemon.service

%preun
%systemd_preun avahi-daemon.socket avahi-daemon.service

%postun
/sbin/ldconfig >/dev/null 2>&1 || :
%systemd_postun_with_restart avahi-daemon.socket avahi-daemon.service

%pre autoipd
/usr/bin/getent group avahi-autoipd >/dev/null 2>&1 || /usr/sbin/groupadd \
        -r \
        -g 170 \
        avahi-autoipd >/dev/null 2>&1 || :
/usr/bin/getent passwd avahi-autoipd >/dev/null 2>&1 || /usr/sbin/useradd \
        -r -l \
        -u 170 \
        -g avahi-autoipd \
        -d %{_localstatedir}/lib/avahi-autoipd \
        -s /sbin/nologin \
        -c "Avahi IPv4LL Stack" \
        avahi-autoipd >/dev/null 2>&1 || :
:;

%post dnsconfd
%systemd_post avahi-dnsconfd.service

%preun dnsconfd
%systemd_preun avahi-dnsconfd.service

%postun dnsconfd
%systemd_postun_with_restart avahi-dnsconfd.service

%post glib -p /sbin/ldconfig
%postun glib -p /sbin/ldconfig

%post compat-howl -p /sbin/ldconfig
%postun compat-howl -p /sbin/ldconfig

%post compat-libdns_sd -p /sbin/ldconfig
%postun compat-libdns_sd -p /sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post gobject -p /sbin/ldconfig
%postun gobject -p /sbin/ldconfig

%if %{WITH_QT3}
%post qt3 -p /sbin/ldconfig
%postun qt3 -p /sbin/ldconfig
%endif

%post qt4 -p /sbin/ldconfig
%postun qt4 -p /sbin/ldconfig

%post ui -p /sbin/ldconfig
%postun ui -p /sbin/ldconfig

%post ui-gtk3 -p /sbin/ldconfig
%postun ui-gtk3 -p /sbin/ldconfig


%files -f %{name}.lang
%doc docs/* avahi-daemon/example.service avahi-daemon/sftp-ssh.service avahi-daemon/ssh.service
%dir %{_sysconfdir}/avahi
%dir %{_sysconfdir}/avahi/etc
%ghost %{_sysconfdir}/avahi/etc/localtime
%config(noreplace) %{_sysconfdir}/avahi/hosts
%dir %{_sysconfdir}/avahi/services
%ghost %dir %{_localstatedir}/run/avahi-daemon
%config(noreplace) %{_sysconfdir}/avahi/avahi-daemon.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/avahi-dbus.conf
%{_sbindir}/avahi-daemon
%dir %{_datadir}/avahi
%{_datadir}/avahi/*.dtd
%{_datadir}/avahi/service-types
%dir %{_libdir}/avahi
%{_libdir}/avahi/service-types.db

%{_mandir}/man5/*
%{_mandir}/man8/avahi-daemon.*
%{_unitdir}/avahi-daemon.service
%{_unitdir}/avahi-daemon.socket
%{_datadir}/dbus-1/system-services/org.freedesktop.Avahi.service
%{_libdir}/libavahi-core.so.*

%files autoipd
%{_sbindir}/avahi-autoipd
%config(noreplace) %{_sysconfdir}/avahi/avahi-autoipd.action
%{_mandir}/man8/avahi-autoipd.*

%files dnsconfd
%config(noreplace) %{_sysconfdir}/avahi/avahi-dnsconfd.action
%{_sbindir}/avahi-dnsconfd
%{_mandir}/man8/avahi-dnsconfd.*
%{_unitdir}/avahi-dnsconfd.service

%files tools
%{_bindir}/*
%{_mandir}/man1/*
%exclude %{_bindir}/b*
%exclude %{_bindir}/avahi-discover*
%exclude %{_bindir}/avahi-bookmarks
%exclude %{_mandir}/man1/b*
%exclude %{_mandir}/man1/avahi-discover*
%exclude %{_mandir}/man1/avahi-bookmarks*


%files ui-tools
%{_bindir}/b*
%{_bindir}/avahi-discover
# avahi-bookmarks is not really a UI tool, but I won't create a seperate package for it...
%{_bindir}/avahi-bookmarks
%{_mandir}/man1/b*
%{_mandir}/man1/avahi-discover*
%{_mandir}/man1/avahi-bookmarks*
%{_datadir}/applications/b*.desktop
%{_datadir}/applications/avahi-discover.desktop
%{_datadir}/avahi/interfaces/
%{python2_sitelib}/avahi_discover/

%files devel
%{_libdir}/libavahi-common.so
%{_libdir}/libavahi-core.so
%{_libdir}/libavahi-client.so
%{_includedir}/avahi-client
%{_includedir}/avahi-common
%{_includedir}/avahi-core
%{_datadir}/dbus-1/interfaces/*.xml
%{_libdir}/pkgconfig/avahi-core.pc
%{_libdir}/pkgconfig/avahi-client.pc

%files libs
%{_libdir}/libavahi-common.so.*
%{_libdir}/libavahi-client.so.*

%files glib
%{_libdir}/libavahi-glib.so.*

%files glib-devel
%{_libdir}/libavahi-glib.so
%{_includedir}/avahi-glib
%{_libdir}/pkgconfig/avahi-glib.pc

%files gobject
%{_libdir}/libavahi-gobject.so.*
%{_libdir}/girepository-1.0/Avahi-0.6.typelib
%{_libdir}/girepository-1.0/AvahiCore-0.6.typelib

%files gobject-devel
%{_libdir}/libavahi-gobject.so
%{_includedir}/avahi-gobject
%{_libdir}/pkgconfig/avahi-gobject.pc
%{_datadir}/gir-1.0/Avahi-0.6.gir
%{_datadir}/gir-1.0/AvahiCore-0.6.gir

%files ui
%{_libdir}/libavahi-ui.so.*

%files ui-gtk3
%{_libdir}/libavahi-ui-gtk3.so.*

%files ui-devel
%{_libdir}/libavahi-ui.so
%{_libdir}/libavahi-ui-gtk3.so
%{_includedir}/avahi-ui
%{_libdir}/pkgconfig/avahi-ui.pc
%{_libdir}/pkgconfig/avahi-ui-gtk3.pc

%if %{WITH_QT3}
%files qt3
%{_libdir}/libavahi-qt3.so.*

%files qt3-devel
%{_libdir}/libavahi-qt3.so
%{_includedir}/avahi-qt3/
%{_libdir}/pkgconfig/avahi-qt3.pc
%endif

%files qt4
%{_libdir}/libavahi-qt4.so.*

%files qt4-devel
%{_libdir}/libavahi-qt4.so
%{_includedir}/avahi-qt4/
%{_libdir}/pkgconfig/avahi-qt4.pc


%if %{WITH_MONO}
%files sharp
%{_prefix}/lib/mono/avahi-sharp
%{_prefix}/lib/mono/gac/avahi-sharp
%{_libdir}/pkgconfig/avahi-sharp.pc

%files ui-sharp
%{_prefix}/lib/mono/avahi-ui-sharp
%{_prefix}/lib/mono/gac/avahi-ui-sharp

%files ui-sharp-devel
%{_libdir}/pkgconfig/avahi-ui-sharp.pc
%endif

%if %{WITH_COMPAT_HOWL}
%files compat-howl
%{_libdir}/libhowl.so.*

%files compat-howl-devel
%{_libdir}/libhowl.so
%{_includedir}/avahi-compat-howl
%{_libdir}/pkgconfig/avahi-compat-howl.pc
%{_libdir}/pkgconfig/howl.pc
%endif

%if %{WITH_COMPAT_DNSSD}
%files compat-libdns_sd
%{_libdir}/libdns_sd.so.*

%files compat-libdns_sd-devel
%{_libdir}/libdns_sd.so
%{_includedir}/avahi-compat-libdns_sd
%{_includedir}/dns_sd.h
%{_libdir}/pkgconfig/avahi-compat-libdns_sd.pc
%{_libdir}/pkgconfig/libdns_sd.pc
%endif

%files -n python-avahi
# These are .py files only, so they don't go in lib64
%{python2_sitelib}/avahi/

%files -n python3-avahi
# These are .py files only, so they don't go in lib64
%{python3_sitelib}/avahi/

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.6.32-2.rc.1
- Rebuild for new 4.0 release.

* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- update to 0.6.32-rc
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

