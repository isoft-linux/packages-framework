Name:           docbook2X
Version:        0.8.8
Release:        2%{?dist}
Summary:        Convert docbook into man and Texinfo

License:        MIT
URL:            http://docbook2x.sourceforge.net/
Source0:        http://downloads.sourceforge.net/docbook2x/docbook2X-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl libxslt openjade texinfo %{_bindir}/sgml2xml
# required by the perl -c calls during build
BuildRequires:  perl(XML::SAX::ParserFactory)
# rpmlint isn't happy with libxslt, but we need xsltproc
Requires:       libxslt openjade texinfo %{_bindir}/sgml2xml
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Required by bin/* scripts, who does know why rpmbuild does not generate
# dependencies automatically:
Requires:  perl(Exporter)
Requires:  perl(IO::File)
Requires:  perl(Text::Wrap)
Requires:  perl(vars)
Requires:  perl(XML::SAX::ParserFactory)

%description
docbook2X converts DocBook documents into man pages and Texinfo
documents.


%prep
%setup -q

%build
# to avoid clashing with docbook2* from docbook-utils
%configure --program-transform-name='s/docbook2/db2x_docbook2/'
make %{?_smp_mflags}
rm -rf __dist_html
mkdir -p __dist_html/html
cp -p doc/*.html __dist_html/html


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -c -p'
rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/
rm -rf $RPM_BUILD_ROOT%{_infodir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING README THANKS AUTHORS __dist_html/html/
%{_bindir}/db2x_manxml
%{_bindir}/db2x_texixml
%{_bindir}/db2x_xsltproc
%{_bindir}/db2x_docbook2man
%{_bindir}/db2x_docbook2texi
%{_bindir}/sgml2xml-isoent
%{_bindir}/utf8trans
%dir %{_datadir}/docbook2X
%{_datadir}/docbook2X/VERSION
%dir %{_datadir}/docbook2X/charmaps
%dir %{_datadir}/docbook2X/dtd
%dir %{_datadir}/docbook2X/xslt
%{_datadir}/docbook2X/charmaps/*
%{_datadir}/docbook2X/dtd/*
%{_datadir}/docbook2X/xslt/*
%{_mandir}/man1/*.1*


%changelog
* Mon Dec 07 2015 Cjacker <cjacker@foxmail.com> - 0.8.8-2
- Initial build

