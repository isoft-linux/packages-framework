Name:           stoken
Version:        0.81
Release:        6
Summary:        Token code generator compatible with RSA SecurID 128-bit (AES) token

License:        LGPLv2+
URL:            http://%{name}.sf.net
Source0:        https://github.com/cernekee/%{name}/archive/v%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  libtool
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(hogweed) >= 2.4
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(nettle) >= 2.4

%description
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description devel
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package provides the development files for %{name}.

%package libs
Summary:        Libraries for %{name}
Requires(post): ldconfig

%description libs
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package contains %{name} libraries.

%package cli
Summary:        Command line tool for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description cli
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package contains the command line tool for %{name}.

%package gui
Summary:        Graphical interface program for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description gui
Software Token for Linux/UNIX. It's a token code generator compatible with RSA
SecurID 128-bit (AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

This package contains the graphical interface program for %{name}.

%prep
%setup -q

%build
autoreconf -v -f --install
%configure --with-gtk --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

#DO NOT display there two menu item
echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/stoken-gui.desktop
echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/stoken-gui-small.desktop

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-gui.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-gui-small.desktop

# Remove stuff we don't need
find %{buildroot} -type f -name "*.la" -delete
rm -fr %{buildroot}%{_docdir}/%{name}

# Merge applications into one software center item
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/stoken-gui-small.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<component type="desktop">
  <metadata_license>CC0-1.0</metadata_license>
  <id>stoken-gui-small.desktop</id>
  <metadata>
    <value key="X-Merge-With-Parent">stoken-gui.desktop</value>
  </metadata>
</component>
EOF

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%doc COPYING.LIB CHANGES
%{_libdir}/*.so.*

%files cli
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%files gui
%{_bindir}/%{name}-gui
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/%{name}-gui.desktop
%{_datadir}/applications/%{name}-gui-small.desktop
%{_datadir}/pixmaps/%{name}-gui.png
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}-gui.1.gz

%files devel
%{_includedir}/%{name}.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.81-6
- Rebuild for new 4.0 release.

