%global pkgconfdir      %{_sysconfdir}/dpkg
%global pkgdatadir      %{_datadir}/dpkg

Summary: Debian package management system.	
Name: dpkg 
Version: 1.18.1
Release: 7 
License: GPLv2 and GPLv2+ and LGPLv2+ and Public Domain and BSD
Source: http://ftp.de.debian.org/debian/pool/main/d/dpkg/dpkg_%{version}.tar.xz
#dummy file.
Source2: http://ftp.de.debian.org/debian/pool/main/d/debhelper/debhelper_9.20150628.tar.xz

Patch0:         dpkg-perl-libexecdir.patch
Patch1:         dpkg-fix-logrotate.patch
Patch3:         dpkg-tar-invocation.patch

BuildRequires:  zlib-devel bzip2-devel gettext ncurses-devel
BuildRequires:  autoconf automake gettext-devel libtool
BuildRequires:  doxygen flex xz-devel
BuildRequires:  perl

#Provides: perl(controllib.pl)
#Provides: perl(dpkg-gettext.pl)
#Provides: perl(file)
#Provides: perl(Debian::Debhelper::Dh_Version)
#Provides: perl(in)
#Provides: perl(extra)

%description
This package contains the tools (including dpkg-source) required
to unpack, build and upload Debian source packages.

This package also contains the programs dpkg which used to handle the
installation and removal of packages on a Debian system.

This package also contains dselect, an interface for managing the
installation and removal of packages on the system.

dpkg and dselect will certainly be non-functional on a rpm-based system
because packages dependencies will likely be unmet.

%package devel
Summary: Debian package management static library
Provides: dpkg-static = %{version}-%{release}

%description devel
This package provides the header files and static library necessary to
develop software using dpkg, the same library used internally by dpkg.

Note though, that the API is to be considered volatile, and might change
at any time, use at your own risk.


%package dev
Summary:  Debian package development tools
Requires: dpkg-perl = %{version}-%{release}
Requires: patch, make, binutils, bzip2, lzma, xz
Obsoletes: dpkg-devel < 1.16
BuildArch: noarch

%description dev
This package provides the development tools (including dpkg-source).
Required to unpack, build and upload Debian source packages

%package perl
Summary: Dpkg perl modules
Requires: dpkg = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires: perl, perl-TimeDate
BuildArch: noarch

%description perl
This package provides the perl modules used by the scripts
in dpkg-dev. They cover a wide range of functionalities. Among them
there are the following modules:
  - Dpkg::Arch: manipulate Debian architecture information
  - Dpkg::BuildOptions: parse and manipulate DEB_BUILD_OPTIONS
  - Dpkg::Changelog: parse Debian changelogs
  - Dpkg::Checksums: generate and parse checksums
  - Dpkg::Compression::Process: wrapper around compression tools
  - Dpkg::Compression::FileHandle: transparently (de)compress files
  - Dpkg::Control: parse and manipulate Debian control information
    (.dsc, .changes, Packages/Sources entries, etc.)
  - Dpkg::Deps: parse and manipulate dependencies
  - Dpkg::ErrorHandling: common error functions
  - Dpkg::Index: collections of Dpkg::Control (Packages/Sources files for
    example)
  - Dpkg::IPC: spawn sub-processes and feed/retrieve data
  - Dpkg::Substvars: substitute variables in strings
  - Dpkg::Vendor: identify current distribution vendor
  - Dpkg::Version: parse and manipulate Debian package versions

%package -n dselect
Summary:  Debian package management front-end
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description -n dselect
dselect is a high-level interface for the installation/removal of debs .


%prep
%setup -q -a2
%patch0 -p1
%patch1 -p1
%patch3 -p1

# Filter unwanted Requires:
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(Dselect::Ftp)/d' -e '/perl(extra)/d' -e '/perl(file)/d' -e '/perl(dpkg-gettext.pl)/d' -e '/perl(controllib.pl)/d' -e '/perl(in)/d'
EOF

%define __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}

 
%Build
%configure --disable-start-stop-daemon \
        --disable-linker-optimisations \
        --with-admindir=%{_localstatedir}/lib/dpkg \
        --without-selinux \
        --with-zlib \
        --with-bz2

make arch=%{_arch} \
    DEB_BUILD_GNU_TYPE=%{_arch}-linux \
    DEB_HOST_GNU_TYPE=%{_arch}-linux

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p %{buildroot}/%{pkgconfdir}/dpkg.cfg.d
mkdir -p %{buildroot}/%{pkgconfdir}/dselect.cfg.d
mkdir -p %{buildroot}/%{pkgconfdir}/origins

# Prepare "vendor" files for dpkg-vendor
cat <<EOF > %{buildroot}/%{pkgconfdir}/origins/isoft
Vendor: iSoft
Vendor-URL: http://www.isoft.com.cn/
Bugs: https://www.isoft.com.cn
EOF
ln -sf isoft %{buildroot}/%{pkgconfdir}/origins/default

# from debian/dpkg.install
install -pm0644 scripts/mk/*mk %{buildroot}/%{pkgdatadir}
install -pm0644 debian/dpkg.cfg %{buildroot}/%{pkgconfdir}
install -pm0644 debian/dselect.cfg %{buildroot}/%{pkgconfdir}
install -pm0644 debian/shlibs.default %{buildroot}/%{pkgconfdir}
install -pm0644 debian/shlibs.override %{buildroot}/%{pkgconfdir}


# patched debian/dpkg.logrotate
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
install -pm0644 debian/dpkg.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}


%find_lang dpkg
%find_lang dpkg-dev
%find_lang dselect

rm -rf $RPM_BUILD_ROOT/usr/bin/update-alternatives
rm -rf $RPM_BUILD_ROOT/usr/share/man/man1/update-alternatives.8*

pushd debhelper
# autoscripts
install -d -m 755 $RPM_BUILD_ROOT/usr/share/debhelper/autoscripts
install -m 644 autoscripts/* $RPM_BUILD_ROOT/usr/share/debhelper/autoscripts
# perl modules:
mkdir -p $RPM_BUILD_ROOT/%perl_vendorlib/Debian/Debhelper
cp -r  Debian/Debhelper/* $RPM_BUILD_ROOT/%perl_vendorlib/Debian/Debhelper
# binaries:
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 dh_*[^1-9] $RPM_BUILD_ROOT/usr/bin/
popd

#clean unused man page and translations
unused_lang="aa  ab  ae  af  am  ar  as  ay  az  ba  be  bg  bh  bi  bn  br  bs  ca  ce  ch  co  cs  cv  cy  da  de  dz  el  en_GB  eo  es  et  eu  fa  fi  fj  fo  fr  fy  ga  gd  gl  gn  gu  gv  ha  he  hi  ho  hr  hsb  hu  hy  hz  id  ie  ik  io  is  it  iu  jv  ka  ki  kl  km  kn  ks  ku  kv  kw  ky  la  lb  li  ln  lo  lt  lv  mg  mh  mi  mk  ml  mo  mr  mt  na  nb  nd  nds  ne  ng  nl  nn  nr  nso  nv  ny  oc  om  or  os  pa  pi  pl  ps  pt*  qu  rn  ro  rw  sa  sc  sd  se  sg  si  sk  sl  sm  sn  so  sq  sr*  ss  st  su  sv  sw  ta  te  tg  ti  tk  tn  to  tr  ts  tt  tw  ty  uk  ur  uz  ven  vo  wa  wo  xh  yi  yo  zu  xx ja ko ru th sr@Latn"

for i in $unused_lang;do
    rm -rf $RPM_BUILD_ROOT/usr/share/doc/HTML/$i
    rm -rf $RPM_BUILD_ROOT/usr/share/man/$i
done

rm -rf $RPM_BUILD_ROOT/usr/sbin/install-info

mkdir -p %{buildroot}%{_localstatedir}/lib/dpkg/alternatives %{buildroot}%{_localstatedir}/lib/dpkg/info \
 %{buildroot}%{_localstatedir}/lib/dpkg/parts %{buildroot}%{_localstatedir}/lib/dpkg/updates \
 %{buildroot}%{_localstatedir}/lib/dpkg/methods


rm -rf %{buildroot}%{_libdir}/*.la

%post
# from dpkg.postinst
# Create the database files if they don't already exist
create_database() {
    admindir=${DPKG_ADMINDIR:-/var/lib/dpkg}

    for file in diversions statoverride status; do
    if [ ! -f "$admindir/$file" ]; then
        touch "$admindir/$file"
    fi
    done
}

# Create log file and set default permissions if possible
create_logfile() {
    logfile=/var/log/dpkg.log
    touch $logfile
    chmod 644 $logfile
    chown root:root $logfile 2>/dev/null || chown 0:0 $logfile
}
create_database
create_logfile


%files -f dpkg.lang
%license debian/copyright
%doc debian/changelog README AUTHORS THANKS TODO
%doc doc/README.feature-removal-schedule debian/usertags debian/dpkg.cron.daily
%dir %{pkgconfdir}
%dir %{pkgconfdir}/dpkg.cfg.d
%dir %{pkgconfdir}/origins
%config(noreplace) %{pkgconfdir}/dpkg.cfg
%config(noreplace) %{pkgconfdir}/origins/*
%config(noreplace) %{_sysconfdir}/logrotate.d/dpkg
%{_bindir}/dpkg
%{_bindir}/dpkg-deb
%{_bindir}/dpkg-maintscript-helper
%{_bindir}/dpkg-query
%{_bindir}/dpkg-split
%{_bindir}/dpkg-trigger
%{_bindir}/dpkg-divert
%{_bindir}/dpkg-statoverride
%dir %{pkgdatadir}
%{pkgdatadir}/abitable
%{pkgdatadir}/cputable
%{pkgdatadir}/ostable
%{pkgdatadir}/triplettable
%{pkgdatadir}/*mk
%dir %{_localstatedir}/lib/dpkg/alternatives
%dir %{_localstatedir}/lib/dpkg/info
%dir %{_localstatedir}/lib/dpkg/parts
%dir %{_localstatedir}/lib/dpkg/updates
%{_mandir}/man1/dpkg.1.gz
%{_mandir}/man1/dpkg-deb.1.gz
%{_mandir}/man1/dpkg-maintscript-helper.1.gz
%{_mandir}/man1/dpkg-query.1.gz
%{_mandir}/man1/dpkg-split.1.gz
%{_mandir}/man1/dpkg-trigger.1.gz
%{_mandir}/man1/dpkg-divert.1.gz
%{_mandir}/man1/dpkg-statoverride.1.gz
%{_mandir}/man5/dpkg.cfg.5.gz
%{_bindir}/dh_*
%{_datadir}/debhelper/


%files devel
%{_libdir}/libdpkg.a
%{_libdir}/pkgconfig/libdpkg.pc
%{_includedir}/dpkg/*.h

%files dev -f dpkg-dev.lang
%doc AUTHORS THANKS debian/usertags doc/README.api doc/README.feature-removal-schedule doc/frontend.txt doc/triggers.txt
%config(noreplace) %{pkgconfdir}/shlibs.default
%config(noreplace) %{pkgconfdir}/shlibs.override
%{_bindir}/dpkg-architecture
%{_bindir}/dpkg-buildpackage
%{_bindir}/dpkg-buildflags
%{_bindir}/dpkg-checkbuilddeps
%{_bindir}/dpkg-distaddfile
%{_bindir}/dpkg-genchanges
%{_bindir}/dpkg-gencontrol
%{_bindir}/dpkg-gensymbols
%{_bindir}/dpkg-mergechangelogs
%{_bindir}/dpkg-name
%{_bindir}/dpkg-parsechangelog
%{_bindir}/dpkg-scanpackages
%{_bindir}/dpkg-scansources
%{_bindir}/dpkg-shlibdeps
%{_bindir}/dpkg-source
%{_bindir}/dpkg-vendor
%{_libexecdir}/dpkg/parsechangelog
%{pkgdatadir}/*.mk
%{_mandir}/man1/dpkg-architecture.1.gz
%{_mandir}/man1/dpkg-buildflags.1.gz
%{_mandir}/man1/dpkg-buildpackage.1.gz
%{_mandir}/man1/dpkg-checkbuilddeps.1.gz
%{_mandir}/man1/dpkg-distaddfile.1.gz
%{_mandir}/man1/dpkg-genchanges.1.gz
%{_mandir}/man1/dpkg-gencontrol.1.gz
%{_mandir}/man1/dpkg-gensymbols.1.gz
%{_mandir}/man1/dpkg-mergechangelogs.1.gz
%{_mandir}/man1/dpkg-name.1.gz
%{_mandir}/man1/dpkg-parsechangelog.1.gz
%{_mandir}/man1/dpkg-scanpackages.1.gz
%{_mandir}/man1/dpkg-scansources.1.gz
%{_mandir}/man1/dpkg-shlibdeps.1.gz
%{_mandir}/man1/dpkg-source.1.gz
%{_mandir}/man1/dpkg-vendor.1.gz
%{_mandir}/man5/deb-control.5.gz
%{_mandir}/man5/deb-extra-override.5.gz
%{_mandir}/man5/deb-old.5.gz
%{_mandir}/man5/deb-origin.5.gz
%{_mandir}/man5/deb-override.5.gz
%{_mandir}/man5/deb-shlibs.5.gz
%{_mandir}/man5/deb-split.5.gz
%{_mandir}/man5/deb-src-control.5.gz
%{_mandir}/man5/deb-substvars.5.gz
%{_mandir}/man5/deb-symbols.5.gz
%{_mandir}/man5/deb-triggers.5.gz
%{_mandir}/man5/deb-version.5.gz
%{_mandir}/man5/deb.5.gz

%files perl
%{perl_vendorlib}/Dpkg*
%{perl_vendorlib}/Debian*
%{_mandir}/man3/Dpkg*.3*

%files -n dselect -f dselect.lang
%doc dselect/methods/multicd/README.multicd 
%config(noreplace) %{pkgconfdir}/dselect.cfg
%{_bindir}/dselect
%{perl_vendorlib}/Dselect
%{_libdir}/dpkg/methods
%{_mandir}/man1/dselect.1.gz
%{_mandir}/man5/dselect.cfg.5.gz
%dir %{pkgconfdir}/dselect.cfg.d
%dir %{_localstatedir}/lib/dpkg/methods


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.18.1-7
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

