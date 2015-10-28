Name:           perl-Text-Soundex
Version:        3.04
Release:        297%{?dist}
Summary:        Implementation of the soundex algorithm
License:        Copyright only
URL:            http://search.cpan.org/dist/Text-Soundex/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Text-Soundex-%{version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time:
# Carp not needed for tests
%if 0%(perl -e 'print $] > 5.016')
BuildRequires:  perl(deprecate)
%endif
BuildRequires:  perl(Exporter)
BuildRequires:  perl(if)
# Text::Unidecode not needed for tests
BuildRequires:  perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
%if 0%(perl -e 'print $] > 5.016')
Requires:       perl(deprecate)
%endif
Requires:       perl(Text::Unidecode)

%{?perl_default_filter}

%description
Soundex is a phonetic algorithm for indexing names by sound, as pronounced in
English. This module implements the original soundex algorithm developed by
Robert Russell and Margaret Odell, as well as a variation called "American
Soundex".

%prep
%setup -q -n Text-Soundex-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Text*
%{_mandir}/man3/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.04-297
- Rebuild for new 4.0 release.

