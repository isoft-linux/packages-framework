Name:           lib3ds
Version:        1.3.0
Release:        20%{?dist}

Summary:        3D Studio file format library

License:        LGPLv2+
URL:            http://lib3ds.sourceforge.net
Source:         http://downloads.sourceforge.net/lib3ds/lib3ds-%{version}.zip
Patch0:         lib3ds-1.3.0-lib3ds-file.h.diff
Patch1:         lib3ds-1.3.0-lib3ds-mesh.c.diff
Patch2:         lib3ds-1.2.0-pkgconfig.diff
Patch3:         lib3ds-1.3.0-config.patch

%description
lib3ds is a free ANSI-C library for working with the popular "3ds" 3D model
format.

Supported platforms include GNU (autoconf, automake, libtool, make, GCC) on
Unix and Cygwin, and MS Visual C++ 6.0. lib3ds loads and saves Atmosphere
settings, Background settings, Shadow map settings, Viewport setting,
Materials, Cameras, Lights, Meshes, Hierarchy, Animation keyframes. It also
contains useful matrix, vector and quaternion mathematics tools. lib3ds
usually integrates well with OpenGL. In addition, some diagnostic and
conversion tools are included.

%package        tools
Summary:        %summary

%description    tools
Some tools to process 3ds files.

%files          tools
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/3dsdump
%{_mandir}/man1/3dsdump.1*

%package        devel
Summary:        %summary
Requires:	pkgconfig
Requires:	lib3ds = %{version}-%{release}

%description    devel
Development files for lib3ds


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
%configure  --disable-static

make %{?_smp_mflags}

sed -e 's,@prefix@,%{_prefix},' \
  -e 's,@exec_prefix@,%{_exec_prefix},' \
  -e 's,@libdir@,%{_libdir},' \
  -e 's,@includedir@,%{_includedir},' \
  -e 's,@VERSION@,%{version},' \
  lib3ds.pc.in > lib3ds.pc

%install
make install DESTDIR=$RPM_BUILD_ROOT

install -d ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
install lib3ds.pc -m 0644 ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig

## Remove libtool archive
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/*.so.*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files devel
%defattr(-,root,root,-)
%{_bindir}/lib3ds-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/lib3ds.pc
%{_mandir}/man1/lib3ds-config.1*
%{_includedir}/lib3ds
%{_datadir}/aclocal/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.3.0-20
- Rebuild for new 4.0 release.

