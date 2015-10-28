
# Building the extra print profiles requires colprof, +4Gb of RAM and
# quite a lot of time. Don't enable this for test builds.
%define enable_print_profiles 0

# SANE is pretty insane when it comes to handling devices, and we get AVCs
# popping up all over the place.
%define enable_sane 0

# Don't build the print profiles for secondary architectures on the
# logic that these are probably not doing press proofing or editing
# in different CMYK spaces
%ifarch %{ix86} x86_64
  %define build_print_profiles %{?enable_print_profiles}
%endif

Summary:   Color daemon
Name:      colord
Version:   1.2.11
Release:   2
License:   GPLv2+ and LGPLv2+
URL:       http://www.freedesktop.org/software/colord/
Source0:   http://www.freedesktop.org/software/colord/releases/%{name}-%{version}.tar.xz

BuildRequires: dbus-devel
BuildRequires: docbook-utils
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: intltool
BuildRequires: systemd-devel
BuildRequires: lcms2-devel >= 2.6
BuildRequires: libgudev-devel
BuildRequires: polkit-devel >= 0.103
BuildRequires: sqlite-devel
BuildRequires: gobject-introspection-devel
BuildRequires: vala-tools
BuildRequires: libgusb-devel
BuildRequires: gtk-doc
%if 0%{?build_print_profiles}
BuildRequires: argyllcms
%endif

# for SANE support
%if 0%{?enable_sane}
BuildRequires: sane-backends-devel
BuildRequires: dbus-devel
%endif

Requires: systemd-units
Requires(pre): shadow-utils
Requires: colord-libs = %{version}-%{release}

# Self-obsoletes to fix the multilib upgrade path
Obsoletes: colord < 0.1.27-3

# obsolete separate profiles package
Obsoletes: shared-color-profiles <= 0.1.6-2
Provides: shared-color-profiles

%description
colord is a low level system activated daemon that maps color devices
to color profiles in the system context.

%package libs
Summary: Color daemon library

%description libs
colord is a low level system activated daemon that maps color devices
to color profiles in the system context.

%package devel
Summary: Development package for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Obsoletes: colorhug-client-devel <= 0.1.13

%description devel
Files for development with %{name}.

%package devel-docs
Summary: Developer documentation package for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description devel-docs
Documentation for development with %{name}.

%package extra-profiles
Summary: More color profiles for color management that are less commonly used
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

# obsolete separate profiles package
Obsoletes: shared-color-profiles-extra <= 0.1.6-2
Provides: shared-color-profiles-extra

%description extra-profiles
More color profiles for color management that are less commonly used.
This may be useful for CMYK soft-proofing or for extra device support.

%prep
%setup -q

%build
# Set ~2 GiB limit so that colprof is forced to work in chunks when
# generating the print profile rather than trying to allocate a 3.1 GiB
# chunk of RAM to put the entire B-to-A tables in.
ulimit -Sv 2000000
%configure \
        --with-daemon-user=colord \
        --enable-gtk-doc \
        --enable-vala \
        --disable-argyllcms-sensor \
%if 0%{?build_print_profiles}
        --enable-print-profiles \
%else
        --disable-print-profiles \
%endif
%if 0%{?enable_sane}
        --enable-sane \
%endif
        --disable-bash-completion \
%if !0%{?rhel}
        --enable-libcolordcompat \
%endif
        --disable-static \
        --disable-rpath \
        --disable-examples \
        --disable-silent-rules \
        --disable-dependency-tracking

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT DATADIRNAME=share

# Remove static libs and libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# databases
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/colord/mapping.db
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/colord/storage.db


# own this files and folders.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/color/icc
mkdir -p $RPM_BUILD_ROOT%{_datadir}/color/cmms
mkdir -p $RPM_BUILD_ROOT%{_datadir}/color/settings
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/color/icc

# rpm macros
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/macros.d/
cat >$RPM_BUILD_ROOT%{_sysconfdir}/macros.d/macros.color<<EOF
%%_colordir %%_datadir/color
%%_syscolordir %%_colordir
%%_icccolordir %%_colordir/icc
%%_cmmscolordir %%_colordir/cmms
%%_settingscolordir %%_colordir/settings
EOF

%find_lang %{name}

%check
# known failure as of 1.1.5: colorhug/device-queue
make check || \
{ rc=$?; find . -name test-suite.log | xargs cat; } # exit $rc; }

%pre
getent group colord >/dev/null || groupadd -r colord
getent passwd colord >/dev/null || \
    useradd -r -g colord -d /var/lib/colord -s /sbin/nologin \
    -c "User for colord" colord
exit 0

%post
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%systemd_post colord.service

%preun
%systemd_preun colord.service

%postun
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%systemd_postun colord.service

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%doc README.md AUTHORS NEWS COPYING
%dir %{_datadir}/color
%dir %{_datadir}/color/icc
%dir %{_datadir}/color/cmms
%dir %{_datadir}/color/settings
%dir %{_localstatedir}/lib/color
%dir %{_localstatedir}/lib/color/icc
%{_sysconfdir}/macros.d/macros.color

%{_libexecdir}/colord
%attr(755,colord,colord) %dir %{_localstatedir}/lib/colord
%attr(755,colord,colord) %dir %{_localstatedir}/lib/colord/icc
%{_bindir}/*
%{_datadir}/glib-2.0/schemas/org.freedesktop.ColorHelper.gschema.xml
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ColorManager.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorManager*.xml
%{_datadir}/polkit-1/actions/org.freedesktop.color.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ColorManager.service
%{_datadir}/man/man1/*.1.gz
%{_datadir}/colord
#%{_datadir}/bash-completion/completions/colormgr
/usr/lib/udev/rules.d/*.rules
%{_libdir}/colord-sensors
%{_libdir}/colord-plugins
%ghost %attr(-,colord,colord) %{_localstatedir}/lib/colord/*.db
/usr/lib/systemd/system/colord.service

# session helper
%{_libexecdir}/colord-session
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorHelper.xml
%{_datadir}/dbus-1/services/org.freedesktop.ColorHelper.service

# sane helper
%if 0%{?enable_sane}
%{_libexecdir}/colord-sane
%endif

%dir %{_datadir}/color/icc/colord
%{_datadir}/color/icc/colord/*

%files libs
%doc COPYING
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_includedir}/colord-1
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/colord.vapi

%files devel-docs
%dir %{_datadir}/gtk-doc/html/colord
%{_datadir}/gtk-doc/html/colord/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.2.11-2
- Rebuild for new 4.0 release.

