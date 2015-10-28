%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Last updated for 1.8.8
%define cairo_version 1.8.6

### Abstract ###

Name: pycairo
Version: 1.10.0
Release: 2 
License: MPLv1.1 or LGPLv2
Summary: Python bindings for the cairo library
URL: http://cairographics.org/pycairo
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Source: http://cairographics.org/releases/py2cairo-%{version}.tar.bz2

### Build Dependencies ###

BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: pkgconfig
BuildRequires: python-devel

%description
Python bindings for the cairo library.

%package devel
Summary: Libraries and headers for pycairo
Requires: %{name} = %{version}-%{release}
Requires: cairo-devel
Requires: pkgconfig
Requires: python-devel

%description devel
This package contains files required to build wrappers for cairo add-on
libraries so that they interoperate with pycairo.

%prep
%setup -q -n py2cairo-%{version}

%build
touch ./ChangeLog
libtoolize -f
aclocal
automake --add-missing
autoreconf
export LDFLAGS="`python-config --ldflags`"
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* INSTALL NEWS README
%doc examples doc/faq.rst doc/overview.rst doc/README
%{python_sitearch}/cairo/

%files devel
%defattr(-,root,root,-)
%{_includedir}/pycairo/
%{_libdir}/pkgconfig/pycairo.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.10.0-2
- Rebuild for new 4.0 release.

