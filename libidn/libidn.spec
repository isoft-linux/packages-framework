Summary: Internationalized Domain Name support library
Name: libidn
Version: 1.30
Release: 2.1
URL: http://www.gnu.org/software/libidn
License: LGPL
Source0: http://ftp.gnu.org/gnu/libidn/libidn-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pkgconfig, gettext
Requires(postun): /sbin/ldconfig
Requires(pre): /sbin/ldconfig

%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package devel
Summary: Development files for the libidn library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes header files and libraries necessary for
developing programs which use the GNU libidn library.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%makeinstall

# provide more examples
make %{?_smp_mflags} -C examples distclean

# clean up docs
find doc -name "Makefile*" | xargs rm
rm -rf $RPM_BUILD_ROOT%{_datadir}/info

%find_lang %{name}

%check
LC_MESSAGES=en_US make %{?_smp_mflags} -C tests check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/idn
%{_mandir}/man1/idn.1*
%{_datadir}/emacs/site-lisp
%{_libdir}/libidn.so.*

%files devel
%defattr(0644,root,root,755)
%{_libdir}/libidn.so
%{_libdir}/libidn.a
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.30-2.1
- Rebuild for new 4.0 release.

* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
