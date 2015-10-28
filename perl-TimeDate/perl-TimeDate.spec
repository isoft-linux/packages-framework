Name:           perl-TimeDate
Version:        2.30
Epoch:          1
Release:        8%{?dist}
Summary:        A Perl module for time and date manipulation
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/TimeDate/
Source0:        http://www.cpan.org/authors/id/G/GB/GBARR/TimeDate-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module includes a number of smaller modules suited for
manipulation of time and date strings with Perl. In particular, the
Date::Format and Date::Parse modules can display and read times and
dates in various formats, providing a more reliable interface to
textual representations of points in time.

%prep
%setup -q -n TimeDate-%{version}
# ChangeLog is ISO-8859-1 encoded
iconv -f iso-8859-1 -t utf8 < ChangeLog > ChangeLog.utf8
mv ChangeLog.utf8 ChangeLog
# Bogus exec permissions on some language modules
chmod -x lib/Date/Language/{Russian_cp1251,Russian_koi8r,Turkish}.pm

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files 
%doc README ChangeLog
%{perl_vendorlib}/Date/
%{perl_vendorlib}/Time/
%{_mandir}/man3/*.3*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:2.30-8
- Rebuild for new 4.0 release.

