Name:		imsettings
Version:	1.6.8
Release:	7
License:	LGPLv2+
URL:		https://tagoh.bitbucket.org/%{name}/
BuildRequires:	desktop-file-utils
BuildRequires:	intltool gettext
BuildRequires:	libtool automake autoconf
BuildRequires:	glib2 >= 2.32.0, gobject-introspection-devel, gtk3-devel >= 3.3.3
BuildRequires:	libnotify-devel
BuildRequires:	libX11-devel, libgxim-devel >= 0.5.0

Source0:	https://bitbucket.org/tagoh/%{name}/downloads/%{name}-%{version}.tar.bz2
## run IM for certain languages only
Patch0:		%{name}-constraint-of-language.patch
## Disable XIM support
Patch1:		%{name}-disable-xim.patch
## Enable xcompose for certain languages
Patch2:		%{name}-xinput-xcompose.patch
## Force enable the IM management on imsettings for Cinnamon
Patch3:		%{name}-force-enable-for-cinnamon.patch
Patch4:		%{name}-fix-configure.patch

Summary:	Delivery framework for general Input Method configuration
Requires:	xorg-x11-xinit >= 1.0.2-22.fc8
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-desktop-module%{?_isa} = %{version}-%{release}
Requires(post):	/usr/bin/dbus-send %{_sbindir}/alternatives
Requires(postun):	/usr/bin/dbus-send %{_sbindir}/alternatives
Suggests:	%{name}-gsettings

%description
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains the core DBus services and some utilities.

%package	libs
Summary:	Libraries for imsettings

%description	libs
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains the shared library for imsettings.

%package	devel
Summary:	Development files for imsettings
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	pkgconfig
Requires:	glib2-devel >= 2.32.0

%description	devel
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains the development files to make any
applications with imsettings.

%package	xim
Summary:	XIM support on imsettings
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	im-chooser

%description	xim
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working with XIM.

%package	gsettings
Summary:	GSettings support on imsettings
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	dconf
Provides:	imsettings-desktop-module%{?_isa} = %{version}-%{release}
Provides:	%{name}-gnome = %{version}-%{release}
Obsoletes:	%{name}-gnome < 1.5.1-3

%description	gsettings
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working on
GNOME and Cinnamon which requires GSettings in their
own XSETTINGS daemons.

%package	qt
Summary:	Qt support on imsettings
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	im-chooser
Provides:	imsettings-desktop-module%{?_isa} = %{version}-%{release}

%description	qt
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working on Qt
applications.

#%package    lxde
#Summary:    LXDE support on imsettings
#Group:      Applications/System
#Requires:   %{name}%{?_isa} = %{version}-%{release}
#Requires:   lxde-settings-daemon
## Hack for upgrades: see https://bugzilla.redhat.com/show_bug.cgi?id=693809
#Requires:   lxsession
#Requires:   /usr/bin/lxsession
#Requires:   im-chooser
#Provides:   imsettings-desktop-module%{?_isa} = %{version}-%{release}
#
#%description    lxde
#IMSettings is a framework that delivers Input Method
#settings and applies the changes so they take effect
#immediately without any need to restart applications
#or the desktop.
#
#This package contains a module to get this working on LXDE.
#
#%package    mate
#Summary:    MATE support on imsettings
#Group:      Applications/System
#Requires:   %{name}%{?_isa} = %{version}-%{release}
## need to keep more deps for similar reason to https://bugzilla.redhat.com/show_bug.cgi?id=693809
#Requires:   mate-settings-daemon >= 1.5.0
#Requires:   mate-session-manager
#Requires:   im-chooser
#Provides:   imsettings-desktop-module%{?_isa} = %{version}-%{release}
#
#%description    mate
#IMSettings is a framework that delivers Input Method
#settings and applies the changes so they take effect
#immediately without any need to restart applications
#or the desktop.
#
#This package contains a module to get this working on MATE.
#
#%package    cinnamon
#Summary:    Cinnamon support on imsettings
#Group:      Applications/System
#Requires:   %{name}%{?_isa} = %{version}-%{release}
## need to keep more deps for similar reason to https://bugzilla.redhat.com/show_bug.cgi?id=693809
#Requires:   cinnamon
#Requires:   cinnamon-session
#Requires:   im-chooser
#Provides:   imsettings-desktop-module%{?_isa} = %{version}-%{release}
#
#%description    cinnamon
#IMSettings is a framework that delivers Input Method
#settings and applies the changes so they take effect
#immediately without any need to restart applications
#or the desktop.
#
#This package contains a module to get this working on Cinnamon.


%prep
%setup -q
%patch0 -p1 -b .0-lang
%patch1 -p1 -b .1-xim
%patch2 -p1 -b .2-xcompose
%patch3 -p1 -b .3-force-cinnamon
%patch4 -p1 -b .4-fix-configure

%build
autoreconf -f
%configure	\
	--with-xinputsh=50-xinput.sh \
	--disable-static \
	--disable-schemas-install

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="/usr/bin/install -p"

# change the file attributes
chmod 0755 $RPM_BUILD_ROOT%{_libexecdir}/imsettings-target-checker.sh
chmod 0755 $RPM_BUILD_ROOT%{_libexecdir}/xinputinfo.sh
chmod 0755 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/50-xinput.sh

# clean up the unnecessary files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/imsettings/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/imsettings/libimsettings-{gconf,mateconf}.so

desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/imsettings-start.desktop

%find_lang %{name}


#%%check
## Disable it because it requires DBus session
# make check

%post
alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_sysconfdir}/X11/xinit/xinput.d/none.conf 10
alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_sysconfdir}/X11/xinit/xinput.d/xcompose.conf 20
alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_sysconfdir}/X11/xinit/xinput.d/xim.conf 30
dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig > /dev/null 2>&1 || :

%postun
if [ "$1" = 0 ]; then
	alternatives --remove xinputrc %{_sysconfdir}/X11/xinit/xinput.d/none.conf
	alternatives --remove xinputrc %{_sysconfdir}/X11/xinit/xinput.d/xcompose.conf
	alternatives --remove xinputrc %{_sysconfdir}/X11/xinit/xinput.d/xim.conf
	dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig > /dev/null 2>&1 || :
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files	-f %{name}.lang
%dir %{_libdir}/imsettings
%{_bindir}/imsettings-info
%{_bindir}/imsettings-list
%{_bindir}/imsettings-reload
%{_bindir}/imsettings-switch
%{_libexecdir}/imsettings-check
%{_libexecdir}/imsettings-daemon
%{_libexecdir}/xinputinfo.sh
%{_libexecdir}/imsettings-functions
%{_libexecdir}/imsettings-target-checker.sh
%{_datadir}/dbus-1/services/*.service
%{_datadir}/pixmaps/*.png
%{_sysconfdir}/X11/xinit/xinitrc.d/50-xinput.sh
%{_sysconfdir}/X11/xinit/xinput.d
%{_sysconfdir}/xdg/autostart/imsettings-start.desktop
%{_mandir}/man1/imsettings-*.1*

%files	libs
%{_libdir}/libimsettings.so.*

%files	devel
%{_includedir}/imsettings
%{_libdir}/libimsettings.so
%{_libdir}/pkgconfig/imsettings.pc
%{_libdir}/girepository-*/IMSettings-*.typelib
%{_datadir}/gir-*/IMSettings-*.gir
%{_datadir}/gtk-doc/html/imsettings

%files	xim
%{_bindir}/imsettings-xim
%{_libdir}/imsettings/libimsettings-xim.so

%files	gsettings
%{_libdir}/imsettings/libimsettings-gsettings.so

%files	qt
%{_libdir}/imsettings/libimsettings-qt.so

#%files  lxde
#%doc AUTHORS COPYING ChangeLog NEWS README
#%{_libdir}/imsettings/libimsettings-lxde.so
#
#%files  mate
#%doc AUTHORS COPYING ChangeLog NEWS README
#%{_libdir}/imsettings/libimsettings-mate-gsettings.so
#
#%files cinnamon
#%doc AUTHORS COPYING ChangeLog NEWS README
#%{_libdir}/imsettings/libimsettings-cinnamon-gsettings.so

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.6.8-7
- Rebuild for new 4.0 release.

