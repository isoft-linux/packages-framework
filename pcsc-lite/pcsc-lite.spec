Name:           pcsc-lite
Version:        1.8.13
Release:        2
Summary:        PC/SC Lite smart card framework and applications

License:        BSD
URL:            http://pcsclite.alioth.debian.org/
Source0:        https://alioth.debian.org/frs/download.php/file/4126/pcsc-lite-%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  systemd-devel
BuildRequires:  /usr/bin/pod2man

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:       %{name}-libs = %{version}-%{release}

%description
The purpose of PC/SC Lite is to provide a Windows(R) SCard interface
in a very small form factor for communicating to smartcards and
readers.  PC/SC Lite uses the same winscard API as used under
Windows(R).  This package includes the PC/SC Lite daemon, a resource
manager that coordinates communications with smart card readers and
smart cards that are connected to the system, as well as other command
line tools.

%package        libs
Summary:        PC/SC Lite libraries

%description    libs
PC/SC Lite libraries.

%package        devel
Summary:        PC/SC Lite development files
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
PC/SC Lite development files.

%package        doc
Summary:        PC/SC Lite developer documentation
BuildArch:      noarch
Requires:       %{name}-libs = %{version}-%{release}

%description    doc
%{summary}.


%prep
%setup -q
%build
%configure \
  --disable-static \
  --enable-usbdropdir=%{_libdir}/pcsc/drivers

make %{?_smp_mflags}

doxygen doc/doxygen.conf ; rm -f doc/api/*.{map,md5}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Create empty directories
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/reader.conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pcsc/drivers
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/pcscd

rm $RPM_BUILD_ROOT%{_libdir}/*.la

# Remove documentation installed in a wrong directory
rm $RPM_BUILD_ROOT%{_docdir}/pcsc-lite/README.DAEMON


%post
%systemd_post pcscd.socket pcscd.service

%preun
%systemd_preun pcscd.socket pcscd.service

%postun
%systemd_postun_with_restart pcscd.socket pcscd.service

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog* DRIVERS HELP README SECURITY TODO
%dir %{_sysconfdir}/reader.conf.d/
%{_unitdir}/pcscd.service
%{_unitdir}/pcscd.socket
%{_sbindir}/pcscd
%dir %{_libdir}/pcsc/
%dir %{_libdir}/pcsc/drivers/
%{_mandir}/man5/reader.conf.5*
%{_mandir}/man8/pcscd.8*
%ghost %dir %{_localstatedir}/run/pcscd/

%files libs
%doc COPYING
%{_libdir}/libpcsclite.so.*

%files devel
%{_bindir}/pcsc-spy
%{_includedir}/PCSC/
%{_libdir}/libpcsclite.so
%{_libdir}/libpcscspy.so*
%{_libdir}/pkgconfig/libpcsclite.pc
%{_mandir}/man1/pcsc-spy.1*

%files doc
%doc doc/api/ doc/example/pcsc_demo.c


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.8.13-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

