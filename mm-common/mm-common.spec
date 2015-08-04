Name:	    mm-common	
Version:	0.9.7
Release:	1
Summary:    Common build files of the C++ bindings	

Group:	    Desktop/Gnome/Development
License:	GPL
URL:		http://www.gnome.org
Source0:	%{name}-%{version}.tar.xz

%description
The mm-common module provides the build infrastructure and utilities shared among the GNOME C++ binding libraries. It is only a required dependency for building the C++ bindings from the gnome.org version control repository. An installation of mm-common is not required for building tarball releases, unless configured to use maintainer-mode.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rpmclean
%files
%{_bindir}/mm-common-prepare
%{_datadir}/aclocal/*.m4
%{_datadir}/mm-common/*
%{_datadir}/pkgconfig/mm-common-libstdc++.pc
%{_datadir}/pkgconfig/mm-common-util.pc
%{_docdir}/mm-common
%{_mandir}/man1/mm-common-prepare.1.gz


%changelog

