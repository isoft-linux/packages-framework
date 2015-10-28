%global cpan_version 5.1
Name:           perl-Module-Pluggable
# Epoch to compete with perl.spec
Epoch:          1
# Keep two digit decimal part
Version:        %{cpan_version}0
Release:        7%{?dist}
Summary:        Automatically give your module the ability to have plugins
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Module-Pluggable/
Source0:        http://www.cpan.org/authors/id/S/SI/SIMONW/Module-Pluggable-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
%if 0%(perl -e 'print $] > 5.017')
BuildRequires:  perl(deprecate)
%endif
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec::Functions) >= 3.00
BuildRequires:  perl(if)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.62
BuildRequires:  perl(warnings)
# Optional tests:
# App::FatPacker not yet packaged
#%%if !%%{defined perl_bootstrap}
#BuildRequires:  perl(App::FatPacker) >= 0.10.0
#BuildRequires:  perl(Cwd)
#BuildRequires:  perl(File::Copy)
#BuildRequires:  perl(File::Path)
#BuildRequires:  perl(File::Temp)
#%%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Spec::Functions) >= 3.00
%if 0%(perl -e 'print $] > 5.017')
Requires:       perl(deprecate)
%endif

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(File::Spec::Functions\\)$

%description
This package provides a simple but, hopefully, extensible way of having
'plugins' for your module. Essentially all it does is export a method into
your name space that looks through a search path for .pm files and turn those
into class names. Optionally it instantiates those classes for you.

%prep
%setup -q -n Module-Pluggable-%{cpan_version}
find -type f -exec chmod -x {} +

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1:5.10-7
- Rebuild for new 4.0 release.

