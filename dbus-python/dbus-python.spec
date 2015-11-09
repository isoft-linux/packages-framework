Summary: D-Bus Python Bindings 
Name:    dbus-python
Version: 1.2.0
Release: 10

License: MIT
URL:     http://www.freedesktop.org/wiki/Software/DBusBindings/
Source0: http://dbus.freedesktop.org/releases/dbus-python/%{name}-%{version}.tar.gz
Source1: http://dbus.freedesktop.org/releases/dbus-python/%{name}-%{version}.tar.gz.asc

# Added functionality for Fedora server dbus api requested by sgallagh
# https://bugs.freedesktop.org/show_bug.cgi?id=26903#c9
Patch0:  object_manager.patch
# borrow centos7 patch to use sitearch properly
Patch2: 0001-Move-python-modules-to-architecture-specific-directo.patch

BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: python2-devel
BuildRequires: python-docutils
BuildRequires: python3-devel
# for %%check
BuildRequires: dbus-x11 pygobject3
# autoreconf and friends
BuildRequires: autoconf automake libtool

Provides: python-dbus = %{version}-%{release}
Provides: python-dbus%{?_isa} = %{version}-%{release}

%description
D-Bus python bindings for use with python programs.   

%package devel
Summary: Libraries and headers for dbus-python
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Headers and static libraries for hooking up custom mainloops to the dbus python
bindings.

%package -n python3-dbus
Summary: D-Bus bindings for python3
%description -n python3-dbus
%{summary}.


%prep
%setup -q
%patch0 -p1 -b .object_manager
%patch2 -p1 -b .sitearch

# For new arches (aarch64/ppc64le), and patch2
autoreconf -vif


%build
%global _configure ../configure

mkdir python2-build; pushd python2-build
%configure PYTHON=python
make %{?_smp_mflags}
popd

mkdir python3-build; pushd python3-build
%configure PYTHON=python3
make %{?_smp_mflags}
popd


%install
make install DESTDIR=$RPM_BUILD_ROOT -C python3-build
make install DESTDIR=$RPM_BUILD_ROOT -C python2-build

# unpackaged files
rm -fv  $RPM_BUILD_ROOT%{python2_sitearch}/*.la
rm -fv  $RPM_BUILD_ROOT%{python3_sitearch}/*.la
rm -rfv $RPM_BUILD_ROOT%{_datadir}/doc/dbus-python/


%check
make check -k -C python2-build
make check -k -C python3-build


%files
%doc COPYING NEWS
%{python2_sitearch}/*.so
%{python2_sitearch}/dbus/

%files devel
%doc README ChangeLog doc/API_CHANGES.txt doc/HACKING.txt doc/tutorial.txt
%{_includedir}/dbus-1.0/dbus/dbus-python.h
%{_libdir}/pkgconfig/dbus-python.pc

%files -n python3-dbus
%doc COPYING
%{python3_sitearch}/*.so
%{python3_sitearch}/dbus/


%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.2.0-10
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.2.0-9
- Rebuild for new 4.0 release.

