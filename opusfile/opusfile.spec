Name:          opusfile
Version:       0.6
Release:       4%{?dist}
Summary:       A high-level API for decoding and seeking within .opus files

License:       BSD
URL:           http://www.opus-codec.org/
Source0:       http://downloads.xiph.org/releases/opus/%{name}-%{version}.tar.gz

BuildRequires: libogg-devel
BuildRequires: openssl-devel
BuildRequires: opus-devel

%description
libopusfile provides a high-level API for decoding and seeking 
within .opus files. It includes:
* Support for all files with at least one Opus stream (including
multichannel files or Ogg files where Opus is muxed with something else).
* Full support, including seeking, for chained files.
* A simple stereo downmixing API (allowing chained files to be
decoded with a single output format, even if the channel count changes).
* Support for reading from a file, memory buffer, or over HTTP(S)
(including seeking).
* Support for both random access and streaming data sources.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.

%prep
%setup -q

%build
%configure --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING AUTHORS
%{_libdir}/libopusfile.so.*
%{_libdir}/libopusurl.so.*

%files devel
%doc %{_docdir}/%{name}
%{_includedir}/opus/opus*
%{_libdir}/pkgconfig/opusfile.pc
%{_libdir}/pkgconfig/opusurl.pc
%{_libdir}/libopusfile.so
%{_libdir}/libopusurl.so

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.6-4
- Rebuild for new 4.0 release.

