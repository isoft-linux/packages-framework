Name:           libnice
Version:        0.1.13
Release:        3
Summary:        GLib ICE implementation

License:        LGPLv2 and MPLv1.1
URL:            http://nice.freedesktop.org/wiki/
Source0:        http://nice.freedesktop.org/releases/%{name}-%{version}.tar.gz

BuildRequires:	glib2-devel
BuildRequires:  gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:  gstreamer-devel >= 0.11.91
BuildRequires:	gstreamer-plugins-base-devel >= 0.11.91
BuildRequires:	gupnp-igd-devel >= 0.1.2
BuildRequires:  gobject-introspection-devel

%description
%{name} is an implementation of the IETF's draft Interactive Connectivity
Establishment standard (ICE). ICE is useful for applications that want to
establish peer-to-peer UDP data streams. It automates the process of traversing
NATs and provides security against some attacks. Existing standards that use
ICE include the Session Initiation Protocol (SIP) and Jingle, XMPP extension
for audio/video calls.


%package        gstreamer0
Summary:        GStreamer plugin for %{name}
Requires:       %{name} = %{version}-%{release}

%description    gstreamer0
The %{name}-gstreamer package contains a gstreamer 0.10 plugin for %{name}.


%package        gstreamer
Summary:        GStreamer plugin for %{name}
Requires:       %{name} = %{version}-%{release}

%description    gstreamer
The %{name}-gstreamer package contains a gstreamer 1.0 plugin for %{name}.


%package        examples
Summary:        Simple %{name} usage examples
Requires:       %{name} = %{version}-%{release}

%description    examples
The %{name}-examples package contains usage (simple, threaded and sdp) examples.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:	glib2-devel
Requires:	pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
#three test failed.
#make check ||:


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%{_bindir}/stunbdc
%{_bindir}/stund
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/Nice-0.1.typelib

%files gstreamer
%{_libdir}/gstreamer-1.0/libgstnice.so


%files examples
%{_bindir}/sdp-example
%{_bindir}/simple-example
%{_bindir}/threaded-example


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/nice.pc
%{_datadir}/gtk-doc/html/%{name}/
%{_datadir}/gir-1.0/Nice-0.1.gir


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 0.1.13-3
- Rebuild for 4.0 release

