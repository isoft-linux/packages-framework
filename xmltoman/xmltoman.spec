Name:           xmltoman
Version:        0.4
Release:        14%{?dist}
Summary:        Scripts for converting XML to roff or HTML

License:        GPLv2+
URL:            http://sourceforge.net/projects/xmltoman/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         xmltoman-0.3-timestamps.patch

BuildRequires:  perl(XML::Parser)
BuildArch:      noarch

%description
This package provides xmltoman and xmlmantohtml scripts, to compile
the xml representation of manual page to either roff source, or HTML
(while providing the CSS stylesheet for eye-candy look). XSL stylesheet
for doing rougly the same job is provided.


%prep
%setup -q
%patch0 -p1 -b .timestamps


%build
make %{?_smp_mflags}


%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1
cp -p *.1 %{buildroot}%{_mandir}/man1


%files
%{_bindir}/xmltoman
%{_bindir}/xmlmantohtml
%{_datadir}/xmltoman
%{_mandir}/*/*
%doc COPYING README


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.4-14
- Rebuild for new 4.0 release.

