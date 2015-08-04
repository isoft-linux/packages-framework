# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           glibmm
Version:        2.44.0
Release:        1
Summary:        C++ interface for the GLib library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/glibmm/%{release_version}/glibmm-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  libsigc++-devel

%description
glibmm is the official C++ interface for the popular cross-platform
library GLib. It provides non-UI API that is not available in standard
C++ and makes it possible for gtkmm to wrap GObject-based APIs.


%package devel
Summary:        Headers for developing programs that will use %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel
Requires:       libsigc++-devel

%description devel
This package contains the static libraries and header files needed for
developing glibmm applications.


%package        doc
Summary:        Documentation for %{name}, includes full API docs
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       libsigc++-doc

%description    doc
This package contains the full API documentation for %{name}.


%prep
%setup -q -n glibmm-%{version}


%build
%configure %{!?_with_static: --disable-static}
# removing rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

rpmclean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/glibmm-2.4/
%{_includedir}/giomm-2.4/
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%{_libdir}/glibmm-2.4/
%{_libdir}/giomm-2.4/
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{_datadir}/devhelp/
%doc %{_docdir}/glibmm-2.4/


%changelog
