%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


# disable broken /usr/lib/rpm/brp-python-bytecompile
%define __os_install_post %{nil}
%define compdir %(pkg-config --variable=completionsdir bash-completion)
%if "%{compdir}" == ""
%define compdir "/etc/bash_completion.d"
%endif

Summary: Creates a common metadata repository
Name: createrepo
Version: 0.10.3
Release: 3%{?dist}
License: GPLv2
Group: System Environment/Base
Source: http://createrepo.baseurl.org/download/%{name}-%{version}.tar.gz
Patch1: ten-changelog-limit.patch
Patch2: createrepo-HEAD.patch
URL: http://createrepo.baseurl.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArchitectures: noarch
Requires: python >= 2.1, python-rpm, rpm >= 4.1.1, python-libxml2
Requires: yum-metadata-parser, yum >= 3.4.3-4, python-deltarpm, deltarpm, pyliblzma
BuildRequires: python
BuildRequires: bash-completion

%description
This utility will generate a common metadata repository from a directory of rpm
packages.

%prep
%setup -q
%patch1 -p0
%patch2 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT sysconfdir=%{_sysconfdir} install

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root,-)
%doc ChangeLog README COPYING COPYING.lib
%(dirname %{compdir})
%{_datadir}/%{name}/
%{_bindir}/createrepo
%{_bindir}/modifyrepo
%{_bindir}/mergerepo
%{_mandir}/*/*
%{python_sitelib}/createrepo

%changelog
