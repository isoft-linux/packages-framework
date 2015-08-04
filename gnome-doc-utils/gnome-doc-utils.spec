Name: gnome-doc-utils
Version: 0.20.10
Release: 1
License: LGPL
Group: Development/Tools
Summary: Documentation utilities for the GNOME project
URL: http://www.gnome.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Source: %{name}-%{version}.tar.xz

BuildArch: noarch

### Patches ###

### Dependencies ###

Requires: libxml2 >= 2.6.12
Requires: libxslt >= 1.1.8
Requires: python-libxml2

### Build Dependencies ###

BuildRequires: libxml2-devel >= 2.6.12
BuildRequires: libxslt-devel >= 1.1.8

BuildRequires: perl-XML-Parser
BuildRequires: gettext

%description
gnome-doc-utils is a collection of documentation utilities for the GNOME
project. Notably, it contains utilities for building documentation and
all auxiliary files in your source tree, and it contains the DocBook
XSLT stylesheets that were once distributed with Yelp.

%prep
%setup -q

%build
%configure --disable-scrollkeeper
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
sed -i 's@#!/bin/python@#!/usr/bin/python@g' $RPM_BUILD_ROOT%{_bindir}/xml2po

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS README NEWS
%{_bindir}/*
%{_datadir}/pkgconfig/*
%{_datadir}/xml/*
%{_datadir}/aclocal/gnome-doc-utils.m4
%{_datadir}/gnome/help
#%{_datadir}/omf/gnome-doc-make
#%{_datadir}/omf/gnome-doc-xslt
%{_datadir}/xml/gnome
%{_libdir}/python*
%{_mandir}/man1/xml2po.1.gz
%{_datadir}/gnome-doc-utils

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

