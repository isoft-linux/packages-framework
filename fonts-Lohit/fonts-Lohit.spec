Summary: Lohit fonts for Indic scripts
Name:    fonts-Lohit
Version: 20140220
Release: 2 
License: LGPLv2+
URL:     https://fedorahosted.org/lohit/
Source0: https://fedorahosted.org/releases/l/o/lohit/lohit-ttf-20140220.tar.gz

Requires: fontconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

%description
Lohit is a font family designed to cover Indic scripts and released by Red Hat. 
The Lohit fonts currently cover 11 languages: Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Oriya, Punjabi, Tamil, Telugu.
%prep
%setup -n lohit-ttf-20140220
%build
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/fonts
install -m 0644 *.ttf $RPM_BUILD_ROOT/usr/share/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root, -)
%{_datadir}/fonts/*.ttf

%changelog
* Sat Oct 24 2015 builder - 20140220-2
- Rebuild for new 4.0 release.

