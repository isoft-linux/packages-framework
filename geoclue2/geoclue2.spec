Name:           geoclue2
Version:        2.4.3
Release:        2
Summary:        Geolocation service

License:        GPLv2+
URL:            http://www.freedesktop.org/wiki/Software/GeoClue/
Source0:        http://www.freedesktop.org/software/geoclue/releases/2.2/geoclue-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  json-glib-devel
BuildRequires:  libsoup-devel
BuildRequires:  ModemManager-devel
BuildRequires:  systemd
BuildRequires:  pkgconfig(avahi-client)
BuildRequires:  pkgconfig(avahi-glib)
Requires(pre):  shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:       dbus

Obsoletes:      geoclue2-server < 2.1.8

%description
Geoclue is a D-Bus service that provides location information. The primary goal
of the Geoclue project is to make creating location-aware applications as
simple as possible, while the secondary goal is to ensure that no application
can access location information without explicit permission from user.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains files for developing applications that
use %{name}.

%package        demos
Summary:        Demo applications for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libnotify
BuildRequires:  libnotify-devel

%description    demos
The %{name}-demos package contains demo applications that use %{name}.


%prep
%setup -q -n geoclue-%{version}

#Here we use keys of archlinux.

# Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
# Note: These are for Arch Linux use ONLY. For your own distribution, please
# get your own set of keys. Feel free to contact foutrelis@archlinux.org for
# more information.
_google_api_key=AIzaSyDwr302FpOSkGRpLlUpPThNTDPbXcIn_FM

# Mozilla API keys (see https://location.services.mozilla.com/api)
# Note: These are for Arch Linux use ONLY. For your own distribution, please
# get your own set of keys. Feel free to contact heftig@archlinux.org for
# more information.
_mozilla_api_key=16674381-f021-49de-8622-3021c5942aff

sed -e "s/key=geoclue/key=$_mozilla_api_key/" \
      -e "s/key=YOUR_KEY/key=$_google_api_key/" \
      -i data/geoclue.conf.in


%build
%configure --with-dbus-service-user=geoclue --enable-demo-agent
make %{?_smp_mflags} V=1


%install
%make_install

# Home directory for the 'geoclue' user
mkdir -p $RPM_BUILD_ROOT/var/lib/geoclue


%pre
# Update the home directory for existing users
getent passwd geoclue >/dev/null && \
    usermod -d /var/lib/geoclue geoclue &>/dev/null
# Create a new user and group if they don't exist
getent group geoclue >/dev/null || groupadd -r geoclue
getent passwd geoclue >/dev/null || \
    useradd -r -g geoclue -d /var/lib/geoclue -s /sbin/nologin \
    -c "User for geoclue" geoclue
exit 0

%post
%systemd_post geoclue.service

%preun
%systemd_preun geoclue.service

%postun
%systemd_postun_with_restart geoclue.service


%files
%doc COPYING NEWS
%config %{_sysconfdir}/geoclue/
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf
%{_libexecdir}/geoclue
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service
%{_unitdir}/geoclue.service
%attr(755,geoclue,geoclue) %dir /var/lib/geoclue

%files devel
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2*.xml
%{_libdir}/pkgconfig/geoclue-2.0.pc
%{_libdir}/pkgconfig/libgeoclue-2.0.pc
%{_includedir}/libgeoclue-2.0/gclue-client.h
%{_includedir}/libgeoclue-2.0/gclue-enum-types.h
%{_includedir}/libgeoclue-2.0/gclue-enums.h
%{_includedir}/libgeoclue-2.0/gclue-helpers.h
%{_includedir}/libgeoclue-2.0/gclue-location.h
%{_includedir}/libgeoclue-2.0/gclue-manager.h
%{_includedir}/libgeoclue-2.0/gclue-simple.h
%{_includedir}/libgeoclue-2.0/geoclue.h
%{_libdir}/libgeoclue-2.so
%{_libdir}/libgeoclue-2.so.0
%{_libdir}/libgeoclue-2.so.0.0.0

%files demos
%{_libexecdir}/geoclue-2.0/demos/where-am-i
%{_libexecdir}/geoclue-2.0/demos/agent
%{_datadir}/applications/geoclue-demo-agent.desktop
%{_datadir}/applications/geoclue-where-am-i.desktop

%changelog
* Mon Jul 11 2016 zhouyang <yang.zhou@i-soft.com.cn> - 2.4.3-2
- Update

* Mon Jul 11 2016 zhouyang <yang.zhou@i-soft.com.cn> - 2.4.3-1
- Update

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.2.0-3
- Rebuild for new 4.0 release.

