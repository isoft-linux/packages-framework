%define debug_package %{nil}

Name:	iso-codes
Summary:	ISO code lists and translations

Version:    3.58	
Release:	1
License:	LGPLv2+
Group:	System Environment/Base
URL:	http://alioth.debian.org/projects/pkg-isocodes/
Source:	http://ftp.debian.org/debian/pool/main/i/iso-codes/iso-codes-%{version}.tar.xz
BuildRequires:	gettext
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
This package provides the ISO-639 Language code list, the ISO-3166 
Territory code list, and ISO-3166-2 sub-territory lists, and all their 
translations in gettext .po form.

%package devel
Summary:	Files for development using %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# for /usr/share/pkgconfig
Requires:	pkgconfig

%description devel
This package contains the pkg-config files for development
when building programs that use %{name}.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%makeinstall

%find_lang iso-codes --all-name

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f iso-codes.lang
%defattr(-,root,root,-)
%doc ChangeLog README
%dir %{_datadir}/xml/iso-codes
%{_datadir}/xml/iso-codes/*.xml

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/iso-codes.pc

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

