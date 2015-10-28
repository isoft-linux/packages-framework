Name: geteltorito 
Version: 0.6
Release: 2
Summary: A El Torito boot image extractor

License: GPLv2
URL: http://userpages.uni-koblenz.de/~krienke/ftp/noarch/geteltorito
Source0: http://userpages.uni-koblenz.de/~krienke/ftp/noarch/geteltorito/geteltorito

Requires: perl 

%description
%{summary}

%prep
%build
%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/

%files
%{_bindir}/geteltorito

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.6-2
- Rebuild for new 4.0 release.

* Sun Sep 13 2015 Cjacker <cjacker@foxmail.com>
- initial build. it's useful to extract some special iso image such as bios update bootable CD.
