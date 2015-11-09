%define cairo_version 1.10.2

Name: python3-cairo
Version: 1.10.0
Release: 3 
License: MPLv1.1 or LGPLv2
Summary: Python 3 bindings for the cairo library
URL: http://cairographics.org/pycairo

Source: http://cairographics.org/releases/pycairo-%{version}.tar.bz2
Patch0: pycairo-1.10.0-waf_unpack-1.patch
Patch1: pycairo-1.10.0-waf_python_3_4-1.patch

BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: pkgconfig
BuildRequires: python3-devel

%description
Python 3 bindings for the cairo library.

%package devel
Summary: Libraries and headers for python3-cairo
Requires: %{name} = %{version}-%{release}
Requires: cairo-devel
Requires: pkgconfig
Requires: python3-devel

%description devel
This package contains files required to build wrappers for cairo add-on
libraries so that they interoperate with python3-cairo.

%prep
%setup -q -n pycairo-%{version}
%patch0 -p1
wafdir=$(./waf unpack)
pushd $wafdir
%patch1 -p1
popd
unset wafdir

%build
# FIXME: we should be using the system version of waf (e.g. %{_bindir}/waf)
export CFLAGS="$RPM_OPT_FLAGS"
PYTHON=/usr/bin/python3 ./waf --prefix=%{_usr} \
              --libdir=%{_libdir} \
              configure

# do not fail on utf-8 encoded files
LANG=en_US.utf8 ./waf build -v

# remove executable bits from examples
find ./examples/ -type f -print0 | xargs -0 chmod -x

# add executable bit to the _cairo.so library so we strip the debug info:wq

%install
DESTDIR=$RPM_BUILD_ROOT ./waf install
# add executable bit to the .so libraries so we strip the debug info
find $RPM_BUILD_ROOT -name '*.so' | xargs chmod +x

find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f

#%check
#cd test
#PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch} %{_bindir}/py.test-3*

%files
%{_libdir}/python*/site-packages/cairo/

%files devel
%{_includedir}/pycairo/py3cairo.h
%{_libdir}/pkgconfig/py3cairo.pc

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.10.0-3
- Fix build with py35

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.10.0-2
- Rebuild for new 4.0 release.

