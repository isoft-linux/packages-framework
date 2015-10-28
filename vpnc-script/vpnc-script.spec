%global git_date 20140805
%global git_commit_hash df5808b

Name:		vpnc-script
Version:	%{git_date}
Release:	4.git%{git_commit_hash}%{?dist}

Summary:	Routing setup script for vpnc and openconnect
BuildArch:	noarch
Requires:	net-tools
Requires:	which

License:	GPLv2+
URL:		http://git.infradead.org/users/dwmw2/vpnc-scripts.git/
Source0:	vpnc-script

%description
This script sets up routing for VPN connectivity, when invoked by vpnc
or openconnect.


%prep
cp -p %SOURCE0 .

%build

%install
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/vpnc
install -m 0755 vpnc-script \
    %{buildroot}%{_sysconfdir}/vpnc/vpnc-script

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/vpnc
%{_sysconfdir}/vpnc/vpnc-script

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 20140805-4.gitdf5808b
- Rebuild for new 4.0 release.

