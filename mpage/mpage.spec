Summary: A tool for printing multiple pages of text on each printed page
Name: mpage
Version: 2.5.6
Release: 17 
License: GPLv2+
Url: http://www.mesa.nl/pub/mpage/
Source: ftp://ftp.mesa.nl/pub/mpage/mpage-%{version}.tgz
Patch0: mpage25-config.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX) 

%description
The mpage utility takes plain text files or PostScript(TM) documents
as input, reduces the size of the text, and prints the files on a
PostScript printer with several pages on each sheet of paper. Mpage is
very useful for viewing large printouts without using up lots of
paper. Mpage supports many different layout options for the printed
pages.

%prep
%setup -q
%patch0 -p1 -b .config

%build
make BINDIR=%{_bindir} LIBDIR=%{_datadir} MANDIR=%{_mandir}/man1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/mpage,%{_mandir}/man1}

make PREFIX=$RPM_BUILD_ROOT/%{_prefix} BINDIR=$RPM_BUILD_ROOT/%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT/%{_datadir} \
	MANDIR=$RPM_BUILD_ROOT/%{_mandir}/man1 \
	install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES Copyright README NEWS TODO FAQ COPYING COPYING.LESSER
%{_bindir}/mpage
%{_mandir}/man1/mpage.*
%{_datadir}/mpage

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.5.6-17
- Rebuild for new 4.0 release.

