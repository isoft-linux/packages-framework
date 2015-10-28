#global		snap r9671

# TODO:
# *  port .spec to use cmake

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Summary:	C++ user interface toolkit
Name:		fltk
Version:	1.3.3
Release:	6%{?dist}

# see COPYING (or http://www.fltk.org/COPYING.php ) for exceptions details
License:	LGPLv2+ with exceptions	
URL:		http://www.fltk.org/
%if "%{?snap:1}" == "1"
Source0:        http://ftp.easysw.com/pub/fltk/snapshots/fltk-1.3.x-%{snap}.tar.bz2
%else
Source0:	http://ftp.easysw.com/pub/fltk/%{version}%{?pre}/%{name}-%{version}%{?pre}-source.tar.gz
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1: fltk-config.sh

## FIXME/TODO: upstream these asap -- Rex
# add lib64 support, drop extraneous libs (bug #708185) and ldflags (#1112930)
Patch1:        	fltk-1.3.2-fltk_config.patch
Patch5: 	fltk-1.1.8-fluid_desktop.patch

## upstream patches
Patch100: fltk-1.3.3-no_undefined.patch
Patch101: fltk-1.3-L3156.patch

#we force font match of Sans/Serif to "English font" in fontconfig.
#here will have a problem that Fox will get an English font even when under none en locale.
#But remember, the root cause is not our fault(althouth we force font matching to English font)
#Here is a dirty fix, at least for CJK.
#By Cjacker.
Patch200: fltk-atleast-cjk-respect-locale-for-fclang.patch

BuildRequires: desktop-file-utils
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(gl) pkgconfig(glu) 
BuildRequires: pkgconfig(ice)
BuildRequires: pkgconfig(sm) 
BuildRequires: pkgconfig(xext) pkgconfig(xinerama) pkgconfig(xft) pkgconfig(xt) pkgconfig(x11) 
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xproto)
BuildRequires: xorg-x11-utils
BuildRequires: zlib-devel
BuildRequires: autoconf

%description
FLTK (pronounced "fulltick") is a cross-platform C++ GUI toolkit.
It provides modern GUI functionality without the bloat, and supports
3D graphics via OpenGL and its built-in GLUT emulation.


%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libstdc++-devel
Requires: pkgconfig(ice) pkgconfig(sm)
Requires: pkgconfig(xft) pkgconfig(xt) pkgconfig(x11)
%description devel
%{summary}.

%package static
Summary: Static libraries for %{name}
Requires: %{name}-devel = %{version}-%{release}
%description static
%{summary}.

%package fluid
Summary: Fast Light User Interface Designer
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-devel
%description fluid
%{summary}, an interactive GUI designer for %{name}. 


%prep
%if 0%{?snap:1}
%setup -q -n fltk-1.3.x-%{snap}
%else
%setup -q  -n fltk-%{version}%{?pre}
%endif

%patch1 -p1 -b .fltk_config
%patch5 -p1 -b .fluid_desktop
%patch100 -p1 -b .no_undefined
%patch101 -p0 -b .L3156

%patch200 -p1

# verbose build output
sed -i.silent '\,^.SILENT:,d' makeinclude.in
autoconf


%build

# using --with-optim, so unset CFLAGS/CXXFLAGS
export CFLAGS=""
export CXXFLAGS=""

%configure \
  --with-links \
  --with-optim="%{optflags}" \
  --enable-largefile \
  --enable-shared \
  --enable-threads \
  --enable-xdbe \
  --enable-xinerama \
  --enable-xft

make %{?_smp_mflags}


%install

make install install-desktop DESTDIR=$RPM_BUILD_ROOT 

# omit examples/games: 
make -C test uninstall-linux DESTDIR=$RPM_BUILD_ROOT
rm -f  $RPM_BUILD_ROOT%{_mandir}/man?/{blocks,checkers,sudoku}*

# we only apply this hack to multilib arch's
%ifarch x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparc
%global arch %(uname -i 2>/dev/null || echo undefined)
mv $RPM_BUILD_ROOT%{_bindir}/fltk-config \
   $RPM_BUILD_ROOT%{_bindir}/fltk-config-%{arch}
install -p -m755 -D %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fltk-config
%endif

# docs
rm -rf __docs
mv $RPM_BUILD_ROOT%{_docdir}/fltk __docs

## unpackaged files
# errant docs
rm -rf $RPM_BUILD_ROOT%{_mandir}/cat*

#Hide fluid menu item
echo "NoDisplay=true" >> $RPM_BUILD_ROOT%{_datadir}/applications/fluid.desktop

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/fluid.desktop


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ANNOUNCEMENT CHANGES COPYING CREDITS README
%{_libdir}/libfltk.so.1.3
%{_libdir}/libfltk_forms.so.1.3
%{_libdir}/libfltk_gl.so.1.3
%{_libdir}/libfltk_images.so.1.3

%files devel
%defattr(-,root,root,-)
%doc __docs/*
%{_bindir}/fltk-config
%{?arch:%{_bindir}/fltk-config-%{arch}}
%{_includedir}/FL/
%{_includedir}/Fl
%{_libdir}/libfltk.so
%{_libdir}/libfltk_forms.so
%{_libdir}/libfltk_gl.so
%{_libdir}/libfltk_images.so
%{_mandir}/man1/fltk-config.1*
%{_mandir}/man3/fltk.3*

%files static
%defattr(-,root,root,-)
%{_libdir}/libfltk.a
%{_libdir}/libfltk_forms.a
%{_libdir}/libfltk_gl.a
%{_libdir}/libfltk_images.a

%post fluid
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun fluid
if [ $1 -eq 0 ] ; then
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans fluid
update-desktop-database -q &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files fluid
%defattr(-,root,root,-)
%{_bindir}/fluid
%{_mandir}/man1/fluid.1*
%{_datadir}/applications/fluid.desktop
%{_datadir}/icons/hicolor/*/*/*
# FIXME, add according to new mime spec
%{_datadir}/mimelnk/*/*.desktop


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.3.3-6
- Rebuild for new 4.0 release.

* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- hide fluid menu item.
