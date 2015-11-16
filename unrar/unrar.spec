%define debug_package %{nil}

Name:	    unrar	
Version:	5.2.2
Release:	2
Summary:	unRAR is a utility to extract, view, and test the contents of an RAR archive

License:	Unrar License
URL:		http://www.rarlab.com/rar_add.htm
Source0:	http://www.rarlab.com/rar/unrarsrc-%{version}.tar.gz
Source1:        http://www.rarlabs.com/rar/rarlinux-x64-5.3.b6.tar.gz

BuildRequires:	compiler-wrapper

%description
%{summary}

%prep
%setup -q -n unrar -a1

%build
make


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m0755 unrar $RPM_BUILD_ROOT%{_bindir}

%files
%{_bindir}/unrar

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 5.2.2-2
- Rebuild for new 4.0 release.


