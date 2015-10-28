
Name:    pinentry
Version: 0.9.2
Release: 3
Summary: Collection of simple PIN or passphrase entry dialogs

# qt & qt4 subpackage have different license, see subpackage definitions
License: GPLv2+
URL:     http://www.gnupg.org/aegypten/
Source0: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2.sig

# borrowed from opensuse
Source10: pinentry-wrapper

Patch1: 0001-Fix-qt4-pinentry-window-created-in-the-background.patch

BuildRequires: gtk2-devel
BuildRequires: libcap-devel
BuildRequires: ncurses-devel
BuildRequires: qt4-devel

Provides: %{name}-curses = %{version}-%{release}

%description
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the curses (text) based version of the PIN entry dialog.

%package gtk
Summary: Passphrase/PIN entry dialog based on GTK+
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
Provides: pinentry-gtk2 = %{version}-%{release}
%description gtk
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the GTK GUI based version of the PIN entry dialog.

%package qt
Summary: Passphrase/PIN entry dialog based on Qt4
# original code for secstring.cpp doesn't allow GPL versions higher than 3 to be
# used
License: GPLv2 or GPLv3
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
Obsoletes: pinentry-qt4 < 0.8.0-2
Provides:  pinentry-qt4 = %{version}-%{release}
%description qt
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the Qt4 GUI based version of the PIN entry dialog.


%prep
%setup -q

%patch1 -p1

%build

CXXFLAGS="%{optflags} -std=c++11"

%configure \
  --disable-rpath \
  --disable-dependency-tracking \
  --without-libcap \
  --enable-pinentry-gtk2 \
  --enable-pinentry-qt4

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Backwards compatibility
ln -s pinentry-gtk-2 $RPM_BUILD_ROOT%{_bindir}/pinentry-gtk
ln -s pinentry-qt4 $RPM_BUILD_ROOT%{_bindir}/pinentry-qt

install -p -m755 -D %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/pinentry

# unpackaged files
rm -rf $RPM_BUILD_ROOT%{_infodir}


%files
%{_bindir}/pinentry-curses
%{_bindir}/pinentry

%files gtk
%{_bindir}/pinentry-gtk
%{_bindir}/pinentry-gtk-2

%files qt
%{_bindir}/pinentry-qt
%{_bindir}/pinentry-qt4


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.9.2-3
- Rebuild for new 4.0 release.

