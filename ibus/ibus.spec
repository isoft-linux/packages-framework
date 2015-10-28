%global ibus_api_version 1.0
%global ibus_xkb_version 1.5.0.20140114

Name:           ibus
Version:        1.5.10
Release:        3 
Summary:        Intelligent Input Bus for Linux OS
License:        LGPLv2+
URL:            http://code.google.com/p/ibus/
Source0:        https://github.com/ibus/ibus/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-xinput
Source2:        %{name}.conf.5
Patch0:         %{name}-HEAD.patch


BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  dbus-python-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk-doc
BuildRequires:  dconf-devel
BuildRequires:  dbus-x11
BuildRequires:  python-devel
BuildRequires:  vala
BuildRequires:  vala-devel
BuildRequires:  vala-tools
# for AM_GCONF_SOURCE_2 in configure.ac
BuildRequires:  GConf2-devel
BuildRequires:  intltool
BuildRequires:  iso-codes-devel
BuildRequires:  libnotify-devel
BuildRequires:  libwayland-client-devel

Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}
Requires:       %{name}-gtk2%{?_isa}   = %{version}-%{release}
Requires:       %{name}-gtk3%{?_isa}   = %{version}-%{release}
Requires:       %{name}-setup          = %{version}-%{release}
Requires:       %{name}-wayland%{?_isa} = %{version}-%{release}

Requires:       iso-codes
Requires:       dbus-python
Requires:       dbus-x11
Requires:       dconf
Requires:       librsvg2
# Owner of %%{_sysconfdir}/X11/xinit
Requires:       xorg-x11-xinit
# for setxkbmap
Requires:       xorg-x11-xkb-utils

Requires(post):  desktop-file-utils
Requires(postun):  desktop-file-utils
Requires(postun):  dconf
Requires(posttrans): dconf

Requires(post):  %{_sbindir}/alternatives
Requires(postun):  %{_sbindir}/alternatives

%global _xinputconf %{_sysconfdir}/X11/xinit/xinput.d/ibus.conf

%description
IBus means Intelligent Input Bus. It is an input framework for Linux OS.

%package libs
Summary:        IBus libraries

Requires:       dbus >= 1.2.4
Requires:       glib2 >= %{glib_ver}
# Owner of %%{_libdir}/girepository-1.0
Requires:       gobject-introspection

%description libs
This package contains the libraries for IBus

%package gtk2
Summary:        IBus im module for gtk2
Requires:       %{name}%{?_isa}        = %{version}-%{release}
Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}
Requires(post): glib2 >= %{glib_ver}
# Added for upgrade el6 to el7
Provides:       ibus-gtk = %{version}-%{release}
Obsoletes:      ibus-gtk < %{version}-%{release}

%description gtk2
This package contains ibus im module for gtk2

%package gtk3
Summary:        IBus im module for gtk3
Requires:       %{name}%{?_isa}        = %{version}-%{release}
Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}
Requires(post): glib2 >= %{glib_ver}

%description gtk3
This package contains ibus im module for gtk3

%package setup
Summary:        IBus setup utility
Requires:       %{name} = %{version}-%{release}
BuildRequires:  gobject-introspection-devel
BuildRequires:  pygobject3-devel
BuildArch:      noarch

%description setup
This is a setup utility for IBus.

%package pygtk2
Summary:        IBus pygtk2 library
Requires:       %{name} = %{version}-%{release}
Requires:       pygtk2
BuildArch:      noarch

%description pygtk2
This is a pygtk2 library for IBus. Now major IBus engines use pygobject3
and this package will be deprecated.

%package wayland
Summary:        IBus im module for Wayland
Requires:       %{name}%{?_isa}        = %{version}-%{release}
Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}

%description wayland
This package contains IBus im module for Wayland

%package devel
Summary:        Development tools for ibus
Requires:       %{name}%{?_isa}        = %{version}-%{release}
Requires:       %{name}-libs%{?_isa}   = %{version}-%{release}
Requires:       dbus-devel
Requires:       glib2-devel
Requires:       gobject-introspection-devel
Requires:       vala

%description devel
The ibus-devel package contains the header files for ibus.

%package devel-docs
Summary:        Developer documents for IBus
Requires:       %{name}                = %{version}-%{release}
BuildArch:      noarch

%description devel-docs
The ibus-devel-docs package contains developer documentation for IBus


%prep
%setup -q
%patch0 -p1

%build
./autogen.sh
%configure \
    --disable-static \
    --enable-gtk2 \
    --enable-gtk3 \
    --enable-xim \
    --disable-gtk-doc \
    --with-no-snooper-apps='gnome-do,Do.*,firefox.*,.*chrome.*,.*chromium.*' \
    --enable-surrounding-text \
    --with-python=/usr/bin/python \
    --disable-python-library \
    --enable-wayland \
    --enable-introspection

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

# install man page
for S in %{SOURCE2}
do
  cp $S .
  MP=`basename $S` 
  gzip $MP
  install -pm 644 -D ${MP}.gz $RPM_BUILD_ROOT%{_datadir}/man/man5/${MP}.gz
done

# install xinput config file
install -pm 644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_xinputconf}

# install .desktop files
echo "NoDisplay=true" >> $RPM_BUILD_ROOT%{_datadir}/applications/ibus-setup.desktop

desktop-file-install --delete-original          \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

# FIXME: no version number
%find_lang %{name}10


%post
# recreate icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ "$1" -eq 0 ]; then
  # recreate icon cache
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
  # 'dconf update' sometimes does not update the db...
  dconf update || :
  [ -f %{_sysconfdir}/dconf/db/ibus ] && \
      rm %{_sysconfdir}/dconf/db/ibus || :
  # 'ibus write-cache --system' updates the system cache.
  [ -f /var/cache/ibus/bus/registry ] && \
      rm /var/cache/ibus/bus/registry || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
dconf update || :
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post gtk2
if [ $1 -eq 1 ] ; then
    gtk-query-immodules-2.0 >%{_libdir}/gtk-2.0/2.10.0/immodules.cache
fi

%postun gtk2
gtk-query-immodules-2.0 >%{_libdir}/gtk-2.0/2.10.0/immodules.cache

%post gtk3
if [ $1 -eq 1 ] ; then
    # For upgrades, the cache will be regenerated by the new package's %%postun
    /usr/bin/gtk-query-immodules-3.0 --update-cache &> /dev/null || :
fi

%postun gtk3
/usr/bin/gtk-query-immodules-3.0 --update-cache &> /dev/null || :


%files -f %{name}10.lang
%dir %{_datadir}/ibus/
%{_bindir}/ibus
%{_bindir}/ibus-daemon
%{_datadir}/bash-completion/completions/ibus.bash
%{_datadir}/GConf/gsettings/*
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/ibus/component
%{_datadir}/ibus/engine
%{_datadir}/ibus/keymaps
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/man/man1/ibus.1.gz
%{_datadir}/man/man1/ibus-daemon.1.gz
%{_datadir}/man/man5/ibus.conf.5.gz
%{_libexecdir}/ibus-engine-simple
%{_libexecdir}/ibus-dconf
%{_libexecdir}/ibus-ui-gtk3
%{_libexecdir}/ibus-x11
%{_sysconfdir}/dconf/db/ibus.d
%{_sysconfdir}/dconf/profile/ibus
%python_sitearch/gi/overrides/IBus.py*
# ibus owns xinput.d because gnome does not like to depend on imsettings.
%dir %{_sysconfdir}/X11/xinit/xinput.d
# Do not use %%config(noreplace) to always get the new keywords in _xinputconf
# For user customization, $HOME/.xinputrc can be used instead.
%config %{_xinputconf}

%files libs
%{_libdir}/libibus-%{ibus_api_version}.so.*
%{_libdir}/girepository-1.0/IBus-1.0.typelib

%files gtk2
%{_libdir}/gtk-2.0/*/immodules/im-ibus.so

%files gtk3
%{_libdir}/gtk-3.0/*/immodules/im-ibus.so

%files setup
%{_bindir}/ibus-setup
%{_datadir}/applications/ibus-setup.desktop
%{_datadir}/ibus/setup
%{_datadir}/man/man1/ibus-setup.1.gz

#%files pygtk2
#%dir %{python_sitelib}/ibus
#%{python_sitelib}/ibus/*

%files wayland
%{_libexecdir}/ibus-wayland

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gir-1.0/IBus-1.0.gir
%{_datadir}/vala/vapi/ibus-1.0.vapi
%{_datadir}/vala/vapi/ibus-1.0.deps

%files devel-docs
%{_datadir}/gtk-doc/html/ibus

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.5.10-3
- Rebuild for new 4.0 release.

* Mon Aug 17 2015 Cjacker <cjacker@foxmail.com>
- rebuild with older glib2. since we decrease glib2 for avoid filemonitor bug.
