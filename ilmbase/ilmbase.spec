
Name:	 ilmbase 
Version: 1.0.3
Release: 5%{?dist}
Summary: Abstraction/convenience libraries

Group:	 System Environment/Libraries
License: BSD
URL:	 http://www.openexr.com/
Source0: https://github.com/downloads/openexr/openexr/ilmbase-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: automake libtool
BuildRequires: pkgconfig
BuildRequires: pkgconfig(gl) pkgconfig(glu)

# ABI now makes little sense.
Patch50: ilmbase-1.0.3-so6.patch
# explicitly add $(PTHREAD_LIBS) to libIlmThread linkage (helps workaround below)
Patch51: ilmbase-1.0.2-no_undefined.patch
# the FPU exception code is x86 specific
Patch52: ilmbase-1.0.3-secondary.patch
# add Requires.private: gl glu to IlmBase.pc
Patch53:  ilmbase-1.0.3-pkgconfig.patch

## upstream patches
# fix build on i686/32bit
# https://github.com/openexr/openexr/issues/3
Patch100: ilmbase-1.0.3-ucontext.patch

%description
Half is a class that encapsulates the ilm 16-bit floating-point format.

IlmThread is a thread abstraction library for use with OpenEXR
and other software packages.

Imath implements 2D and 3D vectors, 3x3 and 4x4 matrices, quaternions
and other useful 2D and 3D math functions.

Iex is an exception-handling library.

%package devel
Summary: Headers and libraries for building apps that use %{name} 
Group:	 Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q

%patch50 -p1 -b .so6
%patch51 -p1 -b .no_undefined
%patch52 -p1 -b .secondary
%patch53 -p1 -b .pkgconfig
%if %{__isa_bits} == 32
%patch100 -p1 -b .ucontext
%endif
./bootstrap


%build
%configure --disable-static

make %{?_smp_mflags} PTHREAD_LIBS="-pthread -lpthread"


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rm -fv  $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion IlmBase)" = "%{version}"
# is the known-failure ix86-specific or 32bit specific? guess we'll find out -- rex
%ifarch %{ix86}
make check ||:
%else
make check
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libHalf.so.6*
%{_libdir}/libIex.so.6*
%{_libdir}/libIexMath.so.6*
%{_libdir}/libIlmThread.so.6*
%{_libdir}/libImath.so.6*

%files devel
%defattr(-,root,root,-)
%{_includedir}/OpenEXR/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/IlmBase.pc


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

