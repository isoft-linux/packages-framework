Name:           libfishsound
Version:        1.0.0
Release:        10%{?dist}
Summary:        Simple programming interface for Xiph.Org codecs

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.xiph.org/fishsound/
Source0:        http://downloads.xiph.org/releases/libfishsound/libfishsound-%{version}.tar.gz

# also pulled in by speex-devel
BuildRequires:  pkgconfig
BuildRequires:  libflac-devel
BuildRequires:  libspeex-devel libvorbis-devel liboggz-devel libsndfile-devel
BuildRequires:  doxygen

%description
libfishsound provides a simple programming interface for decoding and
encoding audio data using Xiph.Org codecs (FLAC, Speex and Vorbis).

libfishsound by itself is designed to handle raw codec streams from a
lower level layer such as UDP datagrams. When these codecs are used in
files, they are commonly encapsulated in Ogg to produce Ogg FLAC, Speex
and Ogg Vorbis files.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
# note: intentionally not noarch; contains a target-specific Makefile
Requires:       %{name} = %{version}-%{release}

%description    doc
The %{name}-doc package contains the documentation for %{name}.

%package        tools
Summary:        Sample programs bundled with %{name}
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description    tools
The %{name}-tools package contains sample programs that use %{name}.
The source code for these are included in %{name}-doc.


%prep
%setup -q
# These dependencies should not be exported
# http://github.com/kfish/libfishsound/issues/#issue/1
sed -i '/^Requires:.*/d' fishsound.pc.in


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# overriding docdir does not work
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name} \
   other-docs
# remove Latex docs, they do not provide hyperlinks and
# thus are less usable than the HTML docs
rm -rf other-docs/latex

# move the examples we want
mkdir -p $RPM_BUILD_ROOT%{_bindir}
(cd src/examples/ && \
  mv .libs/* $RPM_BUILD_ROOT%{_bindir} &&
  make clean && rm -rf .deps .libs Makefile.*)
mv src/examples .


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/fishsound.pc

%files doc
%defattr(-,root,root,-)
%doc examples other-docs/*

%files tools
%defattr(-,root,root,-)
%{_bindir}/*


%changelog
