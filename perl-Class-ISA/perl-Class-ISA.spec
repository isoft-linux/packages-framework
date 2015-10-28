Name:           perl-Class-ISA
Version:        0.36
Release:        1017%{?dist}
Summary:        Report the search path for a class's ISA tree
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-ISA/
Source0:        http://www.cpan.org/authors/id/S/SM/SMUELLER/Class-ISA-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This library provides functions that return the list (in order) of names of
(super-)classes Perl would search to find a method, with no duplicates.

%prep
%setup -q -n Class-ISA-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
rm -rf %{buildroot}/%{_mandir}/man3/*
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc ChangeLog README
%{perl_vendorlib}/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.36-1017
- Rebuild for new 4.0 release.

