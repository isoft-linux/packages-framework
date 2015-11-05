Name:		fonts-fontawesome
Version:	4.4.0
Release:	3%{?dist}

Summary:	Iconic font set
License:	OFL
URL:		http://fontawesome.io/
Source0:	http://fontawesome.io/assets/font-awesome-%{version}.zip
Source1:  60-fontawesome.conf	
BuildArch:	noarch
BuildRequires:	fontpackages-devel
BuildRequires:	ttembed
Requires:	fontpackages-filesystem


%description
Font Awesome gives you scalable vector icons that can instantly be
customized — size, color, drop shadow, and anything that can be done with the
power of CSS.

%package web
License:	MIT
Requires:	fonts-fontawesome = %{version}-%{release}
Summary:	Web files for fontawesome

%description web
Web files for Font Awesome.

%prep
%setup -q -n font-awesome-%{version}

%build
ttembed fonts/*.ttf fonts/*.otf

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/
install -m 0644 -p fonts/*.ttf fonts/*.otf fonts/*.woff fonts/*.svg fonts/*.woff2 $RPM_BUILD_ROOT%{_datadir}/fonts/ 

mkdir -p $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
pushd $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/60-fontawesome.conf .
popd

mkdir -p %{buildroot}%{_datadir}/font-awesome-web/
cp -a css less scss %{buildroot}%{_datadir}/font-awesome-web/

%files
%defattr(-,root,root)
%{_sysconfdir}/fonts/conf.d/*
%{_datadir}/fontconfig/conf.avail/*
%{_datadir}/fonts/*.ttf
%{_datadir}/fonts/*.otf

%files web
%{_datadir}/font-awesome-web/
%{_datadir}/fonts/fontawesome-webfont.svg
%{_datadir}/fonts/fontawesome-webfont.woff
%{_datadir}/fonts/fontawesome-webfont.woff2

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 4.4.0-3
- Initial build

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com>
- Initial build

