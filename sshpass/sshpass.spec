Summary:    Non-interactive SSH authentication utility
Name:       sshpass
Version:    1.05
Release:    8%{?dist}
License:    GPLv2
Group:      Applications/Internet
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
