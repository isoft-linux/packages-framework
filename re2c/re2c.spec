Summary: Tool for generating C-based recognizers from regular expressions
Name: re2c
Version: 0.13.5
Release: 12%{?dist}
License: Public Domain
URL: http://re2c.org/
Source: http://downloads.sf.net/re2c/re2c-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
re2c is a tool for writing very fast and very flexible scanners. Unlike any
other such tool, re2c focuses on generating high efficient code for regular
expression matching. As a result this allows a much broader range of use than
any traditional lexer offers. And Last but not least re2c generates warning
free code that is equal to hand-written code in terms of size, speed and
quality.


%prep
%setup -q
# Fix all those executable files, set executable only the ones that need to be
find . -type f -exec chmod -x {} \;
%{__chmod} +x configure depcomp install-sh missing


%build
%configure
# Build re2c, then our own scanner.cc, then rebuild the final re2c with it
%{__make} %{?_smp_mflags} re2c
%{__rm} -f scanner.cc
./re2c -b -o scanner.cc scanner.re
%{__rm} -f re2c scanner.o
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__install} -D -p -m 0755 re2c %{buildroot}%{_bindir}/re2c
%{__install} -D -p -m 0644 re2c.1 %{buildroot}%{_mandir}/man1/re2c.1


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGELOG README examples/ doc/* lessons/
%{_bindir}/re2c
%{_mandir}/man1/re2c.1*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.13.5-12
- Rebuild for new 4.0 release.

