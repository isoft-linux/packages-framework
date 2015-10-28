Summary:  The Advanced Linux Sound Architecture (ALSA) library
Name:     alsa-lib
Version:  1.0.29
Release:  3
License:  LGPLv2+
URL:      http://www.alsa-project.org/

Source:   ftp://ftp.alsa-project.org/pub/lib/%{name}-%{version}%{?prever}%{?postver}.tar.bz2
Source10: asound.conf
Source11: modprobe-dist-alsa.conf
Source12: modprobe-dist-oss.conf
Patch0:   alsa-lib-1.0.24-config.patch
Patch1:   alsa-lib-1.0.14-glibc-open.patch
Patch2:   alsa-lib-1.0.16-no-dox-date.patch

BuildRequires:  doxygen
Requires(post): /sbin/ldconfig, coreutils

%description
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.

This package includes the ALSA runtime libraries to simplify application
programming and provide higher level functionality as well as support for
the older OSS API, providing binary compatibility for most OSS programs.

%package  devel
Summary:  Development files from the ALSA library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.

This package includes the ALSA development libraries for developing
against the ALSA libraries and interfaces.

%package  -n alsa-ucm
Summary:  ALSA Universal Configuration Manager
Requires: %{name} = %{version}-%{release}

%description -n alsa-ucm
The Advanced Linux Sound Architecture (ALSA) Universal Configuration 
Manager allows configuration of Audio input/output names and routing

%prep
%setup -q -n %{name}-%{version}%{?prever}%{?postver}
%patch0 -p1 -b .config
%patch1 -p1 -b .glibc-open
%patch2 -p1 -b .no-dox-date

%build
%configure --disable-aload --with-plugindir=%{_libdir}/alsa-lib --disable-alisp

# Remove useless /usr/lib64 rpath on 64bit archs
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1
make doc

%install
make DESTDIR=%{buildroot} install

# We need the library to be available even before /usr might be mounted
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libasound.so.* %{buildroot}/%{_lib}
ln -snf ../../%{_lib}/libasound.so.2 %{buildroot}%{_libdir}/libasound.so

# Install global configuration files
mkdir -p -m 755 %{buildroot}/etc
install -p -m 644 %{SOURCE10} %{buildroot}/etc

# Install the modprobe files for ALSA
mkdir -p -m 755 %{buildroot}/lib/modprobe.d/
install -p -m 644 %{SOURCE11} %{buildroot}/lib/modprobe.d/dist-alsa.conf
# bug#926973, place this file to the doc directory
install -p -m 644 %{SOURCE12} .

# Create UCM directory
mkdir -p %{buildroot}/%{_datadir}/alsa/ucm

#Remove libtool archives.
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc doc/asoundrc.txt modprobe-dist-oss.conf
%config %{_sysconfdir}/asound.conf
/%{_lib}/libasound.so.*
%{_bindir}/aserver
%{_libdir}/alsa-lib/
%{_datadir}/alsa/
%exclude %{_datadir}/alsa/ucm
/lib/modprobe.d/dist-*

%files devel
%doc TODO doc/doxygen/
%{_includedir}/alsa/
%{_includedir}/sys/asoundlib.h
%{_libdir}/libasound.so
%{_libdir}/pkgconfig/alsa.pc
%{_datadir}/aclocal/alsa.m4

%files -n alsa-ucm
%{_datadir}/alsa/ucm

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.29-3
- Rebuild for new 4.0 release.

