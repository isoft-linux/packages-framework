%global WITH_SELINUX 0 

%global ALTERNATIVES %{_sbindir}/alternatives

Summary:  An archiving tool with ACL support
Name: star
Version: 1.5.3
Release: 6
License: CDDL
URL: http://freecode.com/projects/star
Source: http://downloads.sourceforge.net/s-tar/%{name}-%{version}.tar.bz2

# do not segfault with data-change-warn option (#255261)
Patch2: star-1.5-changewarnSegv.patch

# Prevent buffer overflow for filenames with length of 100 characters (#556664)
Patch3: star-1.5.2-bufferoverflow.patch

# Fix some invalid manpage references (#624612)
Patch4: star-1.5.1-manpagereferences.patch

# note that the H=crc format uses Sum32 algorithm, not CRC
Patch6: star-1.5.1-crc.patch

# Allow rmt to access all files.
# ~> downstream
# ~> #968980
Patch8: star-1.5.2-rmt-rh-access.patch

# Use ssh rather than rsh by default
# ~> downstream
# ~> related to #968980
Patch9: star-1.5.2-use-ssh-by-default.patch

# Fix broken star.mk in 1.5.3 (included from all.mk)
Patch10: star-1.5.3-star-mk.patch

# Fix segfault for 'pax -X' (rhbz#1175009)
# ~> downstream
Patch11: star-1.5.3-pax-X-option.patch

BuildRequires: libattr-devel libacl-devel libtool
BuildRequires: e2fsprogs-devel

%description
Star saves many files together into a single tape or disk archive,
and can restore individual files from the archive. Star supports ACL.

%package -n     spax
Summary:        Portable archive exchange
Requires(post):  %{ALTERNATIVES}
Requires(preun): %{ALTERNATIVES}


%description -n spax
The pax utility shall read and write archives, write lists of the members of
archive files and copy directory hierarchies as is defined in IEEE Std 1003.1.

%package -n     scpio
Summary:        Copy file archives in and out (LEGACY)

%description -n scpio
The scpio utility, depending on the options used: copies files to an archive
file, extracts files from an archive file, lists files from an archive file or
copies files from one directory tree to another.

%package -n     rmt
Summary: Provides certain programs with access to remote tape devices
# we need to be greater than the version from 'dump' package
Epoch: 2

%description -n rmt
The rmt utility provides remote access to tape devices for programs
like dump (a filesystem backup program), restore (a program for
restoring files from a backup), and tar (an archiving program).

# "desired" alternative constants
%global ALT_NAME                pax
%global ALT_LINK                %{_bindir}/pax
%global ALT_SL1_NAME            pax-man
%global ALT_SL1_LINK            %{_mandir}/man1/pax.1.gz

# "local" alternative constants
%global ALT_PATH                %{_bindir}/spax
%global ALT_SL1_PATH            %{_mandir}/man1/spax.1.gz

%prep
%setup -q
%patch2 -p1 -b .changewarnSegv
%patch3 -p1 -b .namesoverflow
%patch4 -p1 -b .references
%patch6 -p1 -b .crc
%patch8 -p1 -b .rmt-access-rules
%patch9 -p1 -b .ssh-by-default
%patch10 -p1 -b .bug-config-1.5.3
%patch11 -p1 -b .pax-X

# disable single "fat" binary
cp -a star/all.mk star/Makefile

star_recode()
{
    for i in $@; do
        iconv -f iso_8859-1 -t utf-8 $i > .tmp_file
        mv .tmp_file $i
    done
}

star_recode AN-1.5 AN-1.5.2 star/star.4

for PLAT in %{arm} %{power64} aarch64 x86_64 s390 s390x sh3 sh4 sh4a sparcv9; do
    for AFILE in gcc cc; do
            [ ! -e RULES/${PLAT}-linux-${AFILE}.rul ] \
            && ln -s i586-linux-${AFILE}.rul RULES/${PLAT}-linux-${AFILE}.rul
    done
done

%build
# This is config/work-around for atypical build system.  Variables used are
# docummented makefiles.5.  GMAKE_NOWARN silences irritating warnings in
# GNU/Linux ecosystem.
%global make_flags GMAKE_NOWARN=true                                    \\\
    RUNPATH=                                                            \\\
    LDPATH=                                                             \\\
    PARCH=%{_target_cpu}                                                \\\
    K_ARCH=%{_target_cpu}                                               \\\
    INS_BASE=$RPM_BUILD_ROOT%{_prefix}                                  \\\
    INS_RBASE=$RPM_BUILD_ROOT                                           \\\
    INSTALL='sh $(SRCROOT)/conf/install-sh -c -m $(INSMODEINS)'         \\\
    COPTX="$RPM_OPT_FLAGS -DTRY_EXT2_FS"                                \\\
    DEFCCOM=gcc

# Note: disable optimalisation by COPTX='-g3 -O0' LDOPTX='-g3 -O0'
make %{?_smp_mflags} %make_flags

%install
make install -s %make_flags

ln -s star.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/ustar.1
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
ln -s %{_sbindir}/rmt ${RPM_BUILD_ROOT}%{_sysconfdir}/rmt

# XXX Nuke unpackaged files.
( cd ${RPM_BUILD_ROOT}
  rm -f .%{_bindir}/mt
  rm -f .%{_bindir}/smt
  rm -f .%{_bindir}/tartest
  rm -f .%{_bindir}/tar
  rm -f .%{_bindir}/gnutar
  rm -f .%{_bindir}/star_fat
  rm -f .%{_bindir}/star_sym
  rm -f .%{_bindir}/suntar
  rm -f .%{_sysconfdir}/default/star
  rm -rf .%{_prefix}%{_sysconfdir}
  rm -rf .%{_prefix}/include
  rm -rf .%{_prefix}/lib # hard-wired intently
  rm -rf .%{_mandir}/man3
  rm -rf .%{_mandir}/man5/{makefiles,makerules}.5*
  rm -rf .%{_mandir}/man1/{tartest,gnutar,smt,mt,suntar,match}.1*
  rm -rf .%{_docdir}/star/testscripts
  rm -rf .%{_docdir}/star/TODO
  rm -rf .%{_docdir}/rmt
)

%clean

%post -n spax
%{ALTERNATIVES} \
    --install   %{ALT_LINK}     %{ALT_NAME}     %{ALT_PATH}     66 \
    --slave     %{ALT_SL1_LINK} %{ALT_SL1_NAME} %{ALT_SL1_PATH}

%preun -n spax
if [ $1 -eq 0 ]; then
    # only on pure uninstall (not upgrade)
    %{ALTERNATIVES} --remove %{ALT_NAME} %{ALT_PATH}
fi

%files
%{_bindir}/star
%{_bindir}/ustar
%{_mandir}/man1/star.1*
%{_mandir}/man1/ustar.1*
%{_mandir}/man5/star.5*

%files -n scpio
%doc %{_mandir}/man1/scpio.1*
%{_bindir}/scpio

%files -n spax
%doc %{_mandir}/man1/spax.1*
%{_bindir}/spax
%ghost %verify(not md5 size mode mtime) %{ALT_LINK}
%ghost %verify(not md5 size mode mtime) %{ALT_SL1_LINK}

%files -n rmt
%{_sbindir}/rmt
%{_mandir}/man1/rmt.1*
%config %{_sysconfdir}/default/rmt
# This symlink is used by cpio, star, spax, scpio, .. thus it is needed.  Even
# if the cpio may be configured to use /sbin/rmt rather than /etc/rmt, star (and
# thus spax, ..) has the lookup path hardcoded to '/etc/rmt' (it means that even
# non rpm based systems will try to look for /etc/rmt).  And - the conclusion is
# - it does not make sense to fight against /etc/rmt symlink ATM (year 2013).
%{_sysconfdir}/rmt

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.5.3-6
- Rebuild for new 4.0 release.

