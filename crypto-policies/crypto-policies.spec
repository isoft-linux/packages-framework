%global git_date 20151005
%global git_commit_hash c8452f8
%global aname crypto-policies

Name:           crypto-policies
Version:        %{git_date}
Release:        2.git%{git_commit_hash}%{?dist}
Summary:        Crypto policies package for Fedora

License:        LGPLv2+
URL:            https://github.com/nmav/fedora-crypto-policies

# This is a tarball of the git repository without the .git/
# directory.
Source0:        crypto-policies-git%{git_commit_hash}.tar.gz
Source1:	config

BuildArch: noarch
BuildRequires: asciidoc
BuildRequires: libxslt
BuildRequires: openssl
BuildRequires: gnutls-utils
BuildRequires: docbook-style-xsl
# for shell script
Requires(post): coreutils

%description
This package provides update-crypto-policies, which is a tool that sets
the policy applicable for the various cryptographic back-ends, such as
SSL/TLS libraries. The policy set by the tool will be the default policy
used by these back-ends unless the application user configures them otherwise.


%prep
%setup -q -n %{aname}

%build
make %{?_smp_mflags} update-crypto-policies.8

%install
mkdir -p -m 755 %{buildroot}%{_datadir}/crypto-policies/profiles
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/
mkdir -p -m 755 %{buildroot}%{_mandir}/man8
mkdir -p -m 755 %{buildroot}%{_bindir}
install -p -m 644 update-crypto-policies.8 %{buildroot}%{_mandir}/man8
install -p -m 755 update-crypto-policies %{buildroot}%{_bindir}/update-crypto-policies
install -p -m 644 profiles/* %{buildroot}%{_datadir}/crypto-policies/profiles
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/crypto-policies/config

%check
make check %{?_smp_mflags}

%post
%{_bindir}/update-crypto-policies --no-check


%files
%defattr(-,root,root,-)

%dir %{_sysconfdir}/crypto-policies/
%config(noreplace) %{_sysconfdir}/crypto-policies/config

%dir %{_datadir}/crypto-policies/
%{_bindir}/update-crypto-policies
%{_mandir}/man8/update-crypto-policies.8.gz
%{_datadir}/crypto-policies/profiles/

%{!?_licensedir:%global license %%doc}
%license COPYING.LESSER

%changelog
* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 20151005-2.gitc8452f8
- Remove patch0, we change asciidoc path instead

