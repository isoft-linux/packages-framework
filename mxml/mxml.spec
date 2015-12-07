Summary:      Miniature XML development library
Name:         mxml
Version:      2.8
Release:      2%{?dist}
License:      LGPLv2+
URL:          http://www.msweet.org/blog.php?L+Z3
Source0:      https://www.msweet.org/files/project3/mxml-2.8.tar.gz

# This is requires because we patch configure.in.
BuildRequires: autoconf

%description
Mini-XML is a small XML parsing library that you can use to read XML
and XML-like data files in your application without requiring large
non-standard libraries.

%package devel
Summary:  Libraries, includes, etc to develop mxml applications
Requires: mxml = %{version}-%{release}
Requires: pkgconfig

%description devel
Libraries, include files, etc you can use to develop mxml
applications.

%prep
%setup -q

%build
# Run autoconf since we patched configure.in.
autoconf
%configure --enable-shared
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make BUILDROOT=%{buildroot} install

# Configuring with --disable-static doesn't work, so let's just delete
# the .a file by hand.
rm %{buildroot}%{_libdir}/libmxml.a

# remove extra docs
rm -rf %{buildroot}%{_datadir}/doc/mxml/

# remove rendered man pages
rm -f %{buildroot}%{_datadir}/man/cat*/*


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/*
%{_libdir}/libmxml.so.*

%files devel
%defattr(-,root,root,-)
%doc CHANGES doc/*.html doc/*.gif
%{_includedir}/*.h
%{_libdir}/libmxml.so
%{_mandir}/*/*
%{_libdir}/pkgconfig/mxml.pc

%changelog
* Mon Dec 07 2015 Cjacker <cjacker@foxmail.com> - 2.8-2
- Initial build

