%global use_nss 1
%global mailrc %{_sysconfdir}/mail.rc
Summary: Enhanced implementation of the mailx command
Name: mailx
Version: 12.5
Release: 12 
# MPLv1.1 .. nss.c, nsserr.c
License: BSD with advertising and MPLv1.1
URL: http://heirloom.sourceforge.net/mailx.html
# Mailx's upstream provides only the CVS method of downloading source code.
# Use get-upstream-tarball.sh script to download current version of mailx.
Source0: mailx-%{version}.tar.xz
Source1: get-upstream-tarball.sh

Patch0: nail-11.25-config.patch
Patch1: mailx-12.3-pager.patch
Patch2: mailx-12.5-lzw.patch
# resolves: #805410
Patch3: mailx-12.5-fname-null.patch
# resolves: #857120
Patch4: mailx-12.5-collect.patch
# resolves: #948869
Patch5: mailx-12.5-usage.patch

%if %{use_nss}
BuildRequires: nss-devel, pkgconfig, krb5-devel
%else
BuildRequires: openssl-devel
%endif

Obsoletes: nail < %{version}
Provides: nail = %{version}


%description
Mailx is an enhanced mail command, which provides the functionality
of the POSIX mailx command, as well as SysV mail and Berkeley Mail
(from which it is derived).

Additionally to the POSIX features, mailx can work with Maildir/ e-mail
storage format (as well as mailboxes), supports IMAP, POP3 and SMTP
protocols (including over SSL) to operate with remote hosts, handles mime
types and different charsets. There are a lot of other useful features,
see mailx(1).

And as its ancient analogues, mailx can be used as a mail script language,
both for sending and receiving mail.

Besides the "mailx" command, this package provides "mail" and "Mail"
(which should be compatible with its predecessors from the mailx-8.x source),
as well as "nail" (the initial name of this project).


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
sed -i 's,/etc/nail.rc,%{mailrc},g' mailx.1


%build
%if %{use_nss}
INCLUDES="$INCLUDES `pkg-config --cflags-only-I nss`"
export INCLUDES
%endif

echo    PREFIX=%{_prefix} \
    BINDIR=/bin \
    MANDIR=%{_mandir} \
    SYSCONFDIR=%{_sysconfdir} \
    MAILRC=%{mailrc} \
    MAILSPOOL=%{_localstatedir}/mail \
    SENDMAIL=%{_sbindir}/sendmail \
    UCBINSTALL=install \
> makeflags

#  %{?_smp_mflags} cannot be used here
make `cat makeflags` \
    CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64" \
    IPv6=-DHAVE_IPv6_FUNCS


%install
make DESTDIR=$RPM_BUILD_ROOT STRIP=: `cat makeflags` install

ln -s mailx $RPM_BUILD_ROOT/bin/mail

install -d $RPM_BUILD_ROOT%{_bindir}
pref=`echo %{_bindir} | sed 's,/[^/]*,../,g'`

pushd $RPM_BUILD_ROOT%{_bindir}
ln -s ${pref}bin/mailx Mail
ln -s ${pref}bin/mailx nail
popd

pushd $RPM_BUILD_ROOT%{_mandir}/man1
ln -s mailx.1 mail.1
ln -s mailx.1 Mail.1
ln -s mailx.1 nail.1
popd


%triggerpostun -- mailx < 12
[[ -f %{mailrc}.rpmnew ]] && {
    # old config was changed. Merge both together.
    ( echo '# The settings above was inherited from the old mailx-8.x config'
      echo
      cat %{mailrc}.rpmnew
    ) >>%{mailrc}
} || :


%triggerpostun -- nail <= 12.3
[[ -f %{_sysconfdir}/nail.rc.rpmsave ]] && {
    # old config was changed...
    save=%{mailrc}.rpmnew
    [[ -f $save ]] && save=%{mailrc}.rpmsave

    mv -f %{mailrc} $save
    mv -f %{_sysconfdir}/nail.rc.rpmsave %{mailrc}
} || :


%files
%doc COPYING AUTHORS README
%config(noreplace) %{mailrc}
/bin/*
%{_bindir}/*
%{_mandir}/*/*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 12.5-12
- Rebuild for new 4.0 release.

