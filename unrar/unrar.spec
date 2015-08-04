Name:	    unrar	
Version:	5.2.2
Release:	1
Summary:	unRAR is a utility to extract, view, and test the contents of an RAR archive

Group:		Extra/Runtime/Utility
License:	Unrar License
URL:		http://www.rarlab.com/rar_add.htm
Source0:	http://www.rarlab.com/rar/unrarsrc-%{version}.tar.gz

BuildRequires:	compiler-wrapper

%description
%{summary}

%prep
%setup -q -n unrar

%build
make


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m0755 unrar $RPM_BUILD_ROOT%{_bindir}

%files
%{_bindir}/unrar

%changelog

