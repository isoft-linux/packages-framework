Name:			graphviz
Summary:		Graph Visualization Tools
Version:		2.38.0
Release:	 	2	
License:		CPL
URL:			http://www.graphviz.org/
Source0:		http://www.graphviz.org/pub/graphviz/ARCHIVE/%{name}-%{version}.tar.gz
Patch0:         0001-clone-nameclash.patch
#build clang/libc++ need this patch
Patch1:         graphviz-link-to-c++.patch

BuildRequires:		zlib-devel, libpng-devel, libjpeg-devel, expat-devel, freetype-devel >= 2
BuildRequires:		bison, m4, flex, swig
BuildRequires:		fontconfig-devel, libltdl-devel, python-devel
BuildRequires:		cairo-devel >= 1.1.10, pango-devel, gmp-devel
BuildRequires:		perl-devel, swig >= 1.3.33
Requires(post):		/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description
A collection of tools for the manipulation and layout of graphs (as in nodes 
and edges, not as in barcharts).

%package devel
Summary:		Development package for graphviz
Requires:		%{name} = %{version}-%{release}, pkgconfig

%description devel
A collection of tools for the manipulation and layout of graphs (as in nodes 
and edges, not as in barcharts). This package contains development files for 
graphviz.


%package doc
Summary:		PDF and HTML documents for graphviz

%description doc
Provides some additional PDF and HTML documentation for graphviz.

%package graphs
Summary:		Demo graphs for graphviz

%description graphs
Some demo graphs for graphviz.

%package perl
Summary:		Perl extension for graphviz
Requires:		%{name} = %{version}-%{release}
Requires:		perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl extension for graphviz.

%package python
Summary:		Python extension for graphviz
Requires:		%{name} = %{version}-%{release}, python

%description python
Python extension for graphviz.

%prep
%setup -q
%patch0 -p1
#%patch1 -p1

%build
%configure \
    --disable-static \
    --disable-dependency-tracking \
    --disable-sharp \
    --disable-go \
    --disable-r \
    --disable-ruby \
    --disable-tcl \
    --disable-java \
    --disable-lua \
    --disable-php \
    --disable-ocaml \
    --enable-perl \
    --enable-python \
    --with-x \
    --with-poppler \
    --with-rsvg \
    --with-ghostscript \
    --with-pangocairo \
    --with-freetype2 \
    --with-fontconfig \
    --with-gdk \
    --with-gdk-pixbuf \
    --without-gtk \
    --with-gts=no \
    --without-gtkglext \
    --with-libgd=no \
    --without-smyrna \
    --without-qt \
	--without-ming
make %{?_smp_mflags}

%install
rm -rf %{buildroot} __doc
make DESTDIR=%{buildroot} \
        docdir=%{buildroot}%{_docdir}/%{name} \
        pkgconfigdir=%{_libdir}/pkgconfig \
        install
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
chmod -x %{buildroot}%{_datadir}/%{name}/lefty/*
cp -a %{buildroot}%{_datadir}/%{name}/doc __doc
rm -rf %{buildroot}%{_datadir}/%{name}/doc

%check

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
%{_bindir}/dot -c

# if there is no dot after everything else is done, then remove config
%postun
if [ $1 -eq 0 ]; then
        rm -f %{_libdir}/graphviz/config || :
fi
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_libdir}/graphviz
%{_libdir}/*.so.*
%{_libdir}/graphviz/*.so.*
%{_mandir}/man1/*.1*
%{_mandir}/man7/*.7*
%dir %{_datadir}/graphviz
%{_datadir}/graphviz/gvpr
%{_datadir}/graphviz/lefty
%{_libdir}/graphviz/*.so
%exclude %{_libdir}/graphviz/*/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/graphviz
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*

%files doc
%defattr(-,root,root,-)
%doc __doc/*

%files graphs
%defattr(-,root,root,-)
%dir %{_datadir}/graphviz
%{_datadir}/graphviz/graphs

%files perl
%defattr(-,root,root,-)
%{_libdir}/graphviz/perl/
%{_libdir}/perl*/*
%{_datadir}/graphviz/demo/modgraph.pl

%files python
%defattr(-,root,root,-)
%{_libdir}/graphviz/python/
%{_libdir}/python*/*
%{_datadir}/graphviz/demo/modgraph.py


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.38.0-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

