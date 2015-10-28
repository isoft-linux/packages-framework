Name:           perl-Config-IniFiles
Version:        2.88
Release:        2%{?dist}
Summary:        A module for reading .ini-style configuration files
# LICENSE:                              GPL+ or Artistic
# lib/Config/IniFiles.pm:               GPL+ or Artistic
## Not distributed in a binary package
# t/30parameters-with-empty-values.t:   MIT
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Config-IniFiles/
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/Config-IniFiles-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Build) >= 0.36
# Module::Build::Compat not used, we run Build.PL
BuildRequires:  perl(strict)
# Test::Run::CmdLine::Iface not used
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Scalar) >= 2.109
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(Symbol)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(English)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.14
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Not autodetected. Found in lib/Config/IniFiles.pm:2761
Requires:       perl(IO::Scalar) >= 2.109
# Also not autodetected
Requires:       perl(List::Util) >= 1.33

# Filter under-specified requires
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(List::MoreUtils\\)$

%description
Config::IniFiles provides a way to have readable configuration files
outside your Perl script. Configurations can be imported (inherited,
stacked,...), sections can be grouped, and settings can be accessed
from a tied hash.

%prep
%setup -q -n Config-IniFiles-%{version}
# Normalize end-of-lines
sed -i -e 's/\r$//' Changes OLD-Changes.txt

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%license LICENSE
%doc Changes OLD-Changes.txt README
%{perl_vendorlib}/Config/
%{_mandir}/man3/*.3pm*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.88-2
- Rebuild for new 4.0 release.

