Summary: Tools for certain user account management tasks
Name: usermode
Version: 1.111
Release: 8%{?dist}
License: GPLv2+
URL: https://fedorahosted.org/usermode/
Source: https://fedorahosted.org/releases/u/s/usermode/usermode-%{version}.tar.xz
Source1: config-util
Requires: pam, util-linux
#for passwd
Requires: shadow-utils
BuildRequires: gettext, glib2-devel, gtk2-devel, intltool
BuildRequires: libblkid-devel, libSM-devel, libuser-devel
BuildRequires: pam-devel, perl-XML-Parser, startup-notification-devel
BuildRequires: util-linux

%package gtk
Summary: Graphical tools for certain user account management tasks
Requires: %{name} = %{version}-%{release}

%global _hardened_build 1

%description
The usermode package contains the userhelper program, which can be
used to allow configured programs to be run with superuser privileges
by ordinary users.

%description gtk
The usermode-gtk package contains several graphical tools for users:
userinfo, usermount and userpasswd.  Userinfo allows users to change
their finger information.  Usermount lets users mount, unmount, and
format file systems.  Userpasswd allows users to change their
passwords.

Install the usermode-gtk package if you would like to provide users with
graphical tools for certain account management tasks.

%prep
%setup -q

%build
%configure --without-selinux

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

# make userformat symlink to usermount
ln -sf usermount $RPM_BUILD_ROOT%{_bindir}/userformat
ln -s usermount.1 $RPM_BUILD_ROOT%{_mandir}/man1/userformat.1

mkdir -p $RPM_BUILD_ROOT/etc/security/console.apps
install -p -m 644 %{SOURCE1} \
	$RPM_BUILD_ROOT/etc/security/console.apps/config-util

rm -rf $RPM_BUILD_ROOT%{_datadir}/applications

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING ChangeLog NEWS README
%attr(4711,root,root) /usr/sbin/userhelper
%{_bindir}/consolehelper
%{_mandir}/man8/userhelper.8*
%{_mandir}/man8/consolehelper.8*
%config(noreplace) /etc/security/console.apps/config-util

%files gtk
%{_bindir}/usermount
%{_mandir}/man1/usermount.1*
%{_bindir}/userformat
%{_mandir}/man1/userformat.1*
%{_bindir}/userinfo
%{_mandir}/man1/userinfo.1*
%{_bindir}/userpasswd
%{_mandir}/man1/userpasswd.1*
%{_bindir}/consolehelper-gtk
%{_mandir}/man8/consolehelper-gtk.8*
%{_bindir}/pam-panel-icon
%{_mandir}/man1/pam-panel-icon.1*
%{_datadir}/%{name}
%{_datadir}/pixmaps/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.111-8
- Rebuild for new 4.0 release.

