Name:           ragel   
Version:        6.8
Release:        5%{?dist}
Summary:        Finite state machine compiler

Group:          Development/Tools
License:        GPLv2+
URL:            http://www.complang.org/%{name}/
Source0:        http://www.complang.org/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# for documentation building
BuildRequires:  autoconf, gcc
Requires:       gawk

%description
Ragel compiles finite state machines from regular languages into executable C,
C++, Objective-C, or D code. Ragel state machines can not only recognize byte
sequences as regular expression machines do, but can also execute code at
arbitrary points in the recognition of a regular language. Code embedding is
done using inline operators that do not disrupt the regular language syntax.

%prep
%setup -q

# Pass fedora cflags correctly
sed -i.flags \
    -e '\@^CXXFLAGS=@d' \
    configure{.in,}
touch timestamp
touch -r timestamp \
    aclocal.m4 configure.in configure config.h.in \
    Makefile.in */Makefile.in

%build
# set the names of the other programming commandline programs
%configure --docdir=%{_docdir}/%{name} RUBY=ruby JAVAC=javac GMCS=mcs

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING ragel.vim CREDITS ChangeLog
%doc doc/ragel-guide.pdf
%{_bindir}/ragel
%{_mandir}/*/*

%changelog
