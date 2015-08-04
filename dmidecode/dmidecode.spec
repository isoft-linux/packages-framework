Summary:        Tool to analyse BIOS DMI data
Name:           dmidecode
Version:        2.12
Release:        1 
Epoch:          1
Group:          System Environment/Base
License:        GPLv2+
Source0:        %{name}-%{version}.tar.gz
URL:            http://www.nongnu.org/dmidecode/

BuildRequires:  automake autoconf

Provides: /usr/sbin/dmidecode
ExclusiveArch:  %{ix86} x86_64 ia64

%description
dmidecode reports information about x86 & ia64 hardware as described in the
system BIOS according to the SMBIOS/DMI standard. This information
typically includes system manufacturer, model name, serial number,
BIOS version, asset tag as well as a lot of other details of varying
level of interest and reliability depending on the manufacturer.

This will often include usage status for the CPU sockets, expansion
slots (e.g. AGP, PCI, ISA) and memory module slots, and the list of
I/O ports (e.g. serial, parallel, USB).

%prep
%setup -q

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" CC=clang CXX=clang++

%install
rm -rf ${buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} prefix=%{_prefix} install-bin install-man

%clean
rm -rf ${buildroot}

%files
%defattr(-,root,root)
%{_sbindir}/dmidecode
%{_sbindir}/vpddecode
%{_sbindir}/ownership
%{_sbindir}/biosdecode
%{_mandir}/man8/*

