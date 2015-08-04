Summary: An ELF prelinking utility
Name: prelink
Version: 0.5.0
Release: 1%{?dist}
%global svnver 205
License: GPLv2+
Group: System Environment/Base
%define date 20130503
# svn export svn://sourceware.org/svn/prelink/trunk@%{svnver} prelink
# tar cf - prelink | bzip2 -9 > prelink-%{date}.tar.bz2
Source: http://people.redhat.com/jakub/prelink/prelink-%{date}.tar.bz2
Source2: prelink.conf
Source3: prelink.cron
Source4: prelink.sysconfig
Patch0: prelink-armhf-dynamic-linker.patch

BuildRequires: libelfutils-devel
BuildRequires: glibc-devel
Requires: glibc >= 2.2.4-18, coreutils, findutils
Requires: util-linux, gawk, grep
# For now
ExclusiveArch: %{ix86} alpha sparc sparcv9 sparc64 s390 s390x x86_64 ppc ppc64 %{arm}

%description
The prelink package contains a utility which modifies ELF shared libraries
and executables, so that far fewer relocations need to be resolved at runtime
and thus programs come up faster.

%prep
%setup -q -n prelink

# We have two possible dynamic linkers on ARM (soft/hard float ABI). For now,
# specifically patch the name of the linker on hard float systems. FIXME.
%ifarch armv7hl
%patch0 -p1 -b .armhfp-dynamic-linker
%endif

%build
sed -i -e '/^prelink_LDADD/s/$/ -lpthread/' src/Makefile.{am,in}
%configure --disable-shared
make %{_smp_mflags}
echo ====================TESTING=========================
make -C testsuite check-harder
make -C testsuite check-cycle
echo ====================TESTING END=====================

%install
%{makeinstall}
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sysconfdir}/{sysconfig,cron.daily,prelink.conf.d}
cp -a %{SOURCE3} %{buildroot}%{_sysconfdir}/cron.daily/prelink
cp -a %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/prelink
chmod 755 %{buildroot}%{_sysconfdir}/cron.daily/prelink
chmod 644 %{buildroot}%{_sysconfdir}/{sysconfig/prelink,prelink.conf}
cat > %{buildroot}%{_sysconfdir}/rpm/macros.prelink <<"EOF"
# rpm-4.1 verifies prelinked libraries using a prelink undo helper.
#       Note: The 2nd token is used as argv[0] and "library" is a
#       placeholder that will be deleted and replaced with the appropriate
#       library file path.
%%__prelink_undo_cmd     /usr/sbin/prelink prelink -y library
EOF
chmod 644 %{buildroot}%{_sysconfdir}/rpm/macros.prelink
mkdir -p %{buildroot}%{_mandir}/man5
echo '.so man8/prelink.8' > %{buildroot}%{_mandir}/man5/prelink.conf.5
chmod 644 %{buildroot}%{_mandir}/man5/prelink.conf.5

mkdir -p %{buildroot}/var/{lib,log}/prelink
touch %{buildroot}/var/lib/prelink/full
touch %{buildroot}/var/lib/prelink/quick
touch %{buildroot}/var/lib/prelink/force
touch %{buildroot}/var/log/prelink/prelink.log

#prelink wreaks havoc on sparc systems lets make sure its disabled by default there
%ifarch %{sparc}
sed -i -e 's|PRELINKING=yes|PRELINKING=no|g' %{buildroot}%{_sysconfdir}/sysconfig/prelink
%endif

%post
touch /var/lib/prelink/force

%files
%defattr(-,root,root)
%doc doc/prelink.pdf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/prelink.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/sysconfig/prelink
%{_sysconfdir}/rpm/macros.prelink
%dir %attr(0755,root,root) %{_sysconfdir}/prelink.conf.d
%{_sysconfdir}/cron.daily/prelink
%{_prefix}/sbin/prelink
%{_prefix}/bin/execstack
%{_mandir}/man5/prelink.conf.5*
%{_mandir}/man8/prelink.8*
%{_mandir}/man8/execstack.8*
%dir /var/lib/prelink
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/prelink/full
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/prelink/quick
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/prelink/force
%dir /var/log/prelink
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/log/prelink/prelink.log

%changelog
