%{?!with_python:      %global with_python      1}
%{?!with_python3:     %global with_python3     1}
%{?!with_munin:       %global with_munin       0}

%if 0%{with_python} == 0
# if not building Python, don't build Python3
%global with_python3 0
%else # with_python
# needed just for EPEL
%if 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif # rhel <= 6
%endif # with_python

%global _hardened_build 1

#global extra_version rc1

Summary: Validating, recursive, and caching DNS(SEC) resolver
Name: unbound
Version: 1.5.4
Release: 4%{?extra_version:.%{extra_version}}%{?dist}
License: BSD
Url: http://www.nlnetlabs.nl/unbound/
Source: http://www.unbound.net/downloads/%{name}-%{version}%{?extra_version}.tar.gz
Source1: unbound.service
Source2: unbound.conf
Source3: unbound.munin
Source4: unbound_munin_
Source5: root.key
Source6: dlv.isc.org.key
Source7: unbound-keygen.service
Source8: tmpfiles-unbound.conf
Source9: example.com.key
Source10: example.com.conf
Source11: block-example.com.conf
# From http://data.iana.org/root-anchors/icannbundle.pem
Source12: icannbundle.pem
Source13: root.anchor
Source14: unbound.sysconfig
Source15: unbound-anchor.timer
Source16: unbound-munin.README
Source17: unbound-anchor.service

BuildRequires: flex, openssl-devel
BuildRequires: libevent-devel expat-devel
%if 0%{with_python}
BuildRequires: python2-devel swig
%endif # with_python
%if 0%{with_python3}
BuildRequires: python3-devel
%endif # with_python3
BuildRequires: systemd
# Required for SVN versions
# BuildRequires: bison
# BuildRequires: automake autoconf libtool

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# Needed because /usr/sbin/unbound links unbound libs staticly
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
Unbound is a validating, recursive, and caching DNS(SEC) resolver.

The C implementation of Unbound is developed and maintained by NLnet
Labs. It is based on ideas and algorithms taken from a java prototype
developed by Verisign labs, Nominet, Kirei and ep.net.

Unbound is designed as a set of modular components, so that also
DNSSEC (secure DNS) validation and stub-resolvers (that do not run
as a server, but are linked into an application) are easily possible.

%if %{with_munin}
%package munin
Summary: Plugin for the munin / munin-node monitoring package
Requires: munin-node
Requires: %{name} = %{version}-%{release}, bc
BuildArch: noarch

%description munin
Plugin for the munin / munin-node monitoring package
%endif

%package devel
Summary: Development package that includes the unbound header files
Requires: %{name}-libs%{?_isa} = %{version}-%{release}, openssl-devel

%description devel
The devel package contains the unbound library and the include files

%package libs
Summary: Libraries used by the unbound server and client applications
Requires(post): /sbin/ldconfig
Requires(post): systemd
Requires(postun): /sbin/ldconfig
Requires(postun): systemd
Requires(preun): systemd
Requires(pre): shadow-utils
Requires: openssl >= 0.9.8g-12

%description libs
Contains libraries used by the unbound server and client applications

%if 0%{with_python}
%package -n python-unbound
Summary: Python 2 modules and extensions for unbound
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: unbound-python = %{version}-%{release}
Obsoletes: unbound-python < %{version}-%{release}

%description -n python-unbound
Python 2 modules and extensions for unbound
%endif # with_python

%if 0%{with_python3}
%package -n python3-unbound
Summary: Python 3 modules and extensions for unbound
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description -n python3-unbound
Python 3 modules and extensions for unbound
%endif # with_python3


%prep
%{?extra_version:%global pkgname %{name}-%{version}%{extra_version}}%{!?extra_version:%global pkgname %{name}-%{version}}
%setup -qcn %{pkgname}

%if 0%{with_python}
mv %{pkgname} %{pkgname}_python2
pushd %{pkgname}_python2
%endif # with_python

#Add patches here

# only for snapshots
# autoreconf -iv

%if 0%{with_python}
# copy common doc files - after here, since it may be patched
cp -pr doc pythonmod libunbound ../
popd
%endif # with_python

%if 0%{?with_python3}
cp -a %{pkgname}_python2 %{pkgname}_python3
%endif # with_python3


%build
# This is needed to rebuild the configure script to support Python 3.x
# autoreconf -iv
export CFLAGS="$RPM_OPT_FLAGS -fPIE -pie"
export CXXFLAGS="$RPM_OPT_FLAGS -fPIE -pie"

# ./configure script common arguments
%global configure_args --with-libevent --with-pthreads --with-ssl \\\
            --disable-rpath --disable-static \\\
            --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \\\
            --with-pidfile=%{_localstatedir}/run/%{name}/%{name}.pid \\\
            --enable-sha2 --disable-gost --enable-ecdsa \\\
            --with-rootkey-file=%{_sharedstatedir}/unbound/root.key

%if 0%{with_python}
pushd %{pkgname}_python2
%endif # with_python

%configure  \
%if %{with_python}
            --with-pythonmodule --with-pyunbound PYTHON=%{__python2} \
%endif # with_python
            %{configure_args}

%{__make} %{?_smp_mflags}
%{__make} %{?_smp_mflags} streamtcp

%if 0%{with_python}
popd
%endif # with_python

%if 0%{with_python3}
pushd %{pkgname}_python3
%configure  \
            --with-pythonmodule --with-pyunbound PYTHON=%{__python3} \
            %{configure_args}

%{__make} %{?_smp_mflags}
popd
%endif # with_python3


%install
%if 0%{with_python3}
pushd %{pkgname}_python3
%{__make} DESTDIR=%{buildroot} install
popd
%endif # with_python3

%if 0%{with_python}
pushd %{pkgname}_python2
%endif # with_python
%{__make} DESTDIR=%{buildroot} install
%if 0%{with_python}
popd
%endif # with_python

install -d -m 0755 %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/unbound.service
install -p -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/unbound-keygen.service
install -p -m 0644 %{SOURCE15} %{buildroot}%{_unitdir}/unbound-anchor.timer
install -p -m 0644 %{SOURCE17} %{buildroot}%{_unitdir}/unbound-anchor.service
install -p -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/unbound
install -p -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/unbound
install -p -m 0644 %{SOURCE14} %{buildroot}%{_sysconfdir}/sysconfig/unbound
install -p -m 0644 %{SOURCE16} .
%if %{with_munin}
# Install munin plugin and its softlinks
install -d -m 0755 %{buildroot}%{_sysconfdir}/munin/plugin-conf.d
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/munin/plugin-conf.d/unbound
install -d -m 0755 %{buildroot}%{_datadir}/munin/plugins/
install -p -m 0755 %{SOURCE4} %{buildroot}%{_datadir}/munin/plugins/unbound
for plugin in unbound_munin_hits unbound_munin_queue unbound_munin_memory unbound_munin_by_type unbound_munin_by_class unbound_munin_by_opcode unbound_munin_by_rcode unbound_munin_by_flags unbound_munin_histogram; do
    ln -s unbound %{buildroot}%{_datadir}/munin/plugins/$plugin
done
%endif

%if 0%{with_python}
pushd %{pkgname}_python2
%endif # with_python

# install streamtcp used for monitoring / debugging unbound's port 80/443 modes
install -m 0755 streamtcp %{buildroot}%{_sbindir}/unbound-streamtcp
# install streamtcp man page
install -m 0644 testcode/streamtcp.1 %{buildroot}/%{_mandir}/man1/unbound-streamtcp.1

%if 0%{with_python}
popd
%endif # with_python

# Install tmpfiles.d config
install -d -m 0755 %{buildroot}%{_tmpfilesdir} %{buildroot}%{_sharedstatedir}/unbound
install -m 0644 %{SOURCE8} %{buildroot}%{_tmpfilesdir}/unbound.conf

# install root and DLV key - we keep a copy of the root key in old location,
# in case user has changed the configuration and we wouldn't update it there
install -m 0644 %{SOURCE5} %{SOURCE6} %{buildroot}%{_sysconfdir}/unbound/
install -m 0644 %{SOURCE13} %{buildroot}%{_sharedstatedir}/unbound/root.key

# remove static library from install (fedora packaging guidelines)
rm %{buildroot}%{_libdir}/*.la

%if 0%{with_python}
rm %{buildroot}%{python2_sitearch}/*.la
%endif # with_python

%if 0%{with_python3}
rm %{buildroot}%{python3_sitearch}/*.la
%endif # with_python3

# create softlink for all functions of libunbound man pages
for mpage in ub_ctx ub_result ub_ctx_create ub_ctx_delete ub_ctx_set_option ub_ctx_get_option ub_ctx_config ub_ctx_set_fwd ub_ctx_resolvconf ub_ctx_hosts ub_ctx_add_ta ub_ctx_add_ta_file ub_ctx_trustedkeys ub_ctx_debugout ub_ctx_debuglevel ub_ctx_async ub_poll ub_wait ub_fd ub_process ub_resolve ub_resolve_async ub_cancel ub_resolve_free ub_strerror ub_ctx_print_local_zones ub_ctx_zone_add ub_ctx_zone_remove ub_ctx_data_add ub_ctx_data_remove;
do
  echo ".so man3/libunbound.3" > %{buildroot}%{_mandir}/man3/$mpage ;
done

mkdir -p %{buildroot}%{_localstatedir}/run/unbound

# Install directories for easier config file drop in

mkdir -p %{buildroot}%{_sysconfdir}/unbound/{keys.d,conf.d,local.d}
install -p %{SOURCE9} %{buildroot}%{_sysconfdir}/unbound/keys.d/
install -p %{SOURCE10} %{buildroot}%{_sysconfdir}/unbound/conf.d/
install -p %{SOURCE11} %{buildroot}%{_sysconfdir}/unbound/local.d/

# Link unbound-control-setup.8 manpage to unbound-control.8
echo ".so man8/unbound-control.8" > %{buildroot}/%{_mandir}/man8/unbound-control-setup.8


%pre libs
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || \
useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin \
-c "Unbound DNS resolver" unbound

%post
%systemd_post unbound.service
%systemd_post unbound-keygen.service

%post libs
/sbin/ldconfig
%{_sbindir}/runuser  --command="%{_sbindir}/unbound-anchor -a %{_sharedstatedir}/unbound/root.key -c %{_sysconfdir}/unbound/icannbundle.pem"  --shell /bin/sh unbound ||:
%systemd_post unbound-anchor.timer
# start the timer only if installing the package to prevent starting it, if it was stopped on purpose
if [ "$1" -eq 1 ]; then
    # the Unit is in presets, but would be started after reboot
    /bin/systemctl start unbound-anchor.timer >/dev/null 2>&1 || :
fi

%preun
%systemd_preun unbound.service
%systemd_preun unbound-keygen.service

%preun libs
%systemd_preun unbound-anchor.timer

%postun
%systemd_postun_with_restart unbound.service
%systemd_postun unbound-keygen.service

%postun libs
/sbin/ldconfig
%systemd_postun_with_restart unbound-anchor.timer

%triggerun -- unbound < 1.4.12-4
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply unbound
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save unbound >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del unbound >/dev/null 2>&1 || :
/bin/systemctl try-restart unbound.service >/dev/null 2>&1 || :
/bin/systemctl try-restart unbound-keygen.service >/dev/null 2>&1 || :


%check
%if 0%{with_python}
pushd %{pkgname}_python2

#pushd pythonmod
#make test
#popd
%endif # with_python

make check

%if 0%{with_python}
popd
%endif # with_python

%if 0%{with_python3}
pushd %{pkgname}_python3
#pushd pythonmod
#make test
#popd
make check
popd
%endif # with_python3


%files 
%doc doc/CREDITS doc/FEATURES
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-keygen.service
%attr(0755,unbound,unbound) %dir %{_localstatedir}/run/%{name}
%attr(0644,root,root) %{_tmpfilesdir}/unbound.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/unbound.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %attr(0755,root,unbound) %{_sysconfdir}/%{name}/keys.d
%attr(0664,root,unbound) %config(noreplace) %{_sysconfdir}/%{name}/keys.d/*.key
%dir %attr(0755,root,unbound) %{_sysconfdir}/%{name}/conf.d
%attr(0664,root,unbound) %config(noreplace) %{_sysconfdir}/%{name}/conf.d/*.conf
%dir %attr(0755,root,unbound) %{_sysconfdir}/%{name}/local.d
%attr(0664,root,unbound) %config(noreplace) %{_sysconfdir}/%{name}/local.d/*.conf
%{_sbindir}/unbound
%{_sbindir}/unbound-checkconf
%{_sbindir}/unbound-control
%{_sbindir}/unbound-control-setup
%{_sbindir}/unbound-host
%{_sbindir}/unbound-streamtcp
%{_mandir}/man1/*
%{_mandir}/man5/*
%exclude %{_mandir}/man8/unbound-anchor*
%{_mandir}/man8/*

%if 0%{with_python}
%files -n python-unbound
%license pythonmod/LICENSE
%{python2_sitearch}/*
%doc libunbound/python/examples/*
%doc pythonmod/examples/*
%endif

%if 0%{with_python3}
%files -n python3-unbound
%license pythonmod/LICENSE
%{python3_sitearch}/*
%doc libunbound/python/examples/*
%doc pythonmod/examples/*
%endif

%if 0%{with_munin}
%files munin
%doc unbound-munin.README
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/unbound
%{_datadir}/munin/plugins/unbound*
%endif

%files devel
%{_libdir}/libunbound.so
%{_includedir}/unbound.h
%{_mandir}/man3/*

%files libs
%doc doc/README
%license doc/LICENSE
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}
%{_sbindir}/unbound-anchor
%{_libdir}/libunbound.so.*
%{_mandir}/man8/unbound-anchor*
%{_sysconfdir}/%{name}/icannbundle.pem
%{_unitdir}/unbound-anchor.timer
%{_unitdir}/unbound-anchor.service
%dir %attr(0755,unbound,unbound) %{_sharedstatedir}/%{name}
%attr(0644,unbound,unbound) %config(noreplace) %{_sharedstatedir}/%{name}/root.key
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/dlv.isc.org.key
# just left for backwards compat with user changed unbound.conf files - format is different!
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/root.key


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.5.4-4
- Rebuild for new 4.0 release.

