Name:		tigervnc
Version:	1.5.0
Release:	3%{?dist}
Summary:	A TigerVNC remote display system

License:	GPLv2+
URL:		http://www.tigervnc.com

Source0:	%{name}-%{version}.tar.gz
Source6:	vncviewer.desktop

BuildRequires:	libX11-devel, automake, autoconf, libtool, gettext
BuildRequires:	libXext-devel, libXi-devel
BuildRequires:	xorg-x11-xtrans-devel, xorg-x11-util-macros, libXtst-devel
BuildRequires:	libdrm-devel, libXt-devel, pixman-devel libXfont-devel
BuildRequires:	libxkbfile-devel, openssl-devel, libpciaccess-devel
BuildRequires:	mesa-libGL-devel, libXinerama-devel, ImageMagick
BuildRequires:  freetype-devel, libXdmcp-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libjpeg-turbo-devel, gnutls-devel, pam-devel
BuildRequires:	cmake
# TigerVNC 1.4.x requires fltk 1.3.3 for keyboard handling support
# See https://github.com/TigerVNC/tigervnc/issues/8, also bug #1208814
BuildRequires:	fltk-devel >= 1.3.3
%ifnarch s390 s390x
BuildRequires:  xorg-x11-server-devel
%endif

Requires(post):	coreutils
Requires(postun):coreutils

Requires:	hicolor-icon-theme

Provides:	vnc = 4.1.3-2, vnc-libs = 4.1.3-2
Obsoletes:	vnc < 4.1.3-2, vnc-libs < 4.1.3-2
Provides:	tightvnc = 1.5.0-0.15.20090204svn3586
Obsoletes:	tightvnc < 1.5.0-0.15.20090204svn3586

Patch1:		tigervnc-cookie.patch
Patch2:		tigervnc-fix-reversed-logic.patch
Patch3:		tigervnc-libvnc-os.patch
Patch4:		tigervnc11-rh692048.patch
Patch5:		tigervnc-inetd-nowait.patch
Patch7:		tigervnc-manpages.patch
Patch8:		tigervnc-getmaster.patch
Patch9:		tigervnc-shebang.patch
Patch14:	tigervnc-xstartup.patch
Patch15:	tigervnc-xserver118.patch
Patch17:	tigervnc-xorg118-QueueKeyboardEvents.patch

# This is tigervnc-%%{version}/unix/xserver116.patch rebased on the latest xorg
Patch100:       tigervnc-xserver116-rebased.patch

%description
Virtual Network Computing (VNC) is a remote display system which
allows you to view a computing 'desktop' environment not only on the
machine where it is running, but from anywhere on the Internet and
from a wide variety of machine architectures.  This package contains a
client which will allow you to connect to other desktops running a VNC
server.

%prep
%setup -q

%patch1 -p1 -b .cookie
%patch2 -p1 -b .fix-reversed-logic
%patch3 -p1 -b .libvnc-os
%patch4 -p1 -b .rh692048

# Synchronise manpages and --help output (bug #980870).
%patch7 -p1 -b .manpages

# libvnc.so: don't use unexported GetMaster function (bug #744881 again).
%patch8 -p1 -b .getmaster

# Don't use shebang in vncserver script.
%patch9 -p1 -b .shebang

%build
%ifarch sparcv9 sparc64 s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
export CXXFLAGS="$CFLAGS"

%{cmake} .
make %{?_smp_mflags}

# Build icons
pushd media
make
popd

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{README.txt,LICENCE.TXT}

# Install desktop stuff
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/{16x16,24x24,48x48}/apps

pushd media/icons
for s in 16 24 48; do
install -m644 tigervnc_$s.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x$s/apps/tigervnc.png
done
popd

mkdir $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	%{SOURCE6}


#hide the menu item
echo "NoDisplay=true" >> $RPM_BUILD_ROOT%{_datadir}/applications/vncviewer.desktop

%find_lang %{name} %{name}.lang

# remove unwanted files
rm -f  $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/libvnc.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch -c %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor || :
fi

%postun
touch -c %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README.txt
%{_bindir}/vncviewer
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/vncviewer.1*

%changelog
* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- initial build. only client.
