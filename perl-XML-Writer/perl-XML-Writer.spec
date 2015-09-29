Name:           perl-XML-Writer
Version:        0.625
Release:        4%{?dist}
Summary:        A simple Perl module for writing XML documents
Group:          Development/Libraries
License:        CC0
URL:            http://search.cpan.org/dist/XML-Writer/
Source0:        http://www.cpan.org/authors/id/J/JO/JOSEPHW/XML-Writer-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(overload)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Encode)
BuildRequires:  perl(Errno)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test::More) >= 0.047
BuildRequires:  perl(warnings)

BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
Requires:  perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
XML::Writer is a simple Perl module for writing XML documents: it
takes care of constructing markup and escaping data correctly, and by
default, it also performs a significant amount of well-formedness
checking on the output, to make certain (for example) that start and
end tags match, that there is exactly one document element, and that
there are not duplicate attribute names.

%prep
%setup -q -n XML-Writer-%{version}
find examples -type f -exec chmod -x {} +

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} 

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -a \( -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'

%check
make test

%files
%doc Changes examples LICENSE README TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
