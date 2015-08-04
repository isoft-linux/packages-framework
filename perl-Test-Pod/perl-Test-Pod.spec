Name:           perl-Test-Pod
Version:        1.50
Release:        3%{?dist}
Summary:        Test POD files for correctness
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-Pod/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DW/DWHEELER/Test-Pod-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Build) >= 0.30
BuildRequires:  perl(Pod::Simple) >= 3.05
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester) >= 1.02
BuildRequires:  perl(Test::More) >= 0.62
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(File::Find)
Requires:       perl(File::Spec)
Requires:       perl(Pod::Simple) >= 3.05
Requires:       perl(Test::More) >= 0.62

# Remove under-specified dependcies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Simple\\)$

%description
Check POD files for errors or warnings in a test file, using Pod::Simple to do
the heavy lifting.

%prep
%setup -q -n Test-Pod-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}

%check
LC_ALL=C ./Build test

%files
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Pod.3pm*

%changelog
