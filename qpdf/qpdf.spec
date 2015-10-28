Summary: Command-line tools and library for transforming PDF files
Name:    qpdf
Version: 5.1.3
Release: 2 
# MIT: e.g. libqpdf/sha2.c
License: Artistic 2.0 and MIT
URL:     http://qpdf.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/qpdf/qpdf-%{version}.tar.gz

Patch0:  qpdf-doc.patch

BuildRequires: zlib-devel
BuildRequires: pcre-devel

# for fix-qdf and test suite
BuildRequires: perl
BuildRequires: perl(Digest::MD5)

# for autoreconf
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

Requires: qpdf-libs%{?_isa} = %{version}-%{release}

%package libs
Summary: QPDF library for transforming PDF files

%package devel
Summary: Development files for QPDF library
Requires: qpdf-libs%{?_isa} = %{version}-%{release}

%package doc
Summary: QPDF Manual
BuildArch: noarch
Requires: qpdf-libs = %{version}-%{release}

%description
QPDF is a command-line program that does structural, content-preserving
transformations on PDF files. It could have been called something
like pdf-to-pdf. It includes support for merging and splitting PDFs
and to manipulate the list of pages in a PDF file. It is not a PDF viewer
or a program capable of converting PDF into other formats.

%description libs
QPDF is a C++ library that inspect and manipulate the structure of PDF files.
It can encrypt and linearize files, expose the internals of a PDF file,
and do many other operations useful to PDF developers.

%description devel
Header files and libraries necessary
for developing programs using the QPDF library.

%description doc
QPDF Manual

%prep
%setup -q

# fix 'complete manual location' note in man pages
%patch0 -p1 -b .doc

%build
autoreconf --verbose --force --install

%configure --disable-static \
           --enable-show-failed-test-output

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

mkdir __doc
mv  %{buildroot}%{_datadir}/doc/qpdf/* __doc
rm -rf %{buildroot}%{_datadir}/doc/qpdf

rm -f %{buildroot}%{_libdir}/libqpdf.la

%check
make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_bindir}/fix-qdf
%{_bindir}/qpdf
%{_bindir}/zlib-flate
%{_mandir}/man1/*

%files libs
%doc README TODO ChangeLog Artistic-2.0
%{_libdir}/libqpdf*.so.*

%files devel
%doc examples/*.cc examples/*.c
%{_includedir}/*
%{_libdir}/libqpdf*.so
%{_libdir}/pkgconfig/libqpdf.pc

%files doc
%doc __doc/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 5.1.3-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

