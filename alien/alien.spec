Summary:        Converter between the rpm, dpkg, stampede slp, and Slackware tgz file formats
Name:           alien
Version:        8.90
Release:        5%{?dist}

Group:          Applications/System
License:        GPLv2+
URL:            http://kitenet.net/~joey/code/alien/
Source:         http://ftp.debian.org/debian/pool/main/a/alien/alien_%version.tar.gz

Requires:       dpkg, rpm-build
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(ExtUtils::MakeMaker)

BuildArch:      noarch



%description
Alien is a program that converts between the rpm, dpkg, stampede 
slp, and Slackware tgz file formats. If you want to use a package 
from another distribution than the one you have installed on your 
system, you can use alien to convert it to your preferred package 
format and install it.

%prep
%setup -qn %{name}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor VARPREFIX=%{buildroot}

make

%install
make pure_install DESTDIR=%{buildroot} \
        VARPREFIX=%{buildroot} \
        PREFIX=%{buildroot}%{_prefix}

rm -rf %{buildroot}%{perl_vendorarch}/auto/Alien

chmod 755 %{buildroot}%{_bindir}/alien

%files
%doc GPL README debian/changelog
%{_bindir}/*
%{_datadir}/%{name}
%{perl_vendorlib}/*
%{_mandir}/man?/*
%{_localstatedir}/lib/alien

%changelog
