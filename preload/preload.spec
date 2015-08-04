Name:           preload
Version:        0.6.4
Release:        12%{?dist}
Summary:        Preload is an adaptive readahead daemon
Group:          Applications/System
License:        GPLv2+
URL:            http://preload.sf.net/

Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.service

Patch0:         preload-0.6-start-late.patch

BuildRequires:  glib2-devel, help2man
Requires:       logrotate

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd


%description
preload runs as a daemon and gathers information about processes running on
the system and shared-objects that they use.  This information is saved in a
file to keep across runs of preload

%prep
%setup -q
%patch0 -p1 -b .start-late

%build
%configure
make


%install
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_docdir}/*
rm -rf %{buildroot}%{_sysconfdir}/rc.d

# systemd unit
install -Dm644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%doc README AUTHORS COPYING ChangeLog TODO THANKS NEWS doc/index.txt doc/proposal.txt
%{_sbindir}/preload
%{_datadir}/man/man8/preload.8.gz
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/preload.conf
%config(noreplace) %{_sysconfdir}/sysconfig/preload
%config(noreplace) %{_sysconfdir}/logrotate.d/preload
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/log/preload.log
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/lib/preload/preload.state
%attr(0755,root,root) %dir %{_localstatedir}/lib/preload


%changelog
