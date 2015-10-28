Name:           lirc
Version:        0.9.2a
%global         src_vers  %(echo %{version} | sed 's/_/-/g' )
Release:        3%{?dist}

Summary:        The Linux Infrared Remote Control package

                # lib/ciniparser* and lib/dictionary* are BSD, others GPLv2
License:        GPLv2 and BSD
URL:            http://www.lirc.org/
Source0:        http://downloads.sourceforge.net/lirc/%{name}-%{src_vers}.tar.gz
Source7:        99-remote-control-lirc.rules
                # Config only, cannot be upstreamed.
Patch1:         0001-Changing-effective-user-default.patch
Patch2:         0002-Use-puts-instead-of-printf-when-applicalble.patch

BuildRequires:  alsa-lib-devel
Buildrequires:  autoconf
BuildRequires:  automake
BuildRequires:  doxygen
BuildRequires:  kernel-headers
BuildRequires:  libtool
BuildRequires:  libusb-devel
BuildRequires:  libusb1-devel
BuildRequires:  libXt-devel
BuildRequires:  python3-devel
BuildRequires:  python3-PyYAML
BuildRequires:  systemd-devel

Requires:       %{name}-libs = %{version}-%{release}
Requires:       python3-PyYAML

Requires(pre):     shadow-utils
Requires(post):    systemd
Requires(postun):  systemd
Requires(preun):   systemd

%description
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.

Installing this package will install most of the LIRC sub-packages.
You might want to install lirc-core, possibly adding some other
packages to get a smaller installation.


%package        core
Summary:        LIRC core, always needed to run LIRC

%description    core
The LIRC core contains the lircd daemons, the devinput and
default driver and most of the applications.


%package        libs
Summary:        LIRC libraries
Requires:       lirc-core%{?_isa} = %{version}-%{release}

%description    libs
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.  This package includes shared libraries
that applications use to interface with LIRC.


%package        config
Summary:        LIRC Configuration Tools and Data
Requires:       lirc-core = %{version}-%{release}
BuildArch:      noarch

%description    config
The LIRC config package contains tools and data  to ease the
LIRC configuration process.


%package        devel
Summary:        Development files for LIRC
Requires:       lirc-libs%{?_isa} = %{version}-%{release}

%description    devel
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.  This package includes files for
developing applications that use LIRC.

%package        doc
Summary:        LIRC documentation
BuildArch:      noarch

%description    doc
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.  This package contains LIRC
documentation.


%package        disable-kernel-rc
Summary:        Disable kernel ir device handling in favor of lirc
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description  disable-kernel-rc
Udev rule which disables the kernel built-in handling of infrared devices
(i. e., rc* ones) by making lirc the only used protocol.


%package        tools-gui
Summary:        LIRC GUI tools
Requires:       lirc-core%{?_isa} = %{version}-%{release}
Requires:       xorg-x11-fonts-misc

%description   tools-gui
Some seldom used X11-based tools for debugging lirc configurations.


# Don't provide or require anything from _docdir, per policy.
%global __provides_exclude_from ^%{_docdir}/.*$
%global __requires_exclude_from ^%{_docdir}/.*$


%prep
%setup -qn %{name}-%{src_vers}

%patch1 -p1
%patch2 -p1
sed -i -e 's|/usr/local/etc/|/etc/|' contrib/irman2lirc


%build
autoreconf -fi

CFLAGS="%{optflags}" %configure --libdir=%{_libdir}
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

tar -C $RPM_BUILD_ROOT/%{_docdir}/lirc \
    -xzf $RPM_BUILD_ROOT/%{_docdir}/lirc/api-docs.tar.gz
rm -rf $RPM_BUILD_ROOT/%{_docdir}/lirc/api-docs.tar.gz

cd $RPM_BUILD_ROOT%{_datadir}/lirc/contrib
chmod 755 irman2lirc devinput.sh
chmod 755 lirc.debian lirc.redhat lircs lirc.suse*
cd $OLDPWD
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/lirc/plugins/*.la

install -pm 755 contrib/irman2lirc $RPM_BUILD_ROOT%{_bindir}
install -Dpm 644 doc/lirc.hwdb $RPM_BUILD_ROOT%{_datadir}/lirc/lirc.hwdb
install -Dpm 644 %{SOURCE7} \
    $RPM_BUILD_ROOT%{_udevrulesdir}/99-remote-control-lirc.rules

mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
echo "d /var/run/lirc  0755  root  root  10d" \
    > $RPM_BUILD_ROOT%{_tmpfilesdir}/lirc.conf

%pre
getent group lirc >/dev/null || groupadd -r lirc
getent passwd lirc >/dev/null || \
    useradd -r -g lirc -d /var/log/lirc -s /sbin/nologin \
        -c "LIRC daemon user, runs lircd." lirc
exit 0

%post
%systemd_post lircd.service lircmd.service
systemd-tmpfiles --create %{_tmpfilesdir}/lirc.conf
# Remove stale links after service name change lirc -> lircd:
find /etc/systemd -name lirc.service -xtype l -delete || :

%post libs -p /sbin/ldconfig

%preun
%systemd_preun lircd.service lircmd.service

%postun
%systemd_postun_with_restart lircd.service lircmd.servic

%files

%postun libs -p /sbin/ldconfig

%files tools-gui
%{_bindir}/xmode2
%{_bindir}/irxevent
%{_mandir}/man1/irxevent*
%{_mandir}/man1/xmode2*

%files config
%{_bindir}/irdb-get
%{_bindir}/lirc-config-tool
%{_bindir}/lirc-setup
%{_mandir}/man1/irdb-get*
%{_mandir}/man1/lirc-config-tool*
%{_mandir}/man1/lirc-setup*
%{_datadir}/lirc/configs/*
%{python3_sitelib}/lirc
%exclude %{_datadir}/lirc/configs/iguanaIR.conf
%exclude %{_datadir}/lirc/configs/irman.conf
%exclude %{_datadir}/lirc/configs/ftdi.conf
%exclude %{_datadir}/lirc/configs/audio.conf


%files core
%dir  /etc/lirc
/etc/lirc/lircd.conf.d
%config(noreplace) /etc/lirc/lirc*.conf
%{_tmpfilesdir}/lirc.conf
%{_unitdir}/lirc*
%{_bindir}/*ir*
%{_bindir}/*mode2
%exclude %{_bindir}/irdb-get
%exclude %{_bindir}/xmode2
%exclude %{_bindir}/irxevent
%exclude %{_bindir}/lirc-setup
%exclude %{_bindir}/lirc-config-tool
%{_sbindir}/lirc*
%{_libdir}/lirc/plugins
%{_datadir}/lirc/
%exclude %{_datadir}/lirc/configs/*
%{_mandir}/man1/*ir*.1*
%{_mandir}/man1/*mode2*.1*
%{_mandir}/man8/lirc*d.8*
%{_mandir}/man5/lircd.conf.*
%exclude %{_mandir}/man1/lirc-config-tool*
%exclude %{_mandir}/man1/irdb-get*
%exclude %{_mandir}/man1/lirc-setup*
%exclude %{_mandir}/man1/irxevent*
%exclude %{_mandir}/man1/xmode2*


%files libs
#doc COPYING
%{_libdir}/liblirc_client.so.*
%{_libdir}/liblirc_driver.so.*
%{_libdir}/liblirc.so.*

%files devel
%{_includedir}/lirc/
%{_includedir}/lirc_private.h
%{_includedir}/lirc_driver.h
%{_includedir}/lirc_client.h
%{_libdir}/liblirc_client.so
%{_libdir}/liblirc_driver.so
%{_libdir}/liblirc.so
%{_libdir}/pkgconfig/lirc-driver.pc
%{_libdir}/pkgconfig/lirc.pc

%files doc
%{_docdir}/lirc/


%files disable-kernel-rc
%{_udevrulesdir}/99-remote-control-lirc.rules


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.9.2a-3
- Rebuild for new 4.0 release.

