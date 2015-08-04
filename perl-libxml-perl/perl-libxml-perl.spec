Name:           perl-libxml-perl
Version:        0.08
Release:        19
Summary:        A collection of Perl modules for working with XML
Group:          Development/Libraries
License:        (GPL+ or Artistic) and Public Domain
URL:            http://search.cpan.org/dist/libxml-perl/
Source0:        http://www.cpan.org/authors/id/K/KM/KMACLEOD/libxml-perl-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(XML::Parser)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Filter out unversioned provides
%global __provides_exclude %{?__provides_exclude?__provides_exclude|}^perl\\(Data::Grove\\)$

%description
libxml-perl is a collection of smaller Perl modules, scripts, and
documents for working with XML in Perl.  libxml-perl software works in
combination with XML::Parser, PerlSAX, XML::DOM, XML::Grove and
others.

%prep
%setup -q -n libxml-perl-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc ChangeLog Changes README
%{perl_vendorlib}/Data/
%{perl_vendorlib}/XML/
%{_mandir}/man3/*.3*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

