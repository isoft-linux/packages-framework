Name:           uriparser
Version:        0.8.2
Release:        2%{?dist}
Summary:        URI parsing library - RFC 3986

License:        BSD
URL:            http://%{name}.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  doxygen, graphviz, cpptest-devel

%description
Uriparser is a strictly RFC 3986 compliant URI parsing library written
in C. uriparser is cross-platform, fast, supports Unicode and is
licensed under the New BSD license.

%package	devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
sed -i 's/\r//' THANKS
sed -i 's/\r//' COPYING
iconv -f iso-8859-1 -t utf-8 -o THANKS{.utf8,}
mv THANKS{.utf8,}

%build

# Remove qhelpgenerator dependency by commenting Doxygen.in:
# sed -i 's/GENERATE_QHP\ =\ yes/GENERATE_QHP\ =\ no/g' Doxyfile.in
sed -i 's/GENERATE_QHP\ =\ yes/GENERATE_QHP\ =\ no/g' doc/Doxyfile.in

%configure --disable-static 

# disable rpath 
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Generate docs first
cd doc;
make %{?_smp_mflags}
cd ..
# Build
make %{?_smp_mflags}

%check
LD_LIBRARY_PATH=".libs" make check

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -delete

if [ ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name} != ${RPM_BUILD_ROOT}%{_pkgdocdir} ]
  then mv ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}/html ${RPM_BUILD_ROOT}%{_pkgdocdir}
fi

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc THANKS AUTHORS COPYING ChangeLog
%{_bindir}/uriparse
%{_libdir}/*.so.*

%files devel
%doc doc/html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.8.2-2
- Rebuild for new 4.0 release.

