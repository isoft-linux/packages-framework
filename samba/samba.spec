%{!?python_libdir: %define python_libdir %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1,1)")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           samba
Version:        4.2.3
Release:        2 
Summary:        Server and Client software to interoperate with Windows machines
License:        GPLv3+ and LGPLv3+
Group:          System Environment/Daemons
URL:            http://www.samba.org/

Source0:        http://samba.org/samba/ftp/stable/samba-%{version}.tar.gz

Source1: samba.log
Source4: smb.conf.default
Source5: pam_winbind.conf
Source6: samba.pamd

#these two patch added by Cjacker!!!!!!!!!!!
#keep it when update!!!!!!!!!!!!!!!!!!!!!!!
Patch0: samba-disable-debug-msg.patch
Patch1: pam_smbpass-add-user-when-samba-user-didnot-exist.patch 

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Provides: samba4, samba-common, samba-libs, 

BuildRequires: autoconf
BuildRequires: cups-devel
BuildRequires: e2fsprogs-devel
BuildRequires: gawk
BuildRequires: libacl-devel
BuildRequires: libaio-devel
BuildRequires: libattr-devel
BuildRequires: libcap-devel
BuildRequires: libuuid-devel
BuildRequires: ncurses-devel
BuildRequires: pam-devel
BuildRequires: popt-devel
BuildRequires: python-devel
BuildRequires: readline-devel
BuildRequires: sed
BuildRequires: zlib-devel >= 1.2.3
#for manpage

BuildRequires: libxslt
# filter out perl requirements pulled in from examples in the docdir.
%{?filter_setup:
%filter_provides_in %{_docdir}
%filter_requires_in %{_docdir}
%filter_setup
}

%description
Samba is the standard Windows interoperability suite of programs for Linux and Unix.

%package devel
Summary: Developer tools for Samba libraries
Group: Development/Libraries
Requires: %{name}
Provides: samba4-devel

%description devel
The samba4-devel package contains the header files for the libraries
needed to develop programs that link against the SMB, RPC and other
libraries in the Samba suite.

%package -n libsmbclient
Summary: The SMB client library
Group: Applications/System
Requires: %{name}

%description -n libsmbclient
The libsmbclient contains the SMB client library from the Samba suite.

%package -n libsmbclient-devel
Summary: Developer tools for the SMB client library
Group: Development/Libraries
Requires: libsmbclient

%description -n libsmbclient-devel
The libsmbclient-devel package contains the header files and libraries needed to
develop programs that link against the SMB client library in the Samba suite.

%prep
%setup -q -n samba-%{version}
%patch0 -p1
%patch1 -p1


%build
#Why disable so many features:
#Since This samba is only provides file share service and related tools to browse shares from others 
#So winbind is useless and other advanced features such as AD/DC support is useless for a Desktop.
#Remember, this is not a server.
%configure \
        --enable-fhs \
        --with-piddir=/run \
        --with-sockets-dir=/run/samba \
        --with-modulesdir=%{_libdir}/samba \
        --with-pammodulesdir=%{_libdir}/security \
        --with-lockdir=/var/lib/samba \
        --with-cachedir=/var/lib/samba \
        --disable-gnutls \
        --disable-rpath-install \
        --with-pam \
        --without-ad-dc \
        --without-syslog \
        --without-automount \
        --without-aio-support \
        --without-dmapi \
        --without-fam \
        --without-regedit \
        --disable-glusterfs \
        --with-pam_smbpass \
        --without-ads \
        --without-ldap \
        --without-quotas \
        --enable-cups  \
        --enable-avahi \
        --without-automount  \
        --without-cluster-support \
        --without-winbind \
        --without-fam

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

install -d -m 0755 %{buildroot}/usr/{sbin,bin}
install -d -m 0755 %{buildroot}%{_libdir}/security
install -d -m 0755 %{buildroot}/var/lib/samba
install -d -m 0755 %{buildroot}/var/lib/samba/private
install -d -m 0755 %{buildroot}/var/lib/samba/winbindd_privileged
install -d -m 0755 %{buildroot}/var/lib/samba/scripts
install -d -m 0755 %{buildroot}/var/lib/samba/sysvol
install -d -m 0755 %{buildroot}/var/log/samba/old
install -d -m 0755 %{buildroot}/var/spool/samba
install -d -m 0755 %{buildroot}/var/run/samba
install -d -m 0755 %{buildroot}/var/run/winbindd
install -d -m 0755 %{buildroot}/%{_libdir}/samba
install -d -m 0755 %{buildroot}/%{_libdir}/pkgconfig


#for 'net usershare'
install -d -m 1770 %{buildroot}/var/lib/samba/usershares

# Undo the PIDL install, we want to try again with the right options.
rm -rf %{buildroot}/%{_libdir}/perl5
rm -rf %{buildroot}/%{_datadir}/perl5



# Install other stuff
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/samba

install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/samba/smb.conf

install -d -m 0755 %{buildroot}%{_sysconfdir}/security
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/security/pam_winbind.conf

install -d -m 0755 %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/pam.d/samba

echo 127.0.0.1 localhost > %{buildroot}%{_sysconfdir}/samba/lmhosts

install -m 0744 packaging/printing/smbprint %{buildroot}%{_bindir}/smbprint

install -d -m 0755 %{buildroot}%{_sysconfdir}/tmpfiles.d/
install -m644 packaging/systemd/samba.conf.tmp %{buildroot}%{_sysconfdir}/tmpfiles.d/samba.conf
# create /run/samba too.
echo "d /run/samba  755 root root" >> %{buildroot}%{_sysconfdir}/tmpfiles.d/samba.conf

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 packaging/systemd/samba.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/samba


install -d -m 0755 %{buildroot}%{_unitdir}
for i in nmb smb ; do
    install -m 0644 packaging/systemd/$i.service %{buildroot}%{_unitdir}/$i.service
done

# Clean out crap left behind by the PIDL install.
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
rm -f %{buildroot}%{perl_vendorlib}/wscript_build
rm -rf %{buildroot}%{perl_vendorlib}/Parse/Yapp

#DO NOT ship pidl and samba-python
rm -rf %{buildroot}%{perl_vendorlib}/Parse/Pidl*
rm -rf %{buildroot}%{_mandir}/man1/pidl*
rm -rf %{buildroot}%{_mandir}/man3/Parse::Pidl*
rm -rf %{buildroot}%{_bindir}/pidl
rm -rf %{buildroot}%{python_sitearch}/*

# This makes the right links, as rpmlint requires that
# the ldconfig-created links be recorded in the RPM.
/sbin/ldconfig -N -n %{buildroot}%{_libdir}

%post
/sbin/ldconfig
/usr/bin/systemd-tmpfiles --create %{_sysconfdir}/tmpfiles.d/samba.conf

if [ -d /var/cache/samba ]; then
    rm -rf /var/cache/samba/
    ln -sf /var/cache/samba /var/lib/samba/
fi

%systemd_post smb.service
%systemd_post nmb.service
systemctl enable smb ||:
systemctl enable nmb ||:
%preun
%systemd_preun smb.service
%systemd_preun nmb.service

%postun
%systemd_postun_with_restart smb.service
%systemd_postun_with_restart nmb.service

%post -n libsmbclient -p /sbin/ldconfig

%postun -n libsmbclient -p /sbin/ldconfig



%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/samba
%{_libdir}/*.so.*
%{_mandir}/*
%{_sysconfdir}/tmpfiles.d/samba.conf
%{_libdir}/security/pam_smbpass.so
%{_libdir}/security/pam_winbind.so
%{_unitdir}/nmb.service
%{_unitdir}/smb.service
%{_datadir}/samba/codepages/*

%ghost %dir /var/run/samba
%dir /var/lib/samba
%dir %{_sysconfdir}/logrotate.d/
%config(noreplace) %{_sysconfdir}/logrotate.d/samba
%attr(0700,root,root) %dir /var/log/samba
%attr(0700,root,root) %dir /var/log/samba/old

%attr(700,root,root) %dir /var/lib/samba/private
%attr(755,root,root) %dir %{_sysconfdir}/samba
%config(noreplace) %{_sysconfdir}/samba/smb.conf
%config(noreplace) %{_sysconfdir}/samba/lmhosts
%config(noreplace) %{_sysconfdir}/sysconfig/samba

%dir /var/lib/samba/sysvol

%{_sysconfdir}/pam.d/samba
%config(noreplace) %{_sysconfdir}/security/pam_winbind.conf

%attr(1770,root,wheel) %dir /var/lib/samba/usershares

%exclude %{_libdir}/libsmbclient.so.*
%exclude %{_libdir}/libsmbsharemodes.so.*
%exclude %{_mandir}/man7/libsmbclient.7*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/samba-4.0
%{_includedir}/samba-4.0/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
#for libsmbclient-devel
%exclude %{_includedir}/samba-4.0/libsmbclient.h
%exclude %{_includedir}/samba-4.0/smb_share_modes.h
%exclude %{_libdir}/libsmbclient.so
%exclude %{_libdir}/libsmbsharemodes.so
%exclude %{_libdir}/pkgconfig/smbclient.pc
%exclude %{_libdir}/pkgconfig/smbsharemodes.pc

%files -n libsmbclient
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/libsmbclient.so.*

%files -n libsmbclient-devel
%defattr(-,root,root)
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir}/libsmbclient.so
%{_libdir}/pkgconfig/smbclient.pc
%{_mandir}/man7/libsmbclient.7*


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

