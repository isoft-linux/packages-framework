%define lang en
%define langrelease 0
%define aspellversion 6
Summary: English dictionaries for Aspell
Name: aspell-%{lang}
Epoch: 50
Version: 7.1
Release: 10%{?dist}
License: MIT and BSD
URL: http://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/dict/%{lang}/aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}.tar.bz2
Buildrequires: aspell >= 12:0.60
Requires: aspell >= 12:0.60
Obsoletes: aspell-en-gb <= 0.33.7.1
Obsoletes: aspell-en-ca <= 0.33.7.1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define debug_package %{nil}

%description
Provides the word list/dictionaries for the following: English, Canadian
English, British English

%prep
%setup -q -n aspell%{aspellversion}-%{lang}-%{version}-%{langrelease}

%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Copyright
%{_libdir}/aspell-0.60/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 50:7.1-10
- Rebuild for new 4.0 release.

