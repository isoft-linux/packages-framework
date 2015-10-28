%define with_python 1
%define with_php 0
%define with_tcl 0
%define with_ruby 0
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define svnrev r1190
#define pretag 1.2.99908020600

# Private libraries are not be exposed globally by RPM
# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


Summary: Round Robin Database Tool to store and display time-series data
Name: rrdtool
Version: 1.4.7
Release: 6
License: GPLv2+ with exceptions
URL: http://oss.oetiker.ch/rrdtool/
Source0: http://oss.oetiker.ch/%{name}/pub/%{name}-%{version}.tar.gz
Source1: php4-%{svnrev}.tar.gz
Patch1: rrdtool-1.4.4-php54.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel, freetype-devel
BuildRequires: libpng-devel, zlib-devel, intltool >= 0.35.0
BuildRequires: cairo-devel >= 1.4.6, pango-devel >= 1.17
BuildRequires: libtool, groff
BuildRequires: gettext, libxml2-devel
BuildRequires: perl, perl-devel

%description
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). It stores the data in a very compact way that will not
expand over time, and it presents useful graphs by processing the data to
enforce a certain data density. It can be used either via simple wrapper
scripts (from shell or Perl) or via frontends that poll network devices and
put a friendly user interface on it.

%package devel
Summary: RRDtool libraries and header files
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). This package allow you to use directly this library.

%package doc
Summary: RRDtool documentation

%description doc
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). This package contains documentation on using RRD.

%package perl
Summary: Perl RRDtool bindings
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Obsoletes: perl-%{name} < %{version}-%{release}
Provides: perl-%{name} = %{version}-%{release}

%description perl
The Perl RRDtool bindings

%if %{with_python}
# Make sure the runtime python is newer than the build one;
# give a default value to handle parsing in cases when python is not present:
%{!?rrd_python_version: %define rrd_python_version %(%{__python} -c 'import sys; print sys.version.split(" ")[0]' || echo "3.14")}

%package python
Summary: Python RRDtool bindings
BuildRequires: python-devel
Requires: python >= %{rrd_python_version}
Requires: %{name} = %{version}-%{release}
Obsoletes: python-%{name} < %{version}-%{release}
Provides: python-%{name} = %{version}-%{release}

%description python
Python RRDtool bindings.
%endif

%ifarch ppc64
# php bits busted on ppc64 at the moment
%define with_php 0
%endif

%if %{with_php}
%package php
Summary: PHP RRDtool bindings
BuildRequires: php-devel >= 4.0
Requires: php >= 4.0
Requires: %{name} = %{version}-%{release}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
Obsoletes: php-%{name} < %{version}-%{release}
Provides: php-%{name} = %{version}-%{release}
Provides: php-pecl(rrdtool)

%description php
The %{name}-php package includes a dynamic shared object (DSO) that adds
RRDtool bindings to the PHP HTML-embedded scripting language.
%endif

%if %{with_tcl}
%package tcl
Summary: Tcl RRDtool bindings
BuildRequires: tcl-devel >= 8.0
Requires: tcl >= 8.0
Requires: %{name} = %{version}-%{release}
Obsoletes: tcl-%{name} < %{version}-%{release}
Provides: tcl-%{name} = %{version}-%{release}

%description tcl
The %{name}-tcl package includes RRDtool bindings for Tcl.
%endif

%if %{with_ruby}

%package ruby
Summary: Ruby RRDtool bindings
BuildRequires: ruby, ruby-devel
Requires: ruby(abi) = 1.9.1
Requires: %{name} = %{version}-%{release}

%description ruby
The %{name}-ruby package includes RRDtool bindings for Ruby.
%endif

%prep
%setup -q -n %{name}-%{version} %{?with_php: -a 1}
%if %{with_php}
%patch1 -p1 -b .php54
%endif

# Fix to find correct python dir on lib64
%{__perl} -pi -e 's|get_python_lib\(0,0,prefix|get_python_lib\(1,0,prefix|g' \
    configure

# Most edits shouldn't be necessary when using --libdir, but
# w/o, some introduce hardcoded rpaths where they shouldn't
%{__perl} -pi.orig -e 's|/lib\b|/%{_lib}|g' \
    configure Makefile.in php4/configure php4/ltconfig*

# Perl 5.10 seems to not like long version strings, hack around it
%{__perl} -pi.orig -e 's|1.299907080300|1.29990708|' \
    bindings/perl-shared/RRDs.pm bindings/perl-piped/RRDp.pm

#
# fix config files for php4 bindings
# workaround needed due to https://bugzilla.redhat.com/show_bug.cgi?id=211069
cp -p /usr/lib/rpm/config.{guess,sub} php4/

%build
%configure \
    --with-perl-options='INSTALLDIRS="vendor"' \
    --disable-rpath \
%if %{with_tcl}
    --enable-tcl-site \
    --with-tcllib=%{_libdir} \
%else
    --disable-tcl \
%endif
%if %{with_python}
    --enable-python \
%else
    --disable-python \
%endif
%if %{with_ruby}
    --enable-ruby \
%endif
    --disable-static \
    --with-pic

# Fix another rpath issue
%{__perl} -pi.orig -e 's|-Wl,--rpath -Wl,\$rp||g' \
    bindings/perl-shared/Makefile.PL

%if %{with_ruby}
# Remove Rpath from Ruby
%{__perl} -pi.orig -e 's|-Wl,--rpath -Wl,\$\(EPREFIX\)/lib||g' \
    bindings/ruby/extconf.rb
sed -i 's| extconf.rb| extconf.rb --vendor |' bindings/Makefile
%endif

# Force RRDp bits where we want 'em, not sure yet why the
# --with-perl-options and --libdir don't take
pushd bindings/perl-piped/
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__perl} -pi.orig -e 's|/lib/perl|/%{_lib}/perl|g' Makefile
popd

#{__make} %{?_smp_mflags}
make

# Build the php module, the tmp install is required
%if %{with_php}
%define rrdtmp %{_tmppath}/%{name}-%{version}-tmpinstall
%{__make} install DESTDIR="%{rrdtmp}"
pushd php4/
%configure \
    --with-rrdtool="%{rrdtmp}%{_prefix}" \
    --disable-static
#{__make} %{?_smp_mflags}
make
popd
%{__rm} -rf %{rrdtmp}
%endif

# Fix @perl@ and @PERL@
find examples/ -type f \
    -exec %{__perl} -pi -e 's|^#! \@perl\@|#!%{__perl}|gi' {} \;
find examples/ -name "*.pl" \
    -exec %{__perl} -pi -e 's|\015||gi' {} \;

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

# Install the php module
%if %{with_php}
%{__install} -D -m0755 php4/modules/rrdtool.so \
    %{buildroot}%{php_extdir}/rrdtool.so
# Clean up the examples for inclusion as docs
%{__rm} -rf php4/examples/.svn
# Put the php config bit into place
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} << __EOF__ > %{buildroot}%{_sysconfdir}/php.d/rrdtool.ini
; Enable rrdtool extension module
extension=rrdtool.so
__EOF__
%endif

# Pesky RRDp.pm...
%{__mv} $RPM_BUILD_ROOT%{perl_vendorlib}/RRDp.pm $RPM_BUILD_ROOT%{perl_vendorarch}/

# Dunno why this is getting installed here...
%{__rm} -f $RPM_BUILD_ROOT%{perl_vendorlib}/leaktest.pl

# We only want .txt and .html files for the main documentation
%{__mkdir_p} doc2/html doc2/txt
%{__cp} -a doc/*.txt doc2/txt/
%{__cp} -a doc/*.html doc2/html/

# Put perl docs in perl package
%{__mkdir_p} doc3/html
%{__mv} doc2/html/RRD*.html doc3/html/

# Clean up the examples
%{__rm} -f examples/Makefile* examples/*.in

# This is so rpm doesn't pick up perl module dependencies automatically
find examples/ -type f -exec chmod 0644 {} \;

# Clean up the buildroot
%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-* \
        $RPM_BUILD_ROOT%{perl_vendorarch}/ntmake.pl \
        $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod \
        $RPM_BUILD_ROOT%{_datadir}/%{name}/examples \
        $RPM_BUILD_ROOT%{perl_vendorarch}/auto/*/{.packlist,*.bs}
%check
# minimal load test for the PHP extension
%if %{with_php}
LD_LIBRARY_PATH=%{buildroot}%{_libdir} php -n \
    -d extension_dir=%{buildroot}%{php_extdir} \
    -d extension=rrdtool.so -m \
    | grep rrdtool
%endif


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/%{name}
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING COPYRIGHT README TODO NEWS THREADS
%doc examples doc2/html doc2/txt

%files perl
%defattr(-,root,root,-)
%doc doc3/html
%{_mandir}/man3/*
%{perl_vendorarch}/*.pm
%attr(0755,root,root) %{perl_vendorarch}/auto/RRDs/

%if %{with_python}
%files python
%defattr(-,root,root,-)
%doc bindings/python/AUTHORS bindings/python/COPYING bindings/python/README
%{python_sitearch}/rrdtoolmodule.so
%{python_sitearch}/py_rrdtool-*.egg-info
%endif

%if %{with_php}
%files php
%defattr(-,root,root,0755)
%doc php4/examples php4/README
%config(noreplace) %{_sysconfdir}/php.d/rrdtool.ini
%{php_extdir}/rrdtool.so
%endif

%if %{with_tcl}
%files tcl
%defattr(-,root,root,-)
%doc bindings/tcl/README
%{_libdir}/tclrrd*.so
%{_libdir}/rrdtool/*.tcl
%endif

%if %{with_ruby}
%files ruby
%defattr(-,root,root,-)
%doc bindings/ruby/README
%{ruby_vendorarchdir}/RRD.so
%endif

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.4.7-6
- Rebuild for new 4.0 release.

