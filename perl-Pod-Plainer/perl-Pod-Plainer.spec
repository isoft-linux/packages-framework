Name: perl-Pod-Plainer
Version: 1.03
Release: 11%{?dist}
Summary: Perl extension for converting Pod to old-style Pod

License: GPL+ or Artistic
URL: http://search.cpan.org/dist/Pod-Plainer/

Source0: http://search.cpan.org/CPAN/authors/id/R/RM/RMBARKER/Pod-Plainer-%{version}.tar.gz

BuildArch: noarch
# Correct for lots of packages, other common choices include eg. Module::Build
BuildRequires: perl(ExtUtils::MakeMaker), perl(Pod::Parser), perl(Test::More), perl(Test::Pod::Coverage) >= 1.00
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Pod::Plainer uses Pod::Parser which takes Pod with the (new) 'C<< .. >>'
constructs and returns the old(er) style with just 'C<>'; '<' and '>' are
replaced by 'E<lt>' and 'E<gt>'.
This can be used to pre-process Pod before using tools which do not
recognize the new style Pods.

%prep
%setup -q -n Pod-Plainer-%{version}

%build
# Remove OPTIMIZE=... from noarch packages (unneeded)
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
#rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
# Remove the next line from noarch packages (unneeded)
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
ls -lZ $RPM_BUILD_ROOT/*
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc README Changes
# For noarch packages: vendorlib
%{perl_vendorlib}/Pod/Plainer.pm
%{_mandir}/man3/Pod::Plainer.3pm*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.03-11
- Rebuild for new 4.0 release.

