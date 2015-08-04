Name:           perl-XML-LibXML
Version:        2.0117
Release:        1
Epoch:          1
Summary:        Perl interface to the libxml2 library
Group:          Development/Libraries
License:        (GPL+ or Artistic) and MIT
URL:            http://search.cpan.org/dist/XML-LibXML/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/XML-LibXML-%{version}.tar.gz 
Patch0:         XML-LibXML-disable-check-libxml2-we-know-it-works.patch

BuildRequires:  libxml2-devel
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(XML::NamespaceSupport)
BuildRequires:  perl(XML::SAX::Base)
BuildRequires:  perl(XML::SAX::DocumentLocator)
BuildRequires:  perl(XML::SAX::Exception)
BuildRequires:  perl(URI::file)
BuildRequires:  perl(utf8)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# threads and threads::shared are optional
Provides:       perl-XML-LibXML-Common = %{version}
Obsoletes:      perl-XML-LibXML-Common <= 0.13

%{?perl_default_filter}

%description
This module implements a Perl interface to the GNOME libxml2 library
which provides interfaces for parsing and manipulating XML files. This
module allows Perl programmers to make use of the highly capable
validating XML parser and the high performance DOM implementation.

%prep
%setup -q -n XML-LibXML-%{version}
%patch0 -p1
chmod -x *.c

%build
perl Makefile.PL SKIP_SAX_INSTALL=1 INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
THREAD_TEST=1 make test

%triggerin -- perl-XML-SAX
for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
  perl -MXML::SAX -e "XML::SAX->add_parser(q($p))->save_parsers()" \
    2>/dev/null || :
done

%preun
if [ $1 -eq 0 ] ; then
  for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
    perl -MXML::SAX -e "XML::SAX->remove_parser(q($p))->save_parsers()" \
      2>/dev/null || :
  done
fi

%files
%{perl_vendorarch}/auto/XML
%{perl_vendorarch}/XML
%{_mandir}/man3/*.3*

