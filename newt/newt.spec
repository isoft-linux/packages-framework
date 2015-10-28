%define pythonver %(%{__python} -c "import sys; print sys.version[:3]")

Summary: A development library for text mode user interfaces.
Name: newt
%define version 0.52.18
Version: %{version}
release: 8 
License: LGPL
Source: https://fedorahosted.org/releases/n/e/newt/newt-%{version}.tar.gz

BuildRequires: python, python-devel, perl, slang-devel, python3, python3-devel

Requires: slang
Provides: snack
BuildRoot: %{_tmppath}/%{name}-%{version}-root


%Description
Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package also contains the
shared library needed by programs built with newt, as well as a
/usr/bin/dialog replacement called whiptail.  Newt is based on the
slang library.

%package devel
Summary: Newt windowing toolkit development files.
Requires: slang-devel %{name} = %{version}

%description devel
The newt-devel package contains the header files and libraries
necessary for developing applications which use newt.  Newt is a
development library for text mode user interfaces.  Newt is based on
the slang library.

Install newt-devel if you want to develop applications which will use
newt.

%package static
Summary: Static newt library
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static newt library

%package python 
Summary: python binding for newt library
Requires: %{name} = %{version}-%{release}
Requires: python

%description python 
python binding for newt library

%package -n python3-newt
Summary: python3 binding for newt library
Requires: %{name} = %{version}-%{release}
Requires: python3

%description -n python3-newt
python binding for newt library


%prep
%setup -q

%build
%configure 
make %{?_smp_mflags} all
chmod 0644 peanuts.py popcorn.py

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
%makeinstall

/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

python -c 'from compileall import *; compile_dir("'$RPM_BUILD_ROOT'%{_libdir}/python%{pythonver}",10,"%{_libdir}/python%{pythonver}")'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig


%files
%defattr (-,root,root)
%doc CHANGES COPYING
%{_bindir}/whiptail
%{_libdir}/libnewt.so.*
%{_mandir}/man1/whiptail.1.gz

%files python
%defattr (-,root,root)
%doc peanuts.py popcorn.py
%{python_sitearch}/*

%files -n python3-newt
%defattr (-,root,root)
%{python3_sitearch}/*

%files devel
%defattr (-,root,root)
%doc tutorial.sgml
%{_includedir}/newt.h
%{_libdir}/libnewt.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/locale

%files static
%defattr (-,root,root)
%{_libdir}/libnewt.a

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.52.18-8
- Rebuild for new 4.0 release.

