%global with_python3 1

%if 0%{?with_python3}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%endif
%{!?__python2:%global __python2 /usr/bin/python2}
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Summary: SIP - Python/C++ Bindings Generator
Name: sip
Version: 4.16.8
Release: 2%{?dist}

# sipgen/parser.{c.h} is GPLv3+ with exceptions (bison)
License: GPLv2 or GPLv3 and (GPLv3+ with exceptions)
Url: http://www.riverbankcomputing.com/software/sip/intro 
#URL: http://sourceforge.net/projects/pyqt/
Source0:  http://downloads.sourceforge.net/pyqt/sip-%{version}%{?snap:-snapshot-%{snap}}.tar.gz

## upstreamable patches
# make install should not strip (by default), kills -debuginfo
Patch50: sip-4.16.3-no_strip.patch
# try not to rpath the world
Patch51: sip-4.16.3-no_rpath.patch

## upstream patches

# extracted from sip.h, SIP_API_MAJOR_NR SIP_API_MINOR_NR defines
Source1: macros.sip
%global _sip_api_major 11
%global _sip_api_minor 2
%global _sip_api %{_sip_api_major}.%{_sip_api_minor}

Provides: sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}

BuildRequires: python2-devel
BuildRequires: sed

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

%description
SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python bindings for any C++
class library.

%package devel
Summary: Files needed to generate Python bindings for any C++ class library
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-macros = %{version}-%{release}
Requires: python2-devel
%description devel
This package contains files needed to generate Python bindings for any C++
classes library.

%package macros
Summary: RPM macros for use when working with SIP
Requires: rpm
# when arch->noarch happened
Obsoletes: sip-macros < 4.15.5
BuildArch: noarch
%description macros
This package contains RPM macros for use when working with SIP.
%if 0%{?with_python3}
It is used by both the sip-devel (python 2) and python3-sip-devel subpackages.
%endif

%if 0%{?with_python3}
%package -n python3-sip
Summary: SIP - Python 3/C++ Bindings Generator
Provides: python3-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python3-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python3-sip
This is the Python 3 build of SIP.

SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python 3 classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python 3 bindings for any C++
class library.

%package -n python3-sip-devel
Summary: Files needed to generate Python 3 bindings for any C++ class library
Requires: %{name}-macros = %{version}-%{release}
Requires: python3-sip%{?_isa} = %{version}-%{release}
Requires: python3-devel
%description -n python3-sip-devel
This package contains files needed to generate Python 3 bindings for any C++
classes library.
%endif


%prep

%setup -q -n %{name}-%{version}%{?snap:-snapshot-%{snap}}

%patch50 -p1 -b .no_strip
%patch51 -p1 -b .no_rpath

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} configure.py -d %{python3_sitearch} CXXFLAGS="%{optflags}" CFLAGS="%{optflags}" --sipdir=%{_datadir}/python3-sip

make %{?_smp_mflags} 
popd
%endif

%{__python2} configure.py -d %{python2_sitearch} CXXFLAGS="%{optflags}" CFLAGS="%{optflags}"

make %{?_smp_mflags}


%install
# Perform the Python 3 installation first, to avoid stomping over the Python 2
# /usr/bin/sip:
%if 0%{?with_python3}
pushd %{py3dir}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/python3-sip
mv %{buildroot}%{_bindir}/sip %{buildroot}%{_bindir}/python3-sip
popd
%endif

# Python 2 installation:
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/sip

# Macros used by -devel subpackages:
install -D -p -m644 %{SOURCE1} %{buildroot}%{rpm_macros_dir}/macros.sip


%files
%doc LICENSE LICENSE-GPL2 LICENSE-GPL3
%doc NEWS README
%{python2_sitearch}/sip.so
%{python2_sitearch}/sip*.py*

%files devel
%{_bindir}/sip
%{_datadir}/sip/
%{python2_inc}/*

%files macros
%{rpm_macros_dir}/macros.sip

%if 0%{?with_python3}
%files -n python3-sip
%{python3_sitearch}/sip.so
%{python3_sitearch}/sip*.py*

%files -n python3-sip-devel
# Note that the "sip" binary is invoked by name in a few places higher up
# in the KDE-Python stack; these will need changing to "python3-sip":
%{_bindir}/python3-sip
%{_datadir}/python3-sip/
%{python3_inc}/*
%endif


%changelog
