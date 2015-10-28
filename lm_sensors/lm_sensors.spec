Name: lm_sensors
Version: 3.3.5
Release: 7%{?dist}
Summary: Hardware monitoring tools
License: LGPLv2+ and GPLv3+ and GPLv2+ and Verbatim and Public Domain

URL: http://www.lm-sensors.org/

Source: http://dl.lm-sensors.org/lm-sensors/releases/%{name}-%{version}.tar.bz2
Source1: lm_sensors.sysconfig
# these 2 were taken from PLD-linux, Thanks!
Source2: sensord.sysconfig
Source3: lm_sensors-modprobe-wrapper
Source4: lm_sensors-modprobe-r-wrapper
Source5: sensord.service
Source6: sensord-service-wrapper
Source7: lm_sensors.service

Requires: /usr/sbin/modprobe
%ifarch %{ix86} x86_64
Requires: /usr/sbin/dmidecode
%endif
Requires(post): systemd-units
BuildRequires: kernel-headers >= 2.2.16, bison, libsysfs-devel, flex, gawk
BuildRequires: rrdtool-devel


%description
The lm_sensors package includes a collection of modules for general SMBus
access and hardware monitoring.


%package libs
Summary: Lm_sensors core libraries

%description libs
Core libraries for lm_sensors applications


%package devel
Summary: Development files for programs which will use lm_sensors
Requires: %{name}-libs = %{version}-%{release}

%description devel
The lm_sensors-devel package includes a header files and libraries for use
when building applications that make use of sensor data.


%package sensord
Summary: Daemon that periodically logs sensor readings
Requires: %{name} = %{version}-%{release}

%description sensord
Daemon that periodically logs sensor readings to syslog or a round-robin
database, and warns of sensor alarms.


%prep
%setup -q

mv prog/init/README prog/init/README.initscripts
chmod -x prog/init/fancontrol.init

# fixing the sensord-service-wrapper path
cp -p %{SOURCE5} sensord.service
cp -p %{SOURCE7} lm_sensors.service
sed -i "s|\@WRAPPER_DIR\@|%{_libexecdir}/%{name}|" sensord.service
sed -i "s|\@WRAPPER_DIR\@|%{_libexecdir}/%{name}|" lm_sensors.service


%build
export CFLAGS="%{optflags}"
make PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir} EXLDFLAGS= \
  PROG_EXTRA=sensord user


%install
make PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir} PROG_EXTRA=sensord \
  DESTDIR=$RPM_BUILD_ROOT user_install
rm $RPM_BUILD_ROOT%{_libdir}/libsensors.a

ln -s sensors.conf.5.gz $RPM_BUILD_ROOT%{_mandir}/man5/sensors3.conf.5.gz

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sensors.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/lm_sensors
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sensord

# service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -pm 644 prog/init/fancontrol.service $RPM_BUILD_ROOT%{_unitdir}
install -pm 644 lm_sensors.service           $RPM_BUILD_ROOT%{_unitdir}
install -pm 644 sensord.service              $RPM_BUILD_ROOT%{_unitdir}

# customized modprobe calls
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}
install -pm 755 %{SOURCE3} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lm_sensors-modprobe-wrapper
install -pm 755 %{SOURCE4} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lm_sensors-modprobe-r-wrapper

# sensord service wrapper
install -pm 755 %{SOURCE6} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/sensord-service-wrapper


# Note non standard systemd scriptlets, since reload / stop makes no sense
# for lm_sensors
%triggerun -- lm_sensors < 3.3.0-2
if [ -L /etc/rc3.d/S26lm_sensors ]; then
    /bin/systemctl enable lm_sensors.service >/dev/null 2>&1 || :
fi
/sbin/chkconfig --del lm_sensors

# ===== main =====

%post
%systemd_post lm_sensors.service

%preun
%systemd_preun lm_sensors.service

%postun
%systemd_postun_with_restart lm_sensors.service

# ==== sensord ===

%post sensord
%systemd_post sensord.service

%preun sensord
%systemd_preun sensord.service

%postun sensord
%systemd_postun_with_restart sensord.service

# ===== libs =====

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%doc CHANGES CONTRIBUTORS COPYING doc README*
%doc prog/init/fancontrol.init prog/init/README.initscripts
%config(noreplace) %{_sysconfdir}/sensors3.conf
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sbindir}/*
%{_unitdir}/lm_sensors.service
%{_unitdir}/fancontrol.service
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/lm_sensors-modprobe*wrapper
%config(noreplace) %{_sysconfdir}/sysconfig/lm_sensors
%exclude %{_sbindir}/sensord
%exclude %{_mandir}/man8/sensord.8.gz

%files libs
%{_libdir}/*.so.*

%files devel
%{_includedir}/sensors
%{_libdir}/lib*.so
%{_mandir}/man3/*

%files sensord
%doc prog/sensord/README
%{_sbindir}/sensord
%{_mandir}/man8/sensord.8.gz
%config(noreplace) %{_sysconfdir}/sysconfig/sensord
%{_unitdir}/sensord.service
%{_libexecdir}/%{name}/sensord-service-wrapper


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.3.5-7
- Rebuild for new 4.0 release.

