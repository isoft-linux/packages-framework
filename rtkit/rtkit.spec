Name:             rtkit
Version:          0.11
Release:          11%{?dist}
Summary:          Realtime Policy and Watchdog Daemon
Group:            System Environment/Base
# The daemon itself is GPLv3+, the reference implementation for the client BSD
License:          GPLv3+ and BSD
URL:              http://git.0pointer.de/?p=rtkit.git
Requires:         dbus
Requires:         polkit
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    dbus-devel >= 1.2
BuildRequires:    libcap-devel
BuildRequires:    polkit-devel
BuildRequires:    autoconf automake libtool
Source0:          http://0pointer.de/public/%{name}-%{version}.tar.xz
Patch1:           rtkit-mq_getattr.patch
Patch2:           0001-SECURITY-Pass-uid-of-caller-to-polkit.patch
Patch3:           rtkit-controlgroup.patch

%description
RealtimeKit is a D-Bus system service that changes the
scheduling policy of user processes/threads to SCHED_RR (i.e. realtime
scheduling mode) on request. It is intended to be used as a secure
mechanism to allow real-time scheduling to be used by normal user
processes.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
autoreconf -fvi
%configure --with-systemdsystemunitdir=/usr/lib/systemd/system
make %{?_smp_mflags}
./rtkit-daemon --introspect > org.freedesktop.RealtimeKit1.xml

%install
make install DESTDIR=$RPM_BUILD_ROOT
install -D org.freedesktop.RealtimeKit1.xml $RPM_BUILD_ROOT/%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml

%pre
getent group rtkit >/dev/null 2>&1 || groupadd \
        -r \
        -g 172 \
        rtkit
getent passwd rtkit >/dev/null 2>&1 || useradd \
        -r -l \
        -u 172 \
        -g rtkit \
        -d /proc \
        -s /sbin/nologin \
        -c "RealtimeKit" \
        rtkit
:;

%post
%systemd_post rtkit-daemon.service
dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :

%preun
%systemd_preun rtkit-daemon.service

%postun
%systemd_postun

%files
%doc README GPL LICENSE rtkit.c rtkit.h
%attr(0755,root,root) %{_sbindir}/rtkitctl
%attr(0755,root,root) %{_libexecdir}/rtkit-daemon
%{_datadir}/dbus-1/system-services/org.freedesktop.RealtimeKit1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml
%{_datadir}/polkit-1/actions/org.freedesktop.RealtimeKit1.policy
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.RealtimeKit1.conf
%{_prefix}/lib/systemd/system/rtkit-daemon.service
%{_mandir}/man8/*

%changelog
