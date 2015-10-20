%global api_ver 2.0

Name:             gtksourceviewmm2
Version:          2.10.3
Release:          9%{?dist}
Summary:          A C++ wrapper for the gtksourceview widget library

Group:            System Environment/Libraries
License:          LGPLv2+
URL:              http://projects.gnome.org/gtksourceviewmm/
Source0:          http://ftp.gnome.org/pub/GNOME/sources/gtksourceviewmm/2.10/gtksourceviewmm-%{version}.tar.xz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    gtkmm2-devel >= 2.12
BuildRequires:    gtksourceview2-devel >= 2.10.0


%description
gtksourceviewmm is a C++ wrapper for the gtksourceview widget
library. It offers all the power of gtksourceview with an interface
familiar to c++ developers, including users of the gtkmm library


%package          devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         gtkmm2-devel
Requires:         gtksourceview2-devel
Requires:         pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package          doc
Summary:          Developer's documentation for the gtksourceviewmm library
Group:            Documentation
BuildArch:        noarch
Requires:         gtkmm2-doc

%description      doc
This package contains developer's documentation for the Gtksourceviewmm
library. Gtksourceviewmm is the C++ API for the Gtksourceview library.

The documentation can be viewed either through the devhelp
documentation browser or through a web browser.

%prep
%setup -q -n gtksourceviewmm-%{version}


%build
export CXXFLAGS="-std=c++11"
%configure --disable-static
# removing rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog


%install
rm -rf $RPM_BUILD_ROOT
make INSTALL="install -c -p" DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README AUTHORS COPYING ChangeLog NEWS
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/gtksourceviewmm-2.0
%{_libdir}/*.so
%{_libdir}/gtksourceviewmm-2.0
%{_libdir}/pkgconfig/*.pc


%files doc
%defattr(-, root, root, -)
%doc COPYING
%doc %{_datadir}/devhelp/
%doc %{_docdir}/gtksourceviewmm-%{api_ver}


%changelog
