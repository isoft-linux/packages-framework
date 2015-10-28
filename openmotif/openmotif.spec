#%define intern_name openMotif
%define intern_name openmotif

Summary: Open Motif runtime libraries and executables.
Name: openmotif
Version: 2.3.4
Release: 3
License: Open Group Public License
Source: motif-%{version}-src.tgz
Source1: xmbind
URL: http://www.motifzone.net/

BuildRequires: flex
BuildRequires: byacc, pkgconfig
BuildRequires: libjpeg-devel libpng-devel
BuildRequires: libXft-devel libXmu-devel libXt-devel libXext-devel
BuildRequires: xorg-x11-xbitmaps
BuildRequires: perl

Patch22: openmotif-no-demos.patch
Patch23: openMotif-2.2.3-uil_lib.patch
Patch43: openMotif-2.3.0-rgbtxt.patch
Patch47: openMotif-2.3.0-no_X11R6.patch
Conflicts: lesstif <= 0.92.32-6

Prefix: /usr

%description
This is the Open Motif %{version} runtime environment. It includes the
Motif shared libraries, needed to run applications which are dynamically
linked against Motif, and the Motif Window Manager "mwm".

%package devel
Summary: Open Motif development libraries and header files.
Conflicts: lesstif-devel <= 0.92.32-6
Requires: openmotif = %{version}-%{release}
Requires: libjpeg-devel libpng-devel
Requires: libXft-devel libXmu-devel libXt-devel libXext-devel

%description devel
This is the Open Motif %{version} development environment. It includes the
static libraries and header files necessary to build Motif applications.

%prep
%setup -q -n motif-%{version}
%patch22 -p1 -b .no_demos
%patch23 -p1 -b .uil_lib
%patch43 -p1 -b .rgbtxt
%patch47 -p1 -b .no_X11R6
for i in doc/man/man3/{XmColumn,XmDataField}.3; do
	iconv -f windows-1252 -t utf-8 < "$i" > "${i}_"
	mv "${i}_" "$i"
done

%build
./autogen.sh
CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" \
./configure \
   --prefix=%{prefix} \
   --libdir=%{prefix}/%{_lib} \
   --mandir=%{_datadir}/man \
   --enable-static \
   --enable-xft \
   --enable-jpeg \
   --enable-png

# do not use rpath
perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool

export LD_LIBRARY_PATH=`pwd`/lib/Mrm/.libs:`pwd`/lib/Xm/.libs
make clean
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

export LD_LIBRARY_PATH=`pwd`/lib/Mrm/.libs:`pwd`/lib/Xm/.libs
make DESTDIR=$RPM_BUILD_ROOT prefix=%{prefix} install
mkdir -p $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d \
         $RPM_BUILD_ROOT/usr/include

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/xmbind.sh

rm -fr $RPM_BUILD_ROOT%{prefix}/%{_lib}/*.la \
       $RPM_BUILD_ROOT%{prefix}/share/Xm/doc
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/X11/xinit/xinitrc.d/xmbind.sh
%{_prefix}/%{_lib}/X11/system.mwmrc
%{prefix}/bin/mwm
%{prefix}/bin/xmbind
%{prefix}/include/X11/bitmaps/*
%{prefix}/%{_lib}/libMrm.so.*
%{prefix}/%{_lib}/libUil.so.*
%{prefix}/%{_lib}/libXm.so.*
%{_libdir}/X11/bindings
%{_datadir}/man/man1/mwm*
%{_datadir}/man/man1/xmbind*
%{_datadir}/man/man4/mwmrc*

%files devel
%defattr(-,root,root)
%{prefix}/bin/uil
%{prefix}/include/Mrm
%{prefix}/include/Xm
%{prefix}/include/uil
%{prefix}/%{_lib}/lib*.a
%{prefix}/%{_lib}/lib*.so
%{_datadir}/man/man1/uil.1*
%{_datadir}/man/man3/*
%{_datadir}/man/man5/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.3.4-3
- Rebuild for new 4.0 release.

