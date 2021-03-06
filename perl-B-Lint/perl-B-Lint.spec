Name:           perl-B-Lint
Version:        1.20
Release:        6%{?dist}
Summary:        Perl lint
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/B-Lint/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/B-Lint-%{version}.tar.gz
# Work around for Perl 5.22, bug #1231112, CPAN RT#101115
Patch0:         B-Lint-1.20-Skip-a-bare-sub-test.patch
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  sed
# Run-Time:
BuildRequires:  perl(B) 
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
%if 0%(perl -e 'print $] > 5.017')
BuildRequires:  perl(deprecate)
%endif
BuildRequires:  perl(if)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(O)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(constant)
%if 0%(perl -e 'print $] > 5.017')
Requires:       perl(deprecate)
%endif

%description
The B::Lint module is equivalent to an extended version of the -w option of
perl. It is named after the program lint which carries out a similar process
for C programs.

%prep
%setup -q -n B-Lint-%{version}
%patch0 -p1
# Install into architecture-agnostic path, CPAN RT#83049
sed -i '/PM *=>/,/}/d' Makefile.PL

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.20-6
- Rebuild for new 4.0 release.

