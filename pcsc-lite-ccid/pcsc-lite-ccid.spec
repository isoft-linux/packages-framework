%global dropdir %(pkg-config libpcsclite --variable usbdropdir 2>/dev/null)
%global pcsc_lite_ver 1.8.3
Name:           pcsc-lite-ccid
Version:        1.4.19
Release:        2
Summary:        Generic USB CCID smart card reader driver

License:        LGPLv2+
URL:            http://pcsclite.alioth.debian.org/ccid.html
Source0:        https://alioth.debian.org/frs/download.php/file/4132/ccid-%{version}.tar.bz2 

BuildRequires:  libusb1-devel
BuildRequires:  pcsc-lite-devel >= %{pcsc_lite_ver}
Requires(post): systemd
Requires(postun): systemd
Requires:       pcsc-lite >= %{pcsc_lite_ver}
Provides:       pcsc-ifd-handler
# Provide upgrade path from 'ccid' package
Obsoletes:      ccid < 1.4.0-3
Provides:       ccid = %{version}-%{release}

%description
Generic USB CCID (Chip/Smart Card Interface Devices) driver for use with the
PC/SC Lite daemon.


%prep
%setup -q -n ccid-%{version}


%build
%configure --enable-twinserial
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
cp -p src/openct/LICENSE LICENSE.openct


%post
/bin/systemctl try-restart pcscd.service >/dev/null 2>&1 || :

%postun
/bin/systemctl try-restart pcscd.service >/dev/null 2>&1 || :


%files
%doc AUTHORS ChangeLog COPYING LICENSE.openct README
%{dropdir}/ifd-ccid.bundle/
%{dropdir}/serial/
%config(noreplace) %{_sysconfdir}/reader.conf.d/libccidtwin


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.4.19-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

