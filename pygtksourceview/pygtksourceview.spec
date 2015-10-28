%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define pygtk_version 2.8.0
%define pygobject_version 2.15.2
%define gtksourceview_version 2.3.0

Name:           pygtksourceview
Version:        2.10.1
Release:        12%{?dist}
Summary:        Python bindings for gtksourceview

# No version specified.
License:        LGPLv2+
URL:            http://download.gnome.org/sources/pygtksourceview/
#VCS: git:git://git.gnome.org/pygtksourceview
Source0:        http://download.gnome.org/sources/pygtksourceview/2.10/pygtksourceview-%{version}.tar.bz2

BuildRequires:  gtk-doc
BuildRequires:  gtksourceview2-devel >= %{gtksourceview_version}
BuildRequires:  pygobject2-devel >= %{pygobject_version}
BuildRequires:  pygtk2-devel >= %{pygtk_version}
BuildRequires:  python-devel

%description
The %{name} package contains Python bindings for the gtksourceview
library.

%package devel
Summary: Development files for using %{name} in Python programs
Requires: %{name} = %{version}-%{release}
Requires: %{name}-doc = %{version}-%{release}
Requires: gtksourceview2-devel >= %{gtksourceview_version}
Requires: pkgconfig
Requires: pygtk2-devel >= %{pygtk_version}

%description devel
This package contains files required to build Python programs that
use the %{name} bindings.

%package doc
Summary: Documentation files for %{name}

%description doc
This package contains documentation files for %{name}.

%prep
%setup -q

%build
%configure
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{python_sitearch}/gtksourceview2.la

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README NEWS
%{python_sitearch}/*

%files devel
%defattr(-,root,root,-)
%{_datadir}/pygtk/2.0/defs/gtksourceview2.defs
%{_libdir}/pkgconfig/pygtksourceview-2.0.pc

%files doc
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/pygtksourceview2

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.10.1-12
- Rebuild for new 4.0 release.

