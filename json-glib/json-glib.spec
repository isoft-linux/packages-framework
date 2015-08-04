%define glib_ver 2.16

Name:		json-glib
Version:    1.0.4
Release:	2
Summary:	Library for JavaScript Object Notation format

Group:	    Framework/Runtime/Library	
License:	LGPLv2+
URL:		http://live.gnome.org/JsonGlib
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.11/%{name}-%{version}.tar.xz

BuildRequires:	glib2-devel >= %{glib_ver}
BuildRequires:	gobject-introspection-devel


%description
%{name} is a library providing serialization and deserialization support
for the JavaScript Object Notation (JSON) format.


%package devel
Summary:	Development files for %{name}
Group:		Framework/Development/Library
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= %{glib_ver}
Requires:	pkgconfig


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}


%build
%configure --enable-static=no
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Copy the files from the tarball to avoid the IDs generated by gtk-doc being
# different on different builds
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/%{name}/
cp -a doc/reference/html/* $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/%{name}/

%find_lang json-glib-1.0
rpmclean
%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -f json-glib-1.0.lang
%defattr(-,root,root,-)
%doc COPYING README NEWS
%{_libdir}/lib%{name}*.so.*
%{_libdir}/girepository-1.0/Json-1.0.typelib
%{_bindir}/json-glib-format
%{_bindir}/json-glib-validate
%{_mandir}/man1/json-glib-format.1.gz
%{_mandir}/man1/json-glib-validate.1.gz

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}-1.0.pc
%{_includedir}/%{name}-1.0/
%{_datadir}/gtk-doc/html/%{name}/
%{_datadir}/gir-1.0/Json-1.0.gir


%changelog
