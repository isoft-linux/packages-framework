# Define this to link to which library version  eg. /lib64/ld-lsb-x86-64.so.3
%define lsbsover 3 

%ifarch %{ix86}
%define ldso ld-linux.so.2
%define lsbldso ld-lsb.so
%endif

%ifarch ia64
%define ldso ld-linux-ia64.so.2
%define lsbldso ld-lsb-ia64.so
%endif

%ifarch ppc
%define ldso ld.so.1
%define lsbldso ld-lsb-ppc32.so
%endif

%ifarch ppc64
%define ldso ld64.so.1
%define lsbldso ld-lsb-ppc64.so
%endif

%ifarch ppc64le
%define ldso ld64.so.2
%define lsbldso ld-lsb-ppc64le.so
%endif

%ifarch s390
%define ldso ld.so.1
%define lsbldso ld-lsb-s390.so
%endif

%ifarch s390x
%define ldso ld64.so.1
%define lsbldso ld-lsb-s390x.so
%endif

%ifarch x86_64
%define ldso ld-linux-x86-64.so.2
%define lsbldso ld-lsb-x86-64.so
%endif

%ifarch %{arm}
%define ldso ld-linux.so.2
%define lsbldso ld-lsb-arm.so
%endif

%ifarch aarch64
%define ldso ld-linux-aarch64.so.1
%define lsbldso ld-lsb-aarch64.so
%endif

%define upstreamlsbrelver 2.0
%define lsbrelver 4.1
%define srcrelease 1

Summary: Implementation of Linux Standard Base specification
Name: isoft-lsb
Version: 4.1
Release: 31
URL: http://www.linuxfoundation.org/collaborate/workgroups/lsb
Source0: %{name}-%{version}-%{srcrelease}.tar.bz2
Patch0: lsb-release-3.1-update-init-functions.patch
Patch1: isoft-lsb-lsb_start_daemon-fix.patch
Patch2: isoft-lsb-trigger.patch
Patch3: isoft-lsb-arm.patch
Patch4: isoft-lsb-aarch64.patch
License: GPLv2
BuildRequires: glibc-devel

%ifarch %{ix86}
%define archname ia32
%endif
%ifarch ia64
%define archname ia64
%endif
%ifarch ppc
%define archname ppc32
%endif
%ifarch ppc64
%define archname ppc64
%endif
%ifarch ppc64le
%define archname ppc64le
%endif
%ifarch s390
%define archname s390
%endif
%ifarch s390x
%define archname s390x
%endif
%ifarch x86_64
%define archname amd64
%endif
%ifarch %{arm}
%define archname arm
%endif
%ifarch aarch64
%define archname aarch64
%endif

ExclusiveArch: %{ix86} ia64 x86_64 ppc ppc64 s390 s390x %{arm} aarch64 ppc64le

Requires: isoft-lsb-core%{?_isa} = %{version}-%{release}
Requires: isoft-lsb-cxx%{?_isa} = %{version}-%{release}
Requires: isoft-lsb-desktop%{?_isa} = %{version}-%{release}
Requires: isoft-lsb-languages = %{version}-%{release}
Requires: isoft-lsb-printing = %{version}-%{release}
#Requires: isoft-lsb-trialuse = %{version}-%{release}

Provides: lsb = %{version}-%{release}
Provides: lsb-%{archname} = %{version}-%{release}
Provides: lsb-noarch = %{version}-%{release}

%description
The Linux Standard Base (LSB) is an attempt to develop a set of standards that
will increase compatibility among Linux distributions. It is designed to be 
binary-compatible and produce a stable application binary interface (ABI) for
independent software vendors.
The lsb package provides utilities, libraries etc. needed for LSB Compliant 
Applications. It also contains requirements that will ensure that all 
components required by the LSB are installed on the system.

%package submod-security
Summary: LSB Security submodule support
Requires: nspr%{?_isa}
# Requires: nspr-devel
Requires: nss%{?_isa}

Provides: lsb-submod-security-%{archname} = %{version}-%{release}
Provides: lsb-submod-security-noarch = %{version}-%{release}

%description submod-security
The Linux Standard Base (LSB) Security submodule specifications define 
components that are required to be present on an LSB conforming system.

%package submod-multimedia
Summary: LSB Multimedia submodule support
Requires: alsa-lib%{?_isa}

Provides: lsb-submod-multimedia-%{archname} = %{version}-%{release}
Provides: lsb-submod-multimedia-noarch = %{version}-%{release}

%description submod-multimedia
The Linux Standard Base (LSB) Multimedia submodule specifications define 
components that are required to be present on an LSB conforming system.

%package core
Summary: LSB Core module support
# gLSB Library
Requires: glibc%{?_isa}
Requires: glibc-common
Requires: libgcc%{?_isa}
Requires: ncurses-libs%{?_isa}
Requires: pam%{?_isa}
Requires: zlib%{?_isa}

# gLSB Command and Utilities
Requires: /bin/basename
Requires: /bin/cat
Requires: /bin/chgrp
Requires: /bin/chmod
Requires: /bin/chown
Requires: /bin/cp
Requires: /bin/date
Requires: /bin/dd
Requires: /bin/df
Requires: /bin/dmesg
Requires: /bin/echo
Requires: /usr/bin/ed
Requires: /usr/bin/egrep
Requires: /bin/false
Requires: /usr/bin/fgrep
Requires: /bin/find
Requires: /usr/bin/grep
Requires: /bin/gunzip
Requires: /bin/gzip
Requires: /bin/kill
Requires: /bin/ln
Requires: /bin/ls
Requires: /bin/mailx
Requires: /bin/mkdir
Requires: /bin/mknod
Requires: /bin/mktemp
Requires: /bin/more
Requires: /bin/mount
Requires: /bin/mv
Requires: /bin/nice
Requires: /usr/bin/ps
Requires: /bin/pwd
Requires: /bin/rm
Requires: /bin/rmdir
Requires: /bin/sed
Requires: /bin/sh
Requires: /bin/sleep
Requires: /bin/sort
Requires: /bin/stty
Requires: /bin/sync
Requires: /usr/bin/tar
Requires: /bin/touch
Requires: /bin/true
Requires: /bin/umount
Requires: /bin/uname
Requires: /bin/zcat
Requires: /sbin/shutdown
Requires: /usr/bin/[
Requires: /usr/bin/ar
Requires: /usr/bin/at
Requires: /usr/bin/awk
Requires: /usr/bin/batch
Requires: /usr/bin/bc
Requires: /usr/bin/chfn
Requires: /usr/bin/chsh
Requires: /usr/bin/cksum
Requires: /usr/bin/cmp
Requires: /usr/bin/col
Requires: /usr/bin/comm
Requires: /bin/cpio
Requires: /usr/bin/crontab
Requires: /usr/bin/csplit
Requires: /usr/bin/cut
Requires: /usr/bin/diff
Requires: /usr/bin/dirname
Requires: /usr/bin/du
Requires: /usr/bin/env
Requires: /usr/bin/expand
Requires: /usr/bin/expr
Requires: /usr/bin/file
Requires: /usr/bin/find
Requires: /usr/bin/fold
Requires: /usr/bin/gencat
Requires: /usr/bin/getconf
Requires: /usr/bin/gettext
Requires: /usr/bin/groups
Requires: /usr/bin/head
Requires: /usr/bin/hostname
Requires: /usr/bin/iconv
Requires: /usr/bin/id
Requires: /usr/bin/install
Requires: /usr/bin/ipcrm
Requires: /usr/bin/ipcs
Requires: /usr/bin/join
Requires: /usr/bin/killall
Requires: /usr/bin/locale
Requires: /usr/bin/localedef
Requires: /usr/bin/logger
Requires: /usr/bin/logname
Requires: /usr/bin/lp
Requires: /usr/bin/lpr
Requires: /usr/bin/m4
Requires: /usr/bin/make
Requires: /usr/bin/man
Requires: /usr/bin/md5sum
Requires: /usr/bin/mkfifo
Requires: /usr/bin/msgfmt
Requires: /usr/bin/newgrp
Requires: /usr/bin/nl
Requires: /usr/bin/nohup
Requires: /usr/bin/od
Requires: /usr/bin/passwd
Requires: /usr/bin/paste
Requires: /usr/bin/patch
Requires: /usr/bin/pathchk
#better POSIX conformance of /usr/bin/pax
Requires: spax
Requires: /usr/bin/pidof
Requires: /usr/bin/pr
Requires: /usr/bin/printf
Requires: /usr/bin/renice
Requires: /usr/bin/seq
Requires: /usr/bin/split
Requires: /usr/bin/strings
Requires: /usr/bin/strip
Requires: /usr/bin/su
Requires: /usr/bin/tail
Requires: /usr/bin/tee
Requires: /usr/bin/test
Requires: /usr/bin/time
Requires: /usr/bin/tr
Requires: /usr/bin/tsort
Requires: /usr/bin/tty
Requires: /usr/bin/unexpand
Requires: /usr/bin/uniq
Requires: /usr/bin/wc
Requires: /usr/bin/xargs
Requires: /usr/sbin/fuser
Requires: /usr/sbin/groupadd
Requires: /usr/sbin/groupdel
Requires: /usr/sbin/groupmod
Requires: /usr/sbin/useradd
Requires: /usr/sbin/userdel
Requires: /usr/sbin/usermod
Requires: /usr/sbin/sendmail
Requires: isoft-lsb-submod-security%{?_isa} = %{version}-%{release}

Provides: lsb-core-%{archname} = %{version}-%{release}
Provides: lsb-core-noarch = %{version}-%{release}
#Obsoletes: isoft-lsb < %{version}-%{release}

%description core
The Linux Standard Base (LSB) Core module support provides the fundamental
system interfaces, libraries, and runtime environment upon which all conforming
applications and libraries depend.

%package cxx
Summary: LSB CXX module support
Requires: libstdc++%{?_isa}
Requires: isoft-lsb-core%{?_isa} = %{version}-%{release}

Provides: lsb-cxx-%{archname} = %{version}-%{release}
Provides: lsb-cxx-noarch = %{version}-%{release}

%description cxx
The Linux Standard Base (LSB) CXX module supports the core interfaces by
providing system interfaces, libraries, and a runtime environment for 
applications built using the C++ programming language. These interfaces 
provide low-level support for the core constructs of the language, and 
implement the standard base C++ libraries.

%package desktop
Summary: LSB Desktop module support
Requires: xdg-utils
# LSB_Graphics library
Requires: libICE%{?_isa}
Requires: libSM%{?_isa}
Requires: libX11%{?_isa}
Requires: libXext%{?_isa}
Requires: libXi%{?_isa}
Requires: libXt%{?_isa}
Requires: libXtst%{?_isa}
Requires: mesa-libGL%{?_isa}
Requires: libGLU%{?_isa}
# gLSB Graphics and gLSB Graphics Ext Command and Utilities
Requires: /usr/bin/fc-cache
Requires: /usr/bin/fc-list
Requires: /usr/bin/fc-match
# gLSB Graphics Ext library
Requires: cairo%{?_isa}
Requires: freetype%{?_isa}
Requires: libjpeg-turbo%{?_isa}

%ifarch %{ix86} ppc s390 arm
Requires: libpng12.so.0
%endif
%ifarch x86_64 ppc64 s390x aarch64 ppc64le
Requires: libpng12.so.0()(64bit)
%endif
Requires: libpng%{?_isa}
Requires: libXft%{?_isa}
Requires: libXrender%{?_isa}
# toolkit-gtk
Requires: atk%{?_isa}
Requires: gdk-pixbuf2%{?_isa}
Requires: glib2%{?_isa}
Requires: gtk2%{?_isa}
Requires: pango%{?_isa}
# toolkit-qt
Requires: qt4%{?_isa}
# toolkit-qt3
Requires: qt3%{?_isa}
# xml
Requires: libxml2%{?_isa}
Requires: isoft-lsb-submod-multimedia%{?_isa} = %{version}-%{release}
Requires: isoft-lsb-core%{?_isa} = %{version}-%{release}

Provides: lsb-desktop-%{archname} = %{version}-%{release}
Provides: lsb-desktop-noarch = %{version}-%{release}
Provides: lsb-graphics-%{archname} = %{version}-%{release}
Provides: lsb-graphics-noarch = %{version}-%{release}
Obsoletes: isoft-lsb-graphics < %{version}-%{release}

%description desktop
The Linux Standard Base (LSB) Desktop Specifications define components that are
required to be present on an LSB conforming system.

%package languages
Summary: LSB Languages module support
# Perl and Perl non-builtin modules
Requires: /usr/bin/perl
Requires: perl(CGI)
Requires: perl(Class::ISA)
Requires: perl(CPAN)
# Locale::Constants has been Locale::Codes::Costants, so we need
# create a /usr/share/perl5/vendor_perl/Constants.pm manually.
# Requires: perl(Locale::Constants)
# perl(Locale::Constants) requires perl(Locale::Codes)
# DB module is a builtin module, but perl package doesn't contain this provide.
# Requires: perl(DB)
# we also need perl(Pod::Plainer), we need to rpm this package ourself
Requires: perl(Locale::Codes)
Requires: perl(File::Spec)
Requires: perl(Scalar::Util)
Requires: perl(Test::Harness)
Requires: perl(Test::Simple)
Requires: perl(ExtUtils::MakeMaker)
Requires: perl(Pod::Plainer)
Requires: perl(XML::LibXML)
Requires: perl(Pod::LaTeX)
Requires: perl(Pod::Checker)
Requires: perl(B::Lint)
Requires: perl(Text::Soundex)
Requires: perl(Env)
Requires: perl(Time::HiRes)
Requires: perl(Locale::Maketext)
Requires: perl(Fatal)
Requires: perl(File::CheckTree)
Requires: perl(Sys::Syslog)


# python
Requires: /usr/bin/python
# java
Requires: isoft-lsb-core%{?_isa} = %{version}-%{release}

Provides: lsb-languages-%{archname} = %{version}-%{release}
Provides: lsb-languages-noarch = %{version}-%{release}

%description languages
The Linux Standard Base (LSB) Languages module supports components for runtime
languages which are found on an LSB conforming system.

%package printing
Summary: LSB Printing module support
# gLSB Printing Libraries
Requires: cups-libs
# gLSB Printing Command and Utilities
Requires: /usr/bin/foomatic-rip
Requires: /usr/bin/gs
Requires: isoft-lsb-core%{?_isa} = %{version}-%{release}

Provides: lsb-printing-%{archname} = %{version}-%{release}
Provides: lsb-printing-noarch = %{version}-%{release}
Obsoletes: isoft-lsb-printing < %{version}-%{release}

%description printing
The Linux Standard Base (LSB) Printing specifications define components that 
are required to be present on an LSB conforming system.

%package trialuse
Summary: LSB Trialuse module support
Requires: isoft-lsb-submod-multimedia%{?_isa} = %{version}-%{release}
Requires: isoft-lsb-submod-security%{?_isa} = %{version}-%{release}
Requires: isoft-lsb-core%{?_isa} = %{version}-%{release}

Provides: lsb-trialuse-%{archname} = %{version}-%{release}
Provides: lsb-trialuse-noarch = %{version}-%{release}

%description trialuse
The Linux Standard Base (LSB) Trialuse module support defines components
which are not required parts of the LSB Specification.

%package supplemental
Summary: LSB supplemental dependencies required by LSB certification tests
Requires: net-tools
Requires: fonts-Cantarell
Requires: xorg-x11-server-Xvfb

%description supplemental
This subpackage brings in supplemental dependencies for components required for
passing LSB (Linux Standard Base) certification testsuite, but not directly required
to be on LSB conforming system.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0 -b .triggerfix
%patch3 -p1 -b .arm
%patch4 -p1 -b .aarch64

%build
cd lsb-release-%{upstreamlsbrelver}
make

%pre
# remove the extra symlink /bin/mailx -> /bin/mail
if [ -e /bin/mailx ]; then
   if [ -L /bin/mailx ]; then
     rm -f /bin/mailx
   fi
fi

%install
# LSB uses /usr/lib rather than /usr/lib64 even for 64bit OS
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir} $RPM_BUILD_ROOT/%{_lib} $RPM_BUILD_ROOT%{_mandir} \
         $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT/usr/lib/lsb \
         $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/ $RPM_BUILD_ROOT%{_sbindir} \
         $RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}

# manually add Locale::Constants. This module is just an alias of Locale::Codes::Constants
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/Locale
cp -p Constants.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Locale
cp -p Constants.pod $RPM_BUILD_ROOT%{perl_vendorlib}/Locale

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
cd lsb-release-%{upstreamlsbrelver}
make mandir=$RPM_BUILD_ROOT/%{_mandir} prefix=$RPM_BUILD_ROOT/%{_prefix} install
cd ..
# we keep more lsb information in /usr/share/lsb
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/submodules

#prepare installation of doc
cp -p lsb-release-2.0/COPYING .
cp -p lsb-release-2.0/README README.lsb_release

# relations between modules and submodules
modules="core cxx desktop languages printing trialuse"
submodules="core perl python cpp toolkit-gtk toolkit-qt toolkit-qt3"
submodules="${submodules} xml multimedia security desktop-misc graphics graphics-ext"
submodules="${submodules} printing"

core="core security"
cxx="cpp"
desktop="desktop-misc graphics graphics-ext multimedia toolkit-gtk toolkit-qt toolkit-qt3"
desktop="${desktop} xml"
languages="perl python"
printing="printing"
trialuse="security multimedia"

for mod in ${modules};do
  touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/${mod}-%{lsbrelver}-%{archname}
  touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/${mod}-%{lsbrelver}-noarch
done

for submod in ${submodules};do
  touch $RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/submodules/${submod}-%{lsbrelver}-%{archname}
  touch $RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/submodules/${submod}-%{lsbrelver}-noarch
done
for moddir in ${modules};do
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/${moddir}
done

for submod in ${core};do
  ln -snf ../../submodules/${submod}-%{lsbrelver}-%{archname} \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/core/${submod}-%{lsbrelver}-%{archname}
  ln -snf ../../submodules/${submod}-%{lsbrelver}-noarch \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/core/${submod}-%{lsbrelver}-noarch
done
for submod in ${cxx};do
  ln -snf ../../submodules/${submod}-%{lsbrelver}-%{archname} \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/cxx/${submod}-%{lsbrelver}-%{archname}
  ln -snf ../../submodules/${submod}-%{lsbrelver}-noarch \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/cxx/${submod}-%{lsbrelver}-noarch
done
for submod in ${desktop};do
  ln -snf ../../submodules/${submod}-%{lsbrelver}-%{archname} \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/desktop/${submod}-%{lsbrelver}-%{archname}
  ln -snf ../../submodules/${submod}-%{lsbrelver}-noarch \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/desktop/${submod}-%{lsbrelver}-noarch
done
for submod in ${languages};do
  ln -snf ../../submodules/${submod}-%{lsbrelver}-%{archname} \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/languages/${submod}-%{lsbrelver}-%{archname}
  ln -snf ../../submodules/${submod}-%{lsbrelver}-noarch \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/languages/${submod}-%{lsbrelver}-noarch
done
for submod in ${printing};do
  ln -snf ../../submodules/${submod}-%{lsbrelver}-%{archname} \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/printing/${submod}-%{lsbrelver}-%{archname}
  ln -snf ../../submodules/${submod}-%{lsbrelver}-noarch \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/printing/${submod}-%{lsbrelver}-noarch
done
for submod in ${trialuse};do
  ln -snf ../../submodules/${submod}-%{lsbrelver}-%{archname} \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/trialuse/${submod}-%{lsbrelver}-%{archname}
  ln -snf ../../submodules/${submod}-%{lsbrelver}-noarch \
$RPM_BUILD_ROOT%{_datadir}/lsb/%{lsbrelver}/modules/trialuse/${submod}-%{lsbrelver}-noarch
done

for LSBVER in %{lsbsover}; do
  ln -snf %{ldso} $RPM_BUILD_ROOT/%{_lib}/%{lsbldso}.$LSBVER
done

mkdir -p $RPM_BUILD_ROOT/bin

# LSB uses /usr/lib rather than /usr/lib64 even for 64bit OS
# According to the lsb-core documentation provided by 
# http://refspecs.linux-foundation.org/LSB_3.2.0/LSB-Core-generic/LSB-Core-generic.pdf
# it's OK to put non binary in /usr/lib.
ln -snf ../../../sbin/chkconfig $RPM_BUILD_ROOT/usr/lib/lsb/install_initd
ln -snf ../../../sbin/chkconfig $RPM_BUILD_ROOT/usr/lib/lsb/remove_initd
#ln -snf mail $RPM_BUILD_ROOT/bin/mailx

#mkdir -p $RPM_BUILD_ROOT/usr/X11R6/lib/X11/xserver
#ln -snf /usr/%{_lib}/xserver/SecurityPolicy $RPM_BUILD_ROOT/usr/X11R6/lib/X11/xserver/SecurityPolicy
#ln -snf /usr/share/X11/fonts $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts
#ln -snf /usr/share/X11/rgb.txt  $RPM_BUILD_ROOT/usr/X11R6/lib/X11/rgb.txt

# According to https://bugzilla.isoft.com/show_bug.cgi?id=232918 , the '-static' option
# is imported against segfault error while running isoft_lsb_trigger
%ifarch %{arm}
gcc $RPM_OPT_FLAGS -Os -fno-stack-protector -o isoft_lsb_trigger{.%{_target_cpu},.c} -DLSBSOVER='"%{lsbsover}"' \
  -DLDSO='"%{ldso}"' -DLSBLDSO='"/%{_lib}/%{lsbldso}"' -D_GNU_SOURCE
%else
gcc $RPM_OPT_FLAGS -Os -static -fno-stack-protector -o isoft_lsb_trigger{.%{_target_cpu},.c} -DLSBSOVER='"%{lsbsover}"' \
  -DLDSO='"%{ldso}"' -DLSBLDSO='"/%{_lib}/%{lsbldso}"' -D_GNU_SOURCE
%endif
install -p -m 700 isoft_lsb_trigger.%{_target_cpu} \
  $RPM_BUILD_ROOT%{_sbindir}/isoft_lsb_trigger.%{_target_cpu}

cp -p isoft_lsb_init $RPM_BUILD_ROOT/bin/isoft_lsb_init

%triggerpostun -- glibc
if [ -x /usr/sbin/isoft_lsb_trigger.%{_target_cpu} ]; then
  /usr/sbin/isoft_lsb_trigger.%{_target_cpu}
fi

%ifnarch %{ix86}
  /sbin/sln %{ldso} /%{_lib}/%{lsbldso} || :
%else
  if [ -f /emul/ia32-linux/lib/%{ldso} ]; then
    for LSBVER in %{lsbsover}; do
      /sbin/sln /emul/ia32-linux/lib/%{ldso} /%{_lib}/%{lsbldso}.$LSBVER || :
    done
  else
    for LSBVER in %{lsbsover}; do
      /sbin/sln %{ldso} /%{_lib}/%{lsbldso}.$LSBVER || :
    done
  fi
%endif

%post
%ifarch %{ix86}
# make this softlink again for /emul
  if [ -f /emul/ia32-linux/lib/%{ldso} ]; then
    for LSBVER in %{lsbsover}; do
      /sbin/sln /emul/ia32-linux/lib/%{ldso} /%{_lib}/%{lsbldso}.$LSBVER || :
    done
  fi
%endif

%postun submod-security -p <lua>
os.remove("%{_datadir}/lsb/%{lsbrelver}/submodules")
os.remove("%{_datadir}/lsb/%{lsbrelver}/modules")
os.remove("%{_datadir}/lsb/%{lsbrelver}")
os.remove("%{_datadir}/lsb")
%postun submod-multimedia -p <lua>
os.remove("%{_datadir}/lsb/%{lsbrelver}/submodules")
os.remove("%{_datadir}/lsb/%{lsbrelver}/modules")
os.remove("%{_datadir}/lsb/%{lsbrelver}")
os.remove("%{_datadir}/lsb")
%postun core -p <lua> 
os.remove("%{_datadir}/lsb/%{lsbrelver}/submodules")
os.remove("%{_datadir}/lsb/%{lsbrelver}/modules")
os.remove("%{_datadir}/lsb/%{lsbrelver}")
os.remove("%{_datadir}/lsb")
%postun cxx -p <lua> 
os.remove("%{_datadir}/lsb/%{lsbrelver}/submodules")
os.remove("%{_datadir}/lsb/%{lsbrelver}/modules")
os.remove("%{_datadir}/lsb/%{lsbrelver}")
os.remove("%{_datadir}/lsb")
%postun desktop -p <lua> 
os.remove("%{_datadir}/lsb/%{lsbrelver}/submodules")
os.remove("%{_datadir}/lsb/%{lsbrelver}/modules")
os.remove("%{_datadir}/lsb/%{lsbrelver}")
os.remove("%{_datadir}/lsb")
%postun languages -p <lua> 
os.remove("%{_datadir}/lsb/%{lsbrelver}/submodules")
os.remove("%{_datadir}/lsb/%{lsbrelver}/modules")
os.remove("%{_datadir}/lsb/%{lsbrelver}")
os.remove("%{_datadir}/lsb")
%postun printing -p <lua> 
os.remove("%{_datadir}/lsb/%{lsbrelver}/submodules")
os.remove("%{_datadir}/lsb/%{lsbrelver}/modules")
os.remove("%{_datadir}/lsb/%{lsbrelver}")
os.remove("%{_datadir}/lsb")
%postun trialuse -p <lua> 
os.remove("%{_datadir}/lsb/%{lsbrelver}/submodules")
os.remove("%{_datadir}/lsb/%{lsbrelver}/modules")
os.remove("%{_datadir}/lsb/%{lsbrelver}")
os.remove("%{_datadir}/lsb")

%files
%{_datadir}/lsb/

%files submod-security
%{_datadir}/lsb/%{lsbrelver}/submodules/security-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/security-%{lsbrelver}-noarch

%files submod-multimedia
%{_datadir}/lsb/%{lsbrelver}/submodules/multimedia-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/multimedia-%{lsbrelver}-noarch

%files core
%doc README README.lsb_release COPYING
%{_sysconfdir}/isoft-lsb
%dir %{_sysconfdir}/lsb-release.d
%{_mandir}/*/*
%{_bindir}/*
#/bin/mailx
/bin/isoft_lsb_init
/usr/lib/lsb
/%{_lib}/*so*
/lib/lsb*
%{_sbindir}/isoft_lsb_trigger.%{_target_cpu}
%{_datadir}/lsb/%{lsbrelver}/modules/core
%{_sysconfdir}/lsb-release.d/core*
%{_datadir}/lsb/%{lsbrelver}/submodules/core-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/core-%{lsbrelver}-noarch

%files cxx
%{_sysconfdir}/lsb-release.d/cxx*
%{_datadir}/lsb/%{lsbrelver}/modules/cxx
%{_datadir}/lsb/%{lsbrelver}/submodules/cpp-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/cpp-%{lsbrelver}-noarch

%files desktop
%{_sysconfdir}/lsb-release.d/desktop*
%{_datadir}/lsb/%{lsbrelver}/modules/desktop
%{_datadir}/lsb/%{lsbrelver}/submodules/toolkit-gtk-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/toolkit-gtk-%{lsbrelver}-noarch
%{_datadir}/lsb/%{lsbrelver}/submodules/toolkit-qt-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/toolkit-qt-%{lsbrelver}-noarch
%{_datadir}/lsb/%{lsbrelver}/submodules/toolkit-qt3-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/toolkit-qt3-%{lsbrelver}-noarch
%{_datadir}/lsb/%{lsbrelver}/submodules/xml-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/xml-%{lsbrelver}-noarch
%{_datadir}/lsb/%{lsbrelver}/submodules/desktop-misc-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/desktop-misc-%{lsbrelver}-noarch
%{_datadir}/lsb/%{lsbrelver}/submodules/graphics-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/graphics-%{lsbrelver}-noarch
%{_datadir}/lsb/%{lsbrelver}/submodules/graphics-ext-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/graphics-ext-%{lsbrelver}-noarch

%files languages
%{_sysconfdir}/lsb-release.d/languages*
%{_datadir}/lsb/%{lsbrelver}/modules/languages
%{_datadir}/lsb/%{lsbrelver}/submodules/perl-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/perl-%{lsbrelver}-noarch
%{perl_vendorlib}/Locale/Constants.pm
%{perl_vendorlib}/Locale/Constants.pod
%{_datadir}/lsb/%{lsbrelver}/submodules/python-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/python-%{lsbrelver}-noarch

%files printing
%{_sysconfdir}/lsb-release.d/printing*
%{_datadir}/lsb/%{lsbrelver}/modules/printing
%{_datadir}/lsb/%{lsbrelver}/submodules/printing-%{lsbrelver}-%{archname}
%{_datadir}/lsb/%{lsbrelver}/submodules/printing-%{lsbrelver}-noarch

%files trialuse
%{_sysconfdir}/lsb-release.d/trialuse*
%{_datadir}/lsb/%{lsbrelver}/modules/trialuse

%files supplemental
#no files, just dependencies


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.1-31
- Rebuild for new 4.0 release.

