%global apiver 3.0
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           gtkmm
Version:        3.18.0
Release:        1
Summary:        C++ interface for the GTK+ library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gtkmm/%{release_version}/gtkmm-%{version}.tar.xz

BuildRequires:  atkmm-devel
BuildRequires:  cairomm-devel
BuildRequires:  glibmm-devel
BuildRequires:  gtk3-devel
BuildRequires:  pangomm-devel

%description
gtkmm is the official C++ interface for the popular GUI library GTK+.
Highlights include type safe callbacks, and a comprehensive set of
widgets that are easily extensible via inheritance.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        API documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       glibmm-doc

%description    doc
This package contains the full API documentation for %{name}.


%prep
%setup -q -n gtkmm-%{version}

# Copy demos before build to avoid including built binaries in -doc package
mkdir -p _docs
cp -a demos/ _docs/


%build
%configure --disable-static

# fix lib64 rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# avoid unused direct dependencies
sed -i 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rpmclean

%check
make check %{?_smp_mflags}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/gtkmm-%{apiver}/
%{_includedir}/gdkmm-%{apiver}/
%{_libdir}/*.so
%{_libdir}/gtkmm-%{apiver}/
%{_libdir}/gdkmm-%{apiver}/
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{_docdir}/gtkmm-%{apiver}/
%doc %{_datadir}/devhelp/
%doc _docs/*


%changelog
* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

