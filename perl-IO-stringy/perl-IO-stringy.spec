Summary:	I/O on in-core objects like strings and arrays for Perl
Name:		perl-IO-stringy
Version:	2.111
Release:	3%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/IO-stringy/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DS/DSKOLL/IO-stringy-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
# Module Build
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(FileHandle)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(overload)
BuildRequires:	perl(strict)
BuildRequires:	perl(Symbol)
BuildRequires:	perl(vars)
# Test Suite
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(lib)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Avoid doc-file dependency on /usr/bin/perl
%{?perl_default_filter}

%description
This toolkit primarily provides modules for performing both traditional
and object-oriented I/O) on things *other* than normal filehandles; in
particular, IO::Scalar, IO::ScalarArray, and IO::Lines.

In the more-traditional IO::Handle front, we have IO::AtomicFile, which
may be used to painlessly create files that are updated atomically.

And in the "this-may-prove-useful" corner, we have IO::Wrap, whose
exported wraphandle() function will clothe anything that's not a blessed
object in an IO::Handle-like wrapper... so you can just use OO syntax
and stop worrying about whether your function's caller handed you a
string, a globref, or a FileHandle.

%prep
%setup -q -n IO-stringy-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}

%files
%if 0%{?_licensedir:1}
%license COPYING
%else
%doc COPYING
%endif
%doc README examples/
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::AtomicFile.3*
%{_mandir}/man3/IO::InnerFile.3*
%{_mandir}/man3/IO::Lines.3*
%{_mandir}/man3/IO::Scalar.3*
%{_mandir}/man3/IO::ScalarArray.3*
%{_mandir}/man3/IO::Stringy.3*
%{_mandir}/man3/IO::Wrap.3*
%{_mandir}/man3/IO::WrapTie.3*

%changelog
