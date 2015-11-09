%global hawkey_version 0.6.1
%global librepo_version 1.7.16
%global libcomps_version 0.1.6
%global rpm_version 4.12.0

%global confdir %{_sysconfdir}/dnf

%global pluginconfpath %{confdir}/plugins
%global py2pluginpath %{python_sitelib}/dnf-plugins
%global py3pluginpath %{python3_sitelib}/dnf-plugins

Name:		dnf
Version:	1.1.3
Release:	2%{?snapshot}%{?dist}
Summary:	Package manager forked from Yum, using libsolv as a dependency resolver
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:	GPLv2+ and GPLv2 and GPL
URL:		https://github.com/rpm-software-management/dnf
Source0:    https://github.com/rpm-software-management/dnf/archive/%{name}-%{version}.tar.gz
BuildArch:  noarch
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  python-bugzilla
BuildRequires:  python-sphinx
BuildRequires:  systemd
Requires:   python3-dnf = %{version}-%{release}
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
Provides:       dnf-command(autoremove)
Provides:       dnf-command(check-update)
Provides:       dnf-command(clean)
Provides:       dnf-command(distro-sync)
Provides:       dnf-command(downgrade)
Provides:       dnf-command(group)
Provides:       dnf-command(history)
Provides:       dnf-command(info)
Provides:       dnf-command(install)
Provides:       dnf-command(list)
Provides:       dnf-command(makecache)
Provides:       dnf-command(mark)
Provides:       dnf-command(provides)
Provides:       dnf-command(reinstall)
Provides:       dnf-command(remove)
Provides:       dnf-command(repolist)
Provides:       dnf-command(repository-packages)
Provides:       dnf-command(search)
Provides:       dnf-command(updateinfo)
Provides:       dnf-command(upgrade)
Provides:       dnf-command(upgrade-to)
%description
Package manager forked from Yum, using libsolv as a dependency resolver.

%package conf
Summary:    Configuration files for DNF.
%description conf
Configuration files for DNF.

%package -n dnf-yum
Conflicts:      yum < 3.4.3-505
Requires:   dnf = %{version}-%{release}
Summary:    As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF.
%description -n dnf-yum
As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF.

%package -n python-dnf
Summary:    Python 2 interface to DNF.
%{?python_provide:%python_provide python-dnf}
BuildRequires:  pygpgme
BuildRequires:  pyliblzma
BuildRequires:  python2
BuildRequires:  python-hawkey >= %{hawkey_version}
BuildRequires:  python-iniparse
BuildRequires:  python-libcomps >= %{libcomps_version}
BuildRequires:  python-librepo >= %{librepo_version}
BuildRequires:  python-nose
BuildRequires:  python-rpm >= %{rpm_version}
Recommends: bash-completion
Requires:   dnf-conf = %{version}-%{release}
Requires:   deltarpm
Requires:   pygpgme
Requires:   pyliblzma
Requires:   python-hawkey >= %{hawkey_version}
Requires:   python-iniparse
Requires:   python-libcomps >= %{libcomps_version}
Requires:   python-librepo >= %{librepo_version}
Requires:   rpm
Requires:   python-rpm >= %{rpm_version}
Obsoletes:  dnf <= 0.6.4
%description -n python-dnf
Python 2 interface to DNF.

%package -n python3-dnf
Summary:    Python 3 interface to DNF.
%{?python_provide:%python_provide python3-dnf}
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-hawkey >= %{hawkey_version}
BuildRequires:  python3-iniparse
BuildRequires:  python3-libcomps >= %{libcomps_version}
BuildRequires:  python3-librepo >= %{librepo_version}
BuildRequires:  python3-nose
BuildRequires:  python3-pygpgme
BuildRequires:  python3-rpm >= %{rpm_version}
Recommends: bash-completion
Requires:   dnf-conf = %{version}-%{release}
Requires:   deltarpm
Requires:   python3-hawkey >= %{hawkey_version}
Requires:   python3-iniparse
Requires:   python3-libcomps >= %{libcomps_version}
Requires:   python3-librepo >= %{librepo_version}
Requires:   python3-pygpgme
Requires:   rpm
Requires:   python3-rpm >= %{rpm_version}
Obsoletes:  dnf <= 0.6.4
%description -n python3-dnf
Python 3 interface to DNF.

%package automatic
Summary:    Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.
BuildRequires:  systemd
Requires:   dnf = %{version}-%{release}
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):	systemd
%description automatic
Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.

%prep
%setup -q -n dnf-%{version}
rm -rf py3
mkdir ../py3
cp -a . ../py3/
mv ../py3 ./

%build
%cmake .
make %{?_smp_mflags}
make doc-man
pushd py3
%cmake -DPYTHON_DESIRED:str=3 -DWITH_MAN=0 .
make %{?_smp_mflags}
popd

%install
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
pushd py3
make install DESTDIR=$RPM_BUILD_ROOT
popd

mkdir -p $RPM_BUILD_ROOT%{pluginconfpath}
mkdir -p $RPM_BUILD_ROOT%{py2pluginpath}
mkdir -p $RPM_BUILD_ROOT%{py3pluginpath}/__pycache__
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
mkdir -p $RPM_BUILD_ROOT%{_var}/cache/dnf
touch $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}.log
ln -sr $RPM_BUILD_ROOT%{_bindir}/dnf-3 $RPM_BUILD_ROOT%{_bindir}/dnf
mv $RPM_BUILD_ROOT%{_bindir}/dnf-automatic-3 $RPM_BUILD_ROOT%{_bindir}/dnf-automatic
rm $RPM_BUILD_ROOT%{_bindir}/dnf-automatic-2

%check
make ARGS="-V" test
pushd py3
make ARGS="-V" test
popd

%files -f %{name}.lang
%doc AUTHORS README.rst COPYING PACKAGE-LICENSING
%{_bindir}/dnf
%{_mandir}/man8/dnf.8.gz
%{_mandir}/man8/yum2dnf.8.gz
%{_unitdir}/dnf-makecache.service
%{_unitdir}/dnf-makecache.timer
%{_var}/cache/dnf

%files conf
%doc AUTHORS README.rst COPYING PACKAGE-LICENSING
%dir %{confdir}
%dir %{pluginconfpath}
%dir %{confdir}/protected.d
%config(noreplace) %{confdir}/dnf.conf
%config(noreplace) %{confdir}/protected.d/dnf.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%ghost %{_localstatedir}/%{_lib}/dnf
%ghost %{_localstatedir}/log/hawkey.log
%ghost %{_localstatedir}/log/%{name}.log
%ghost %{_localstatedir}/log/%{name}.librepo.log
%ghost %{_localstatedir}/log/%{name}.rpm.log
%ghost %{_localstatedir}/log/%{name}.plugin.log
%config %{_sysconfdir}/bash_completion.d/dnf-completion.bash
%{_mandir}/man5/dnf.conf.5.gz
%{_tmpfilesdir}/dnf.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf

%files -n dnf-yum
%doc AUTHORS README.rst COPYING PACKAGE-LICENSING
%{_bindir}/yum
%{_mandir}/man8/yum.8.gz

%files -n python-dnf
%{_bindir}/dnf-2
%doc AUTHORS README.rst COPYING PACKAGE-LICENSING
%exclude %{python_sitelib}/dnf/automatic
%{python_sitelib}/dnf/
%dir %{py2pluginpath}

%files -n python3-dnf
%doc AUTHORS README.rst COPYING PACKAGE-LICENSING
%{_bindir}/dnf-3
%exclude %{python3_sitelib}/dnf/automatic
%{python3_sitelib}/dnf/
%dir %{py3pluginpath}
%dir %{py3pluginpath}/__pycache__

%files automatic
%doc AUTHORS COPYING PACKAGE-LICENSING
%{_bindir}/dnf-automatic
%config(noreplace) %{confdir}/automatic.conf
%{_mandir}/man8/dnf.automatic.8.gz
%{_unitdir}/dnf-automatic.service
%{_unitdir}/dnf-automatic.timer
%{python3_sitelib}/dnf/automatic
%{python3_sitelib}/dnf/automatic/__pycache__/*

%post
%systemd_post dnf-makecache.timer

%preun
%systemd_preun dnf-makecache.timer

%postun
%systemd_postun_with_restart dnf-makecache.timer

%posttrans
# cleanup pre-1.0.2 style cache
for arch in armv7hl i686 x86_64 ; do
    rm -rf /var/cache/dnf/$arch
done
exit 0

%post automatic
%systemd_post dnf-automatic.timer

%preun automatic
%systemd_preun dnf-automatic.timer

%postun automatic
%systemd_postun_with_restart dnf-automatic.timer

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.1.3-2
- Rebuild with py35

