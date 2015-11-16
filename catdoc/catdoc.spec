Name: catdoc
Version: 0.94.2
Release: 2%{?dist}
Summary: A program which converts Microsoft office files to plain text        

License: GPL+       
URL: http://www.wagner.pp.ru/~vitus/software/catdoc/           
Source0: http://ftp.wagner.pp.ru/pub/catdoc/%{name}-%{version}.tar.gz      
Patch0: makefilefix.patch
Patch1: catdoc-0.94.2-bufferoverflow-rh872390-rh872391.patch
Patch2: catdoc-0.94.2-cflags.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: tk
Requires: tk

%description
catdoc is program which reads one or more Microsoft word files
and outputs text, contained insinde them to standard output.
Therefore it does same work for.doc files, as unix cat
command for plain ASCII files.
It is now accompanied by xls2csv - program which converts
Excel spreadsheet into comma-separated value file,
and catppt - utility to extract textual information
from Powerpoint files

%prep
%setup -q
%patch0 -p1 -b .makefilefix
%patch1 -p1 -b .bufferoverflow
%patch2 -p1 -b .cflags

%build
%configure \
    --with-wish=/usr/bin/wish
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/catdoc
%{_bindir}/catppt
%{_bindir}/wordview
%{_bindir}/xls2csv
%{_mandir}/man1/catdoc.1.*
%{_mandir}/man1/catppt.1.*
%{_mandir}/man1/wordview.1.*
%{_mandir}/man1/xls2csv.1.*
%{_datadir}/catdoc
%doc COPYING README NEWS



%changelog
* Sun Nov 15 2015 Cjacker <cjacker@foxmail.com> - 0.94.2-2
- Initial build

