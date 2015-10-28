Summary:    Non-interactive SSH authentication utility
Name:       sshpass
Version:    1.05
Release:    9%{?dist}
License:    GPLv2
Url:        http://sshpass.sourceforge.net/
Source0:    http://downloads.sourceforge.net/sshpass/sshpass-%{version}.tar.gz

%description
Tool for non-interactively performing password authentication with so called
"interactive keyboard password authentication" of SSH. Most users should use
more secure public key authentication of SSH instead.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%{_bindir}/sshpass
%{_datadir}/man/man1/sshpass.1.gz
%doc AUTHORS COPYING ChangeLog NEWS

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.05-9
- Rebuild for new 4.0 release.

