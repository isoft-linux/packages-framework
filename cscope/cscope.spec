Summary: Cscope is a text screen based source browsing tool.
Name: cscope
Version: 15.8b
Release: 2 
License: GPL
Source: http://prdownloads.sourceforge.net/cscope/cscope-%{version}.tar.gz
Source1: xcscope-init.el
URL: http://cscope.sourceforge.net
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
Cscope is a text screen based source browsing tool.  Although it is
primarily designed to search C code (including lex and yacc files), it
can also be used for C++ code.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/cscope
%{_bindir}/ocs
%{_mandir}/man1/cscope.1.gz

%changelog

