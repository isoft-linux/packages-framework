Name:	    fonts-Unifont	
Version:	7.0.06
Release:	2
Summary:	GNU Unifont

License:	GPLV2+
URL:		http://unifoundry.com/unifont.html
Source0:	http://unifoundry.com/pub/unifont-7.0.06/font-builds/unifont-%{version}.pcf.gz
Requires(post):fontconfig

BuildArch: noarch

%description
%{summary}

%prep

%build
%install
mkdir -p %{buildroot}%{_datadir}/fonts/unifont
install -m0644 %{SOURCE0} %{buildroot}%{_datadir}/fonts/unifont/
pushd %{buildroot}%{_datadir}/fonts/unifont
gunzip unifont-%{version}.pcf.gz 
popd

%files
%{_datadir}/fonts/unifont/unifont-%{version}.pcf

%changelog
* Sat Oct 24 2015 builder - 7.0.06-2
- Rebuild for new 4.0 release.


