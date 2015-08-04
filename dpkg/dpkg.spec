Summary:  	    dpkg, debian package management system.	
Name:           dpkg 
Version:        1.18.1
Release:        6 
License:       	GPL
Source:         http://ftp.de.debian.org/debian/pool/main/d/dpkg/dpkg_%{version}.tar.xz
#dummy file.
Source1:		update-rc.d.c
Source2:	    http://ftp.de.debian.org/debian/pool/main/d/debhelper/debhelper_9.20150628.tar.xz


Provides: perl(controllib.pl)
Provides: perl(dpkg-gettext.pl)
Provides: perl(file)
Provides: perl(Debian::Debhelper::Dh_Version)
Provides: perl(in)
Provides: perl(extra)

%description
dpkg, debian package management system.

%prep
%setup -q -a2
 
%Build
./configure --prefix=/usr --sysconfdir=/etc --with-admindir=/var/lib/dpkg --without-selinux

make arch=%{_arch} \
    DEB_BUILD_GNU_TYPE=%{_arch}-linux \
    DEB_HOST_GNU_TYPE=%{_arch}-linux
gcc -o update-rc.d %{SOURCE1}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/sbin/update-alternatives
rm -rf $RPM_BUILD_ROOT/usr/share/man/man8/update-alternatives.8*
install -m 755 update-rc.d $RPM_BUILD_ROOT/usr/sbin


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
    rm -rf $RPM_BUILD_ROOT/usr/share/locale/$i
    rm -rf $RPM_BUILD_ROOT/usr/share/man/$i
done

rm -rf $RPM_BUILD_ROOT/usr/sbin/install-info
rpmclean
%post
cd /var/lib/dpkg
for f in available status ; do
        if [ ! -f "$f" ] ; then
                touch "$f"
        fi
done
%files
/etc
/usr
/var

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

