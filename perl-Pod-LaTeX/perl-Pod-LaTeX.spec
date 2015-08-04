Name:           perl-Pod-LaTeX
Version:        0.61
Release:        296%{?dist}
Summary:        Convert POD data to formatted LaTeX
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Pod-LaTeX/
Source0:        http://www.cpan.org/authors/id/T/TJ/TJENNESS/Pod-LaTeX-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
%if 0%(perl -e 'print $] > 5.017')
BuildRequires:  perl(deprecate)
%endif
BuildRequires:  perl(if)
BuildRequires:  perl(Pod::ParseUtils) >= 0.3
BuildRequires:  perl(Pod::Select)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if 0%(perl -e 'print $] > 5.017')
Requires:       perl(deprecate)
%endif
Requires:       perl(Pod::ParseUtils) >= 0.3

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::ParseUtils\\)$

%description
Pod::LaTeX is a module to convert documentation in the POD format into
LaTeX. A pod2latex replacement command is provided.

%prep
%setup -q -n Pod-LaTeX-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc ChangeLog README
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
