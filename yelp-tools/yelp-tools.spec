Name:          yelp-tools
Version:       3.18.0
Release:       1
Summary:       Create, manage, and publish documentation for Yelp

License:       GPLv2+
URL:           http://projects.gnome.org/yelp/
Source0:       http://download.gnome.org/sources/yelp-tools/3.10/yelp-tools-%{version}.tar.xz
BuildArch:     noarch

BuildRequires: yelp-xsl-devel
BuildRequires: itstool
BuildRequires: libxslt

Requires: /usr/bin/itstool
Requires: /usr/bin/xmllint
Requires: yelp-xsl

%description
yelp-tools is a collection of scripts and build utilities to help create,
manage, and publish documentation for Yelp and the web. Most of the heavy
lifting is done by packages like yelp-xsl and itstool. This package just
wraps things up in a developer-friendly way.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%{_bindir}/yelp-build
%{_bindir}/yelp-check
%{_bindir}/yelp-new
%{_datadir}/yelp-tools
%{_datadir}/aclocal/yelp.m4

%changelog
* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

