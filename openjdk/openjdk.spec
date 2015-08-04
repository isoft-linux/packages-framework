%global script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%global abs2rel %{__perl} -e %{script}

Name:	    openjdk	
Version:    8u45b14	
Release:	1
Summary:	Oracle OpenJDK 7 via IcedTea

License:  ASL 1.1 and ASL 2.0 and GPL+ and GPLv2 and GPLv2 with exceptions and LGPL+ and LGPLv2 and MPLv1.0 and MPLv1.1 and Public Domain and W3C
URL:      http://openjdk.java.net/

Source0:   http://hg.openjdk.java.net/jdk8u/jdk8u/archive/jdk8u-jdk8u45-b14.tar.bz2

Source1:    http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-1.8.0.45/corba.tar.xz
Source2:    http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-1.8.0.45/hotspot.tar.xz
Source3:    http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-1.8.0.45/jaxp.tar.xz
Source4:    http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-1.8.0.45/jaxws.tar.xz
Source5:    http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-1.8.0.45/langtools.tar.xz
Source6:    http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-1.8.0.45/jdk.tar.xz

Source7:    http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-1.8.0.45/nashorn.tar.xz

BuildRequires: alsa-lib-devel
BuildRequires: openjdk
BuildRequires: cpio unzip which zip
BuildRequires: cups-devel
BuildRequires: libX11
BuildRequires: giflib-devel

Source100:  openjdk-path.sh

Patch1: 8017773.diff
Patch2: 8067231.diff
Patch3:  8074312.diff
Patch4:  adlc-parser.patch
Patch5:  alpha-float-const.diff
Patch6:  applet-hole.patch
Patch7:  autoconf-select.diff
Patch8:  autoconf-updates.diff
Patch9:  compare-pointer-with-literal.patch
Patch10:  disable-doclint-by-default.diff
Patch11:  dnd-files.patch
Patch12:  dont-strip-images.diff
Patch13:  enumipv6-fix.patch
Patch14:  hotspot-disable-werror.diff
Patch15:  hotspot-set-compiler.diff
Patch16:  hotspot-warn-no-errformat.diff
Patch17:  icedtea-4953367.patch
Patch18:  jdk-8067331.diff
Patch19:  jdk-freeNativeStringArray-decl.diff
Patch20:  jdk-freetypeScaler-crash.diff
Patch21:  ld-symbolic-functions-default.diff
Patch22:  libjpeg-fix.diff
Patch23:  libpcsclite-dlopen.diff
Patch24:  link-with-as-needed.diff
Patch25:  make4-compatibility.diff
Patch26:  nonreparenting-wm.diff
Patch27:  no-pch-build.diff
Patch28:  zero-missing-headers.diff
Patch29:  isoft-jdk-fix-build-with-gcc5-avoid-overflow.patch
Patch30:  giflib5-fix.patch

#from tuxjdk
#https://code.google.com/p/tuxjdk/
Patch40: add-fontconfig-support.diff 
Patch41: fix-typographical-point-size.diff 
Patch42: lcd-hrgb-by-default.diff

#this patch is a modified version of patch20, should applied after tuxjdk
Patch50: jdk-freetypeScaler-crash-with-tuxjdk.diff


#this patch is force to enable on the spot input method style for fcitx.
#Cursor follow issue still exists!!!!!!!!!!!
#currently, there is no way to fix it in awt_InputMethod.c
#By Cjacker
Patch60: force-to-on-the-spot-xim-style.patch

#try to fix cursor follow issue in SWING/AWT, swing should works. awt still had some problem about cursor position calculate.
#!!!!!!!!!!!!!!Please do not apply this time, since it's will cause deadlock.
Patch61: try-to-fix-xim-spotlocation.patch

BuildRequires: gcc
BuildRequires: findutils tar zip gawk pkgconfig util-linux
BuildRequires: ca-certificates libxslt zip
BuildRequires: autoconf automake 
BuildRequires: nss-devel cups-devel 
BuildRequires: libjpeg-turbo-devel giflib-devel libpng-devel lcms2-devel 
BuildRequires: libXt-devel libXp-devel libXtst-devel libXinerama-devel libXrender-devel 
BuildRequires: libattr-devel zlib-devel alsa-lib-devel freetype-devel fontconfig-devel krb5-devel
BuildRequires: gtk2-devel 

#disable autorequires and provides
AutoReqProv: no
#at least
Requires: libgcc, libstdc++

#for trust
Requires: p11-kit-trust

%description
%{summary}

%prep
%setup -q -n jdk8u-jdk8u45-b14 -a1 -a2 -a3 -a4 -a5 -a6 -a7 
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
#%patch13 -p1
%patch14 -p1
%patch15 -p1
#%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch21 -p1
#%patch22 -p1
%patch23 -p1
#%patch24 -p1
%patch25 -p1
%patch26 -p1
#%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1

%patch40 -p1
#this patch is wrong to use hardcode 72dpi
#%patch41 -p1
%patch42 -p1


%patch50 -p1


%patch60 -p1
#%patch61 -p1


%build
#ensure use gcc/g++
export CC=gcc
export CXX=g++

#Modern Java installations do not need JAVA_HOME 
unset JAVA_HOME

sh ./configure \
   --with-update-version=45 \
   --with-build-number=b14 \
   --with-debug-level=release \
   --enable-unlimited-crypto  \
   --with-zlib=system \
   --with-giflib=system \
   --with-x \
   --with-cups \
   --with-alsa \
   --with-jobs=`/usr/bin/getconf _NPROCESSORS_ONLN`

make DISABLE_HOTSPOT_OS_VERSION_CHECK=ok all

find build/*/images/j2sdk-image -iname \*.diz -delete


%install
IMG_PATH=`find . -name j2sdk-image -type d`

mkdir -p $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8

cp -RT $IMG_PATH $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8


#fix perms, use ||: to avoid failed.
pushd $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8
find . -perm 600|xargs chmod 644 ||:
popd

install -Dm0755 %{SOURCE100} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/openjdk-path.sh


# Install cacerts symlink.
rm -f $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8/jre/lib/security/cacerts
pushd $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8/jre/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_libdir}/jvm/openjdk8/jre/lib/security)
    ln -sf $RELATIVE/cacerts .
popd

%post

%files
%{_sysconfdir}/profile.d/openjdk-path.sh
%dir %{_libdir}/jvm/openjdk8
%{_libdir}/jvm/openjdk8/*

%changelog

