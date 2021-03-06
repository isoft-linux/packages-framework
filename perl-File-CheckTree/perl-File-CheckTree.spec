Name:           perl-File-CheckTree
Version:        4.42
Release:        296%{?dist}
Summary:        Run many file-test checks on a tree
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/File-CheckTree/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/File-CheckTree-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Cwd)
%if 0%(perl -e 'print $] > 5.017')
BuildRequires:  perl(deprecate)
%endif
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(if)
# Tests:
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if 0%(perl -e 'print $] > 5.017')
Requires:       perl(deprecate)
%endif

%description
File::CheckTree::validate() routine takes a single multi-line string
consisting of directives, each containing a file name plus a file test to try
on it. (The file test may also be a "cd", causing subsequent relative file
names to be interpreted relative to that directory.) After the file test you
may put || die to make it a fatal error if the file test fails. The default is
|| warn.  The file test may optionally have a "!' prepended to test for the
opposite condition. If you do a cd and then list some relative file names, you
may want to indent them slightly for readability. If you supply your own die()
or warn() message, you can use $file to interpolate the file name.

%prep
%setup -q -n File-CheckTree-%{version}

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
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.42-296
- Rebuild for new 4.0 release.

