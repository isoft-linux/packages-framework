Name:          usbmuxd
Version:       1.1.0
Release:       10
Summary:       Daemon for communicating with Apple's iOS devices

Group:         Applications/System
# All code is dual licenses as GPLv3+ or GPLv2+, except libusbmuxd which is LGPLv2+.
License:       GPLv3+ or GPLv2+ and LGPLv2+
URL:           http://www.libimobiledevice.org/
Source0:       http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2

# For systemd.macros
BuildRequires: systemd
BuildRequires: libplist-devel
BuildRequires: libusb-devel
BuildRequires: libusbmuxd-devel
Requires(pre): shadow-utils
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch, iPhone, 
iPad and Apple TV devices. It allows multiple services on the device to be 
accessed simultaneously.

%prep
%setup -q
%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%pre
getent group usbmux >/dev/null || groupadd -r usbmux -g 113
getent passwd usbmux >/dev/null || \
useradd -r -g usbmux -d / -s /sbin/nologin \
	-c "usbmux user" -u 113 usbmux
exit 0

%post
/sbin/ldconfig
%systemd_post usbmuxd.service

%preun
%systemd_preun usbmuxd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart usbmuxd.service 

%files
%doc AUTHORS README COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1 README.devel
%{_sbindir}/usbmuxd
%{_libdir}/udev/rules.d/39-usbmuxd.rules
%{_libdir}/systemd/system/usbmuxd.service
%{_mandir}/man1/usbmuxd.1.gz
%changelog
