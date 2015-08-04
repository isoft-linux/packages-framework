# for other future directories from http://www.unicode.org/Public
%global unicodedir %{_datadir}/unicode
%global ucddir %{unicodedir}/ucd

Name:           unicode-ucd
Version:        8.0.0
Release:        1%{?dist}
Summary:        Unicode Character Database

# https://fedoraproject.org/wiki/Licensing/MIT#Modern_Style_without_sublicense_.28Unicode.29
License:        MIT
URL:            http://www.unicode.org/ucd/
Source0:        http://www.unicode.org/Public/zipped/%{version}/UCD.zip
# http://www.unicode.org/terms_of_use.html referenced in ReadMe.txt redirects to:
Source1:        http://www.unicode.org/copyright.html
BuildArch:      noarch

%description
The Unicode Character Database (UCD) consists of a number of data files listing
Unicode character properties and related data. It also includes data files
containing test data for conformance to several important Unicode algorithms.


%prep
%setup -q -c

grep -q "%{version}" ReadMe.txt || (echo "zip file seems not %{version}" ; exit 1)


%build
%{nil}


%install
mkdir -p %{buildroot}%{ucddir}
cp -ar . %{buildroot}%{ucddir}

cp -p %{SOURCE1} .


%files
%doc copyright.html
%dir %{unicodedir}
%{ucddir}


%changelog
