Name:           perl-Devel-Symdump
Version:        2.15
Release:        2%{?dist}
Epoch:          1
Summary:        A Perl module for inspecting Perl's symbol table
Group:          Development/Libraries
License:        GPL+ or Artistic
Url:            http://search.cpan.org/dist/Devel-Symdump/
Source0:        http://www.cpan.org/authors/id/A/AN/ANDK/Devel-Symdump-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(English)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Harness) >= 3.04
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
# Release Tests
%if 0%{!?perl_bootstrap:1}
# Compress::Zlib (IO-Compress) ⇒ Test::NoWarnings ⇒ Devel::StackTrace ⇒
#   Test::NoTabs ⇒ Test::Pod::Coverage ⇒ Pod::Coverage ⇒ Devel::Symdump
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Test::Pod) >= 1.00
# Test::Pod::Coverage ⇒ Pod::Coverage ⇒ Devel::Symdump
BuildRequires:  perl(Test::Pod::Coverage)
%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B)

%description
The perl module Devel::Symdump provides a convenient way to inspect
perl's symbol table and the class hierarchy within a running program.

%prep
%setup -q -n Devel-Symdump-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

# Release tests
%if 0%{!?perl_bootstrap:1}
prove t/pod.t t/podcover.t t/glob_to_local_typeglob.t :: --doit
%endif

%files
%doc Changes README
%{perl_vendorlib}/Devel/
%{_mandir}/man3/Devel::Symdump.3*

%changelog
