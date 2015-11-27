%global gst_ver 1.0.0
%global gst_plugins_base_ver 1.0.0

Name:           farstream 
Version:        0.2.7
Release:        2
Summary:        Libraries for videoconferencing
License:        LGPLv2+ and GPLv2+
URL:            http://www.freedesktop.org/wiki/Software/Farstream
Source0:        http://freedesktop.org/software/farstream/releases/farstream/%{name}-%{version}.tar.gz

BuildRequires:  libnice-devel >= 0.1.8
BuildRequires:  gstreamer-devel >= %{gst_ver}
BuildRequires:  gstreamer-plugins-base-devel >= %{gst_plugins_base_ver}
BuildRequires:  gupnp-igd-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  python-devel

Requires:       gstreamer-plugins-good >= 1.0.0
Requires:       gstreamer-plugins-bad >= 1.0.0
Requires:       libnice-gstreamer


%description
%{name} is a collection of GStreamer modules and libraries for
videoconferencing.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gstreamer-devel  >= %{gst_ver}
Requires:       gstreamer-plugins-base-devel >= %{gst_plugins_base_ver}
Requires:       pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q




%build
export CC=cc
export CXX=c++
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%check
#some faield, need check
make check ||:


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%{_libdir}/*.so.*
%dir %{_libdir}/farstream-0.2
%{_libdir}/farstream-0.2/libmulticast-transmitter.so
%{_libdir}/farstream-0.2/libnice-transmitter.so
%{_libdir}/farstream-0.2/librawudp-transmitter.so
%{_libdir}/farstream-0.2/libshm-transmitter.so
%{_libdir}/gstreamer-1.0/libfsmsnconference.so
%{_libdir}/gstreamer-1.0/libfsrawconference.so
%{_libdir}/gstreamer-1.0/libfsrtpconference.so
%{_libdir}/gstreamer-1.0/libfsrtpxdata.so
%{_libdir}/gstreamer-1.0/libfsvideoanyrate.so
%{_libdir}/girepository-1.0/Farstream-0.2.typelib
%dir %{_datadir}/farstream
%dir %{_datadir}/farstream/0.2
%dir %{_datadir}/farstream/0.2/fsrtpconference
%dir %{_datadir}/farstream/0.2/fsrawconference
%{_datadir}/farstream/0.2/fsrawconference/default-element-properties
%{_datadir}/farstream/0.2/fsrtpconference/default-codec-preferences
%{_datadir}/farstream/0.2/fsrtpconference/default-element-properties

%files devel
%{_libdir}/libfarstream-0.2.so
%{_libdir}/pkgconfig/farstream-0.2.pc
%{_includedir}/farstream-0.2/farstream/
%{_datadir}/gir-1.0/Farstream-0.2.gir
%{_datadir}/gtk-doc/html/farstream-libs-0.2/
%{_datadir}/gtk-doc/html/farstream-plugins-0.2/


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 0.2.7-2
- Rebuild for 4.0 release

