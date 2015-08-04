Name:          gypsy
Version:       0.9
Release:       5%{?dist}
Summary:       A GPS multiplexing daemon

Group:         System Environment/Libraries
# See LICENSE file for details
License:       LGPLv2 and GPLv2
URL:           http://gypsy.freedesktop.org/
Source0:       http://gypsy.freedesktop.org/releases/%{name}-%{version}.tar.gz
Patch0:        gypsy-0.8-unusedvar.patch
Patch1:        gypsy-0.9-gtypeinit.patch

BuildRequires: bluez-libs-devel
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: glib2-devel
BuildRequires: gtk-doc
BuildRequires: libgudev-devel
BuildRequires: libxslt

Requires: dbus

%description
Gypsy is a GPS multiplexing daemon which allows multiple clients to 
access GPS data from multiple GPS sources concurrently. 

%package devel
Summary: Development package for gypsy
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: dbus-glib-devel
Requires: pkgconfig

%description devel
Header files for development with gypsy.

%package docs
Summary: Documentation files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description docs
This package contains developer documentation for %{name}.

%prep
%setup -q
%patch0 -p1 -b .unusedvar
%patch1 -p1 -b .gtypeinit

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libgypsy.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING COPYING.lib LICENSE
%config(noreplace) %{_sysconfdir}/gypsy.conf
%{_sysconfdir}/dbus-1/system.d/Gypsy.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.Gypsy.service
%{_libexecdir}/gypsy-daemon
%{_libdir}/libgypsy.so.0
%{_libdir}/libgypsy.so.0.0.0

%files devel
%{_libdir}/pkgconfig/gypsy.pc
%{_includedir}/gypsy
%{_libdir}/libgypsy.so

%files docs
%doc %{_datadir}/gtk-doc/html/gypsy

%changelog
